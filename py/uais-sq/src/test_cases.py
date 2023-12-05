import asyncio
import json
import os
import re
import time

import httpx
import numpy as np
import tiktoken
from rate_limiter import RateLimiter, worker
from tqdm import tqdm
from util import gpt_async, sleep

np.random.seed(42)


# TODO: remove progress bars when running in gh
# make it an arg that gh passes in

if not os.path.exists("openai.toml"):
    cfg = {
        "key": os.environ["AZURE_OAI_KEY"],
        "azure_endpoint": os.environ["AZURE_OAI_ENDPOINT"],
        "deployment_name": os.environ["AZURE_OAI_DEPL_NAME"],
    }
else:
    import tomllib

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


encoder = tiktoken.encoding_for_model("gpt-4")
# init rate tracker
rl = RateLimiter(12_000)


async def rpm_no_err(n_tasks, n_workers=30, worker_bars=True):
    # init the task queue of requests that will be sent to gpt
    task_queue = asyncio.Queue()
    ttl_tokens = 0

    for i in range(n_tasks):
        # init requests (for future work regarding tracking tokens)
        spl = base_story.split(" ")
        idx = np.random.randint(len(spl))
        prompt = base_prompt + " ".join(spl[:idx])

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
    assert len(results) == n_tasks
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


async def rpm_err(rpm=3):
    # fire off workers in quick succession with no regard for spacing
    task_queue = []
    ttl_tokens = 0
    async with asyncio.TaskGroup() as tg:
        start = time.monotonic()
        for i in range(rpm + 5):
            # init requests (for future work regarding tracking tokens)
            spl = base_story.split(" ")
            idx = np.random.randint(len(spl))
            prompt = base_prompt + " ".join(spl[:idx])
            t = tg.create_task(gpt_async(i, prompt, project_id=str(rpm)))
            ttl_tokens += len(encoder.encode(prompt))

            # add job to the queue (function, args)
            task_queue.append(t)

        print(f"Sent {rpm+5} requests in {time.monotonic() - start} seconds")
        print(f"Total tokens used: {ttl_tokens}")

    # collate task results
    results = []
    for t in task_queue:
        r = t.result()
        results.append(r)

    # print the results of the requests. Specifically, if any of them had an error
    # res = [x[1] for x in sorted(results, key=lambda x: x[0])]
    # print(json.dumps(res, indent=2))
    # print(len(results))
    print()
    assert len(results) == rpm + 5, f"{len(results)} != {rpm+5}"
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

    nl = "\n\t - "
    print(f"Unique error messages:\n\t{nl.join(x for x in set(err_msgs))}")
    return errs


async def tpm_err(n_workers=30):
    # make requests with enough tokens to not trip RPM limit and not exceed model's context length
    # GPT 35-turbo context size is 4096 tokens per request
    tpm_prompt = "One evening, as Emily stood in her studio, brush in hand, she felt a strange energy emanating from the artifact hidden within the city's heart. It pulsed with a vibrant light, beckoning her closer. Curiosity consumed her, and she couldn't resist the allure of the artifact's power.\n\nWith trembling hands, Emily reached out and touched the artifact. Instantly, a surge of energy coursed through her veins, filling her with a newfound sense of purpose. She realized that her art was not just a means of expression but a tool to shape the destiny of both realms.\n\nAs she returned to her canvas, Emily's strokes became bolder and more deliberate. Each stroke seemed to breathe life into her creations, and the worlds she painted came alive before her eyes. The once static images now moved and danced, as if they had a mind of their own.\n\nWord of Emily's extraordinary talent spread throughout the city, attracting the attention of both artists and collectors. They flocked to her studio, eager to witness the magic that unfolded on her canvases. But Emily knew that her art was not just for entertainment; it held the power to heal, to inspire, and to change the course of history.\n\nOne day, a visitor arrived at Emily's studio, a wise old man who claimed to be a guardian of the artifact. He explained that the artifact was a relic from a forgotten era, a time when the boundaries between realms were fluid and interconnected. He revealed that Emily was chosen to be the guardian of this ancient power, entrusted with the responsibility to use her art for the greater good.\n\nWith the guidance of the old man, Emily delved deeper into her artistic abilities. She learned to channel her emotions and intentions into her paintings, infusing them with purpose and meaning. Each stroke became a deliberate act of creation, shaping the destiny of both realms.\n\nAs Emily's art gained recognition, she used her newfound influence to bring about positive change. She painted scenes of unity and harmony, inspiring people to come together and bridge the gaps between their differences. Her art became a catalyst for social change, sparking conversations and igniting a collective desire for a better world.\n\nBut as Emily's creations grew more powerful, so did the forces that sought to control them. Dark entities from the realms beyond imagination sensed the artifact's awakening and sought to harness its power for their own nefarious purposes. They sent their minions to steal the artifact, hoping to use it to plunge both realms into chaos.\n\nEmily, now aware of the danger, rallied her allies and embarked on a perilous journey to protect the artifact. With her brush as her weapon and her art as her shield, she fought against the darkness that threatened to consume everything she held dear.\n\nIn the final battle, Emily stood before the dark entities, her canvas glowing with an ethereal light. With a single stroke, she unleashed a wave of pure energy, banishing the darkness and restoring balance to the realms. The artifact, now free from the clutches of evil, returned to its dormant state, awaiting the next guardian who would rise to the challenge.\n\nEmily, exhausted but triumphant, returned to her studio. She knew that her journey was far from over, but she also knew that her art would continue to shape the fate of both realms. With renewed determination, she picked up her brush and began to paint, ready to create a world where imagination and reality intertwined, where shadows whispered untold stories, and where her art would forever be a bridge between worlds."
    tpm_prompt_tkns = len(encoder.encode(tpm_prompt))

    # init the task queue of requests that will be sent to gpt
    task_queue = asyncio.Queue()
    ttl_tokens = 0
    n_tasks = int(min(rl.tpm / tpm_prompt_tkns, rl.rpm)) + 10

    for i in range(n_tasks):
        # init requests (for future work regarding tracking tokens)

        # add job to the queue (function, args)
        task_queue.put_nowait((gpt_async, (i, tpm_prompt)))
        ttl_tokens += tpm_prompt_tkns

    print(f"Total tokens used: {ttl_tokens:,}")

    # Create N workers to process the queue concurrently.
    loop = asyncio.get_event_loop()
    tasks: list[asyncio.Task] = []
    ttl_tracker = tqdm(position=0, total=n_tasks, desc="Tasks", unit="tasks")
    for n in range(min(n_tasks, n_workers)):
        task = loop.create_task(
            worker(n, rl, task_queue, ttl_tracker=ttl_tracker, worker_bars=worker_bars)
        )
        tasks.append(task)

    # wait for workers to finish jobs
    await task_queue.join()

    ttl_tracker.close()
    # collate task results
    results = []
    for t in tasks:
        r: list = t.result()
        if r[1] is not None:
            r[1].close()
        r = r[0]
        results.extend(r)

    print()
    assert len(results) == n_tasks, f"{len(results)} != {n_tasks}"
    errs = 0
    err_msgs = []
    for x in sorted(results, key=lambda x: x[0]):
        if "Err" in x[1]:
            errs += 1
            json_string = re.search(r"\{.*\}", x[1])
            if json_string is not None:
                json_string = json_string.group(0).replace("'", '"')
                msg = json.loads(json_string)
                err_msgs.append(msg["error"]["message"])
            else:
                print(x[1])
                print("error parsing error message")
                return 0
    print(f"{errs} errors")

    nl = "\n\t - "
    print(f"Unique error messages:\n\t{nl.join(x for x in set(err_msgs))}")
    return errs


