import asyncio
import json
import time
import tomllib

import httpx
import numpy as np
import tiktoken
from openai.types.chat import ChatCompletion
from tqdm import trange

with open("openai.toml", "rb") as fin:
    cfg = tomllib.load(fin)
oai_token = cfg["key"]
azure_endpoint = cfg["azure_endpoint"]
deployment_name = cfg["deployment_name"]

api_version = "2023-07-01-preview"
encoding = tiktoken.encoding_for_model("gpt-4")
base_story = """In the bulstling cityscape, shadows whispered untold sotries. Emily, and enigmatic artist, unraveled mysteries through her canvases, each stroke a portal to forgotten realms. \
As twilight painted the skyline, her studio became a sanctuary of creativity. Yet, an ancient artifact, hidden within the citiy's heart, held the key to an unforseen destiny. \
Unbeknownst to Emily, the canvas she painted on was a conduit to realms beyond imagination. As the artifact's power awakened, her art became a bridge between worlds, intertwining \
reality and fantasy. Little did she know, her creations would shape the fate of both realms in ways unimaginable.\
"""
base_prompt = "Help me continue this story:\n"

import openai

oai_client = openai.AsyncAzureOpenAI(
    api_key=oai_token,
    azure_endpoint=azure_endpoint,
    api_version="2023-07-01-preview",
    azure_deployment=deployment_name,
    max_retries=0,  # demo only
)


async def gpt_async(i: int, prompt):
    # print("sent:", i)
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": prompt},
    ]

    response: ChatCompletion = await oai_client.chat.completions.create(
        model="gpt-4-32k",
        messages=messages,  # pyright: ignore
        temperature=0,
    )

    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         azure_endpoint
    #         + f"/openai/deployments/gpt-35-turb-16k/chat/completions?api-version={api_version}",
    #         json={"messages": messages, "temperature": 0},
    #         headers={"api-key": oai_token},
    #         timeout=None,
    #     )

    msg = ""
    # err = response.json().get("error") is not None
    err = json.loads(response.model_dump_json()).get("error") is not None
    if err:
        # msg = f"| Err: { response.json().get('error')['code'] }: { response.json().get('error')['message'] }"
        msg = f"| Err: { json.loads(response.model_dump_json()).get('error')['code'] }: { json.loads(response.model_dump_json()).get('error')['message'] }"

    return i, f"done: {i} {msg}"


async def main(rpm):
    # run the maximum number of requests based on the RPM limit
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for i in trange(rpm):
            # init requests (for future work regarding tracking tokens)
            spl = base_story.split(" ")
            idx = np.random.randint(len(spl))
            prompt = base_prompt + " ".join(spl[:idx])

            # kick off request asychronously
            t = tg.create_task(gpt_async(i + 1, prompt))
            tasks.append(t)

            # evenly space requests according the the RPM limit
            # extra = rpm * 0.07
            extra = 0
            await asyncio.sleep(60 / (rpm - extra))

    # collate results
    res = []
    for t in tasks:
        r = t.result()
        res.append((r[0], r[1]))

    # print the results of the requests. Specifically if any of them had an error
    print(len(res))
    res = [x[1] for x in sorted(res, key=lambda x: x[0])]
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    import os
    import sys

    os.system("clear")

    rpm = 72
    if len(sys.argv) > 1:
        rpm = sys.argv[1]
        rpm = int(rpm)
    print("*" * 80)
    print(f"RPM: {rpm}")
    x = time.time()
    asyncio.run(main(rpm))
    print(f"{time.time() - x:.3f} seconds elapsed")
    print("done")
