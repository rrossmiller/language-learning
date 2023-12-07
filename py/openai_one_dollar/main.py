import asyncio
import json
import os
import re
from typing import Any

import openai
import tiktoken
from rate_limiter import RateLimiter, worker
from tqdm import tqdm

encoder = tiktoken.encoding_for_model("gpt-4")
prompt = """Help me complete this story:
In the bulstling cityscape, shadows whispered untold sotries. Emily, and enigmatic artist, unraveled mysteries through her canvases, each stroke a portal to forgotten realms. \
As twilight painted the skyline, her studio became a sanctuary of creativity. Yet, an ancient artifact, hidden within the citiy's heart, held the key to an unforseen destiny. \
Unbeknownst to Emily, the canvas she painted on was a conduit to realms beyond imagination. As the artifact's power awakened, her art became a bridge between worlds, intertwining \
reality and fantasy. Little did she know, her creations would shape the fate of both realms in ways unimaginable."""


rl = RateLimiter(90_000)

if not os.path.exists("openai.toml"):
    cfg = {
        "key": os.environ["KEY"],
    }
else:
    import tomllib

    with open("openai.toml", "rb") as fin:
        cfg = tomllib.load(fin)
oai_token = cfg["KEY"]
oai_client = openai.AsyncClient(api_key=oai_token)


async def gpt_async(i: int, prompt: str, bar=None, worker=None) -> tuple[int, str, Any]:
    messages = [
        {"role": "user", "content": prompt},
    ]

    if bar is not None:
        bar.set_description_str(f"{worker} processing request {i}")

    # the rate limiter does not handle errors gracefully. That's up to you for now.
    try:
        response = await oai_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,  # pyright: ignore
            temperature=0,
        )

        if bar is not None:
            bar.set_description_str(f"{worker} got response {i}")

        msg = ""
        err = json.loads(response.model_dump_json()).get("error") is not None
        if bar is not None and err:
            bar.set_description_str(f"{worker} err for {i}")
            await asyncio.sleep(1)

        if err:
            # msg = f"| Err: { response.json().get('error')['code'] }: { response.json().get('error')['message'] }"
            msg = f"| Err: { json.loads(response.model_dump_json()).get('error')['code'] }: { json.loads(response.model_dump_json()).get('error')['message'] }"
        return i, f"done: {i} {msg}", response.usage
    except Exception as e:
        return i, f"done: {i} | Err: {e}", None


async def rpm_no_err(n_tasks, n_workers=30, worker_bars=True):
    # init the task queue of requests that will be sent to gpt
    task_queue = asyncio.Queue()
    ttl_tokens = 0

    for i in range(n_tasks):
        # init requests (for future work regarding tracking tokens)
        # add job to the queue (function, args)
        task_queue.put_nowait((gpt_async, (i, prompt)))
        ttl_tokens += len(encoder.encode(prompt))

    # Create N workers to process the queue concurrently.
    loop = asyncio.get_event_loop()
    tasks: list[asyncio.Task] = []
    ttl_tracker = None
    # if worker_bars:
    ttl_tracker = tqdm(position=0, total=n_tasks, desc="Tasks", unit="tasks")
    for n in range(min(n_tasks, n_workers)):
        task = loop.create_task(
            worker(n, rl, task_queue, ttl_tracker=ttl_tracker, worker_bars=worker_bars)
        )
        tasks.append(task)

    # wait for workers to finish jobs
    await task_queue.join()

    # if worker_bars:
    ttl_tracker.close()  # pyright: ignore

    # collate task results
    results = []
    for t in tasks:
        r: list = t.result()
        if r[1] is not None:
            r[1].close()
        r = r[0]
        results.extend(r)

    # print the results of the requests. Specifically, if any of them had an error
    # res = [x[1] for x in sorted(results, key=lambda x: x[0])]
    # print(json.dumps(res, indent=2))
    # print(len(results))
    print()
    errs = 0
    err_msgs = []
    for x in sorted(results, key=lambda x: x[0]):
        if "Err" in x[1]:
            errs += 1
            json_string = re.search(r"\{.*\}", x[1])
            if json_string is not None:
                json_string = json_string.group(0).replace("'", '"')
                # msg = json.loads(json_string)
                # err_msgs.append(msg["error"]["message"])
                err_msgs.append(json_string)
            else:
                print(x[1])
                raise Exception("error parsing error message")
    print(f"{errs} errors")
    err_msgs = list(set(err_msgs))
    nl = "\n\t - "
    print(f"Unique error messages:\n\t{nl.join(x for x in err_msgs)}")
    print(f"Total tokens used: {ttl_tokens}")
    return errs


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--disable-worker-bars", action="store_true")
    parser.add_argument("--n-tasks", type=int, default=-1)
    parser.add_argument("--n-workers", type=int, default=32)
    args = parser.parse_args()

    worker_bars = not args.disable_worker_bars
    n_workers = args.n_workers

    os.system("clear")
    RateLimiter(90_000)

    # get the rate limit
    n_tasks = rl.rpm
    if args.n_tasks > 0:
        n_tasks = args.n_tasks
    # print("worker bars:", worker_bars)
    # print("n tasks:", n_tasks)
    errs = asyncio.run(rpm_no_err(n_tasks, n_workers=n_workers, worker_bars=worker_bars))