async def test_authnz(headers):
    url = f"{azure_endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    headers["api-key"] = oai_token
    messages = [{"role": "user", "content": "hello"}]
    response = httpx.post(
        url, headers=headers, json={"messages": messages}, timeout=None
    )
    if response.status_code == 200:
        return ""
    else:
        return response.reason_phrase


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--disable-worker-bars", action="store_true")
    parser.add_argument("--n-tasks", type=int, default=-1)
    args = parser.parse_args()

    worker_bars = not args.disable_worker_bars

    os.system("clear")

    # get the rate limit
    n_tasks = rl.rpm
    if args.n_tasks > 0:
        n_tasks = args.n_tasks

    try:
        """
        Test calling the model with an invalid project-id. This will throw a 401 unauthorized error.
        """
        print("*" * 80)
        print("Testing auth - no err")
        headers = {"project-id": "10"}
        response = asyncio.run(test_authnz(headers))
        assert response == ""
        # no project id header
        print("Testing auth - missing project-id header")
        time.sleep(1)
        response = asyncio.run(test_authnz({}))
        assert response == "You must provide a `project-id` header"
        # project id header is invalid
        print("Testing auth - invalid header")
        time.sleep(1)
        headers = {"project-id": "-1"}
        response = asyncio.run(test_authnz(headers))
        assert response == "Not Found"

        # no RPM error
        asyncio.run(sleep(5))
        """
        Test calling the model through APIM at the fastest rate possible without tripping the RPM limit.
        """
        print()
        print("*" * 80)
        print("Testing RPM limit - no err")
        x = time.monotonic()
        errs = asyncio.run(
            rpm_no_err(n_tasks + 5, n_workers=32, worker_bars=worker_bars)
        )
        print(f"{time.monotonic() - x:.2f} seconds elapsed")
        assert errs == 0, "There was a RPM error when there should not have been"

        # RPM error
        """
        Test calling the model through APIM as fast as possible. This will cause at least one 429 rate limit error for exceeding the RPM limit.
        """
        print()
        print("*" * 80)
        print(f"This test will cause an RPM error")
        x = time.monotonic()
        errs = asyncio.run(rpm_err(3))
        print(f"{time.monotonic() - x:.2f} seconds elapsed")
        assert errs > 0, "There was no RPM error when there should have been"

        # no TPM error
        print()

        # TPM error
        # time.sleep(60)
        # print("*" * 80)
        # print(f"This test will cause a TPM error")
        # x = time.monotonic()
        # errs = asyncio.run(tpm_err(n_tasks))
        # print(f"{time.monotonic() - x:.2f} seconds elapsed")
        # assert errs > 0, "There was no TPM error when there should have been."
    except AssertionError as e:
        print(e)

    print("*** DONE ***")
