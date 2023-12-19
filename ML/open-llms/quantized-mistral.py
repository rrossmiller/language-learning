# From this article: https://levelup.gitconnected.com/a-step-by-step-guide-to-runing-mistral-7b-ai-on-a-single-gpu-with-google-colab-274a20eb9e40
import os

import torch
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          BitsAndBytesConfig)

device = "cuda" if torch.cuda.is_available() else "mps"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=False,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model_id = "mistralai/Mistral-7B-Instruct-v0.1"
model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb_config, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

os.system("clear")
print()
while True:
    q = input("> ")
    if len(q) == 0:
        q = "Explain to me what is Large Language Model. Assume that I am a 5-year-old child."

    else:
        q = q.replace("\n", "")

    PROMPT = f"""### Instruction: You are a baseball expert. You know every player who has ever played. However, you're not afraid to say\
    you don't know, or that something doesn't exist.
### Question:
{q}

### Answer:"""

    encodeds = tokenizer(PROMPT, return_tensors="pt", add_special_tokens=True)
    model_inputs = encodeds.to(device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1000,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    decoded = tokenizer.batch_decode(generated_ids)
    print(decoded[0])
