import torch
from transformers import pipeline

generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")

while True:
    i = input("> ")
    if len(i)==0:
        res = generate_text("Explain to me the difference between nuclear fission and fusion.")
    else:
        res = generate_text(i.replace('\n',''))
    print()
    print(res[0]["generated_text"]) # pyright: ignore

