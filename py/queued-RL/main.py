import asyncio
import json
import time
import tomllib

import numpy as np
import openai
from tqdm import tqdm

from rate_watcher import RateLimiter, worker

with open("openai.toml", "rb") as fin:
    cfg = tomllib.load(fin)
oai_token = cfg["key"]
azure_endpoint = cfg["azure_endpoint"]
deployment_name = cfg["deployment_name"]

api_version = "2023-07-01-preview"
base_story = """In the bulstling cityscape, shadows whispered untold sotries. Emily, and enigmatic artist, unraveled mysteries through her canvases, each stroke a portal to forgotten realms. \
As twilight painted the skyline, her studio became a sanctuary of creativity. Yet, an ancient artifact, hidden within the citiy's heart, held the key to an unforseen destiny. \
Unbeknownst to Emily, the canvas she painted on was a conduit to realms beyond imagination. As the artifact's power awakened, her art became a bridge between worlds, intertwining \
reality and fantasy. Little did she know, her creations would shape the fate of both realms in ways unimaginable.\
"""
base_prompt = "Help me continue this story:\n"


oai_client = openai.AsyncAzureOpenAI(
    api_key=oai_token,
    azure_endpoint=azure_endpoint,
    api_version="2023-07-01-preview",
    azure_deployment=deployment_name,
)
# init rate tracker
rl = RateLimiter(12_000)


async def gpt_async(i: int, prompt, bar, worker) -> tuple[int, str]:
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": prompt},
    ]

    if bar is not None:
        bar.set_description_str(f"{worker} Sent request {i}")
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         azure_endpoint
    #         + f"/openai/deployments/gpt-35-turb-16k/chat/completions?api-version={api_version}",
    #         json={"messages": messages, "temperature": 0},
    #         headers={"api-key": oai_token},
    #         timeout=None,
    #     )

    # the rate limiter does not handle errors gracefully. That's up to you for now.
    try:
        response = await oai_client.chat.completions.create(
            model="gpt35-turbo",
            messages=messages,  # pyright: ignore
            temperature=0,
            extra_headers={"project-id": "9"},
        )
    except Exception as e:
        return i, f"done: {i} | Err: {e}"

    msg = ""
    # use below if calling with httpx
    # err = response.json().get("error") is not None
    # if err:
    #     msg = f"| Err: { response.json().get('error')['code'] }: { response.json().get('error')['message'] }"

    # use below if calling with openai client
    err = json.loads(response.model_dump_json()).get("error") is not None
    if err:
        # msg = f"| Err: { response.json().get('error')['code'] }: { response.json().get('error')['message'] }"
        msg = f"| Err: { json.loads(response.model_dump_json()).get('error')['code'] }: { json.loads(response.model_dump_json()).get('error')['message'] }"

    return i, f"done: {i} {msg}"


async def main(n_tasks, n_workers=30):
    # init the task queue of requests that will be sent to gpt
    task_queue = asyncio.Queue()

    for i in range(n_tasks):
        # init requests (for future work regarding tracking tokens)
        spl = base_story.split(" ")
        idx = np.random.randint(len(spl))
        prompt = base_prompt + " ".join(spl[:idx])

        # add job to the queue (function, args)
        task_queue.put_nowait((gpt_async, (i, prompt)))

    # Create N workers to process the queue concurrently.
    loop = asyncio.get_event_loop()
    tasks: list[asyncio.Task] = []
    ttl_tracker = tqdm(position=0, total=n_tasks, desc="Tasks")
    for n in range(min(n_tasks, n_workers)):
        task = loop.create_task(
            worker(n, rl, task_queue, ttl_tracker=ttl_tracker, worker_bars=True)
        )
        tasks.append(task)

    # wait for workers to finish jobs
    await task_queue.join()

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
    assert len(results) == n_tasks
    errs = 0
    for x in sorted(results, key=lambda x: x[0]):
        if "Err" in x[1]:
            errs += 1
    print(f"{errs} errors")


if __name__ == "__main__":
    import os
    import sys

    os.system("clear")

    # get the rate limit
    n_tasks = rl.rpm  # * 2
    if len(sys.argv) > 1:
        n_tasks = sys.argv[1]
        n_tasks = int(n_tasks)
    print("*" * 80)
    print(f"Running {n_tasks} tasks")

    # start the main loop
    x = time.monotonic()
    asyncio.run(main(n_tasks, n_workers=32))
    print(f"{time.monotonic() - x:.2f} seconds elapsed")
