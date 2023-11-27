import os

import matplotlib.pyplot as plt
import pandas as pd
import torch
from tqdm import trange

from bigram_model import BiGramLanguageModel

torch.manual_seed(1337)


# hyperparams
batch_size =32 
block_size = 8
max_iters = 50_000
learning_rate = 1e-2


def get_batch(data: torch.Tensor):
    ix = torch.randint(
        len(data) - block_size, (batch_size,)
    )  # get [batchsize X 1] random numbers betwen 0 and len(data)-block_size (so when building chunks, no index out of bounds)
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
    return x, y


def train(model: torch.nn.Module, data: torch.Tensor):
    device = (
        torch.device("mps")
        if torch.backends.mps.is_available()
        else torch.device("cpu")
    )
    # model.to(device)
    # data.to(device)
    batch_size = 32
    # typical lr would be 3e-4, but BiGram is small
    optim = torch.optim.AdamW(model.parameters(), lr=1e-3)

    losses = []
    for _ in trange(50000):
        xb, yb = get_batch(data)
        # xb.to(device)
        # yb.to(device)

        logits, loss = model(xb, yb)
        optim.zero_grad(set_to_none=True)
        loss.backward()
        optim.step()

        losses.append(loss.item())

    # pd.DataFrame({"loss": losses}).plot()
    # plt.show()

    print("generate:")
    idx = torch.ones(1, 1, dtype=torch.long)
    print(decode(bigram_model.generate(idx, 300)[0].tolist()))


if __name__ == "__main__":
    os.system("clear")

    # read the data
    with open("../data/shakespeare.txt") as f:
        text = f.read()

    chars = sorted(list(set(text)))
    stoi = {c: i for i, c in enumerate(chars)}
    itos = {i: c for i, c in enumerate(chars)}
    encode = lambda x: [stoi[c] for c in x]
    decode = lambda x: "".join(itos[c] for c in x)

    print(f"chars: {''.join(c for c in chars[1:])}")
    vocab_size = len(chars)

    # encode data
    data = torch.tensor(encode(text), dtype=torch.long)
    print(data[:10])

    n = int(0.9 * len(data))
    train_data, val_data = data[:n], data[n:]

    # chunking text
    # Example test block
    x = train_data[:block_size]
    y = train_data[1 : block_size + 1]

    print()
    for t in range(block_size):
        context = x[: t + 1]
        target = y[t]
        print(f"Input: {str(context.tolist()):<35} | Target: {target.tolist()}")

    # Batching
    xb, yb = get_batch(train_data)
    print()
    print("inputs")
    print(xb.shape)
    print(xb)
    print("targets")
    print(yb.shape)
    print(yb)

    ##### BiGramModel
    print()
    bigram_model = BiGramLanguageModel(vocab_size)
    out, loss = bigram_model(xb, yb)
    print(out.shape, loss)

    # testing generate
    print("generate:")
    idx = torch.ones(1, 1, dtype=torch.long)
    print(decode(bigram_model.generate(idx, 100)[0].tolist()))

    # train
    print()
    train(bigram_model, train_data)
