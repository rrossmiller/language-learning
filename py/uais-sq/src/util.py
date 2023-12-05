import asyncio
import json
import os

import openai

base_prompt = "Help me continue this story:\n"

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
oai_client = openai.AsyncAzureOpenAI(
    api_key=oai_token,
    azure_endpoint=azure_endpoint,
    api_version="2023-07-01-preview",
    azure_deployment=deployment_name,
)


async def gpt_async(
    i: int, prompt: str, project_id="200", bar=None, worker=None
) -> tuple[int, str]:
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": prompt},
    ]

    if bar is not None:
        bar.set_description_str(f"{worker} processing request {i}")
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
            extra_headers={"project-id": project_id},
        )

        if bar is not None:
            bar.set_description_str(f"{worker} got response {i}")

        msg = ""
        # use below if calling with httpx
        # err = response.json().get("error") is not None
        # if err:
        #     msg = f"| Err: { response.json().get('error')['code'] }: { response.json().get('error')['message'] }"

        # use below if calling with openai client
        err = json.loads(response.model_dump_json()).get("error") is not None
        if bar is not None and err:
            bar.set_description_str(f"{worker} err for {i}")
            await asyncio.sleep(10)

        if err:
            # msg = f"| Err: { response.json().get('error')['code'] }: { response.json().get('error')['message'] }"
            msg = f"| Err: { json.loads(response.model_dump_json()).get('error')['code'] }: { json.loads(response.model_dump_json()).get('error')['message'] }"
        return i, f"done: {i} {msg}"
    except Exception as e:
        return i, f"done: {i} | Err: {e}"


async def sleep(i: int):
    print(f"Sleeping for {i}")
    await asyncio.sleep(i)
