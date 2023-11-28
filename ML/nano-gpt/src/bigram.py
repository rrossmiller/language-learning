import os

import torch
from tqdm import trange

from bigram_model import BiGramLanguageModel

torch.manual_seed(1337)
torch.set_printoptions(precision=4)


# hyperparams
n_embed = 256
batch_size = 32
block_size = 8
learning_rate = 1e-2
max_iters = 5000
eval_iters = 200
eval_interval = 300
# ---------------
device = "mps" if torch.backends.mps.is_available() else "cpu"


def get_batch(data: torch.Tensor):
    ix = torch.randint(
        len(data) - block_size, (batch_size,)
    )  # get [batchsize X 1] random numbers betwen 0 and len(data)-block_size (so when building chunks, no index out of bounds)
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
    return x.to(device), y.to(device)


@torch.no_grad()
def estimate_loss(model, train_data, val_data):
    out = {}
    model.eval()
    for m, split in [("train", train_data), ("val", val_data)]:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            _, loss = model(X, Y)
            losses[k] = loss.item()
        out[m] = losses.mean()
    model.train()
    return out


def train(
    model: torch.nn.Module,
    train_data: torch.Tensor,
    val_data: torch.Tensor,
    print_loss=False,
):
    print("using:", device)
    # typical lr would be 3e-4, but BiGram is small
    optim = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    losses = []
    t = trange(max_iters)
    for i in t:
        # every once in a while evaluate the loss on train and val sets
        if i % eval_interval == 0:
            l = estimate_loss(model, train_data, val_data)
            t.set_postfix(
                {
                    "step": i,
                    "train loss": l["train"].item(),
                    "val loss": l["val"].item(),
                }
            )

        xb, yb = get_batch(train_data)
        xb.to(device)
        yb.to(device)

        _, loss = model(xb, yb)
        optim.zero_grad(set_to_none=True)
        loss.backward()
        optim.step()

        losses.append(loss.item())

    if print_loss:
        import matplotlib.pyplot as plt
        import pandas as pd

        pd.DataFrame({"loss": losses}).plot()
        plt.show()

    print("generate:")
    idx = torch.ones(1, 1, dtype=torch.long, device=device)
    print(decode(bigram_model.generate(idx, 300)[0].tolist()))
    torch.save(model.state_dict(), "bigram_model.pt")


def gen(decode, vocab_size):
    model = BiGramLanguageModel(vocab_size, n_embed)

    st_dict = torch.load("bigram_model.pt")
    model.load_state_dict(st_dict)
    model.to(device)
    model.eval()
    print("generate:")
    idx = torch.ones(1, 1, dtype=torch.long, device=device)
    print(decode(model.generate(idx, 300)[0].tolist()))


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
    # print(data[:10])

    n = int(0.9 * len(data))
    train_data, val_data = data[:n], data[n:]

    # chunking text
    # # Example test block
    # x = train_data[:block_size]
    # y = train_data[1 : block_size + 1]
    #
    # print()
    # for t in range(block_size):
    #     context = x[: t + 1]
    #     target = y[t]
    #     print(f"Input: {str(context.tolist()):<35} | Target: {target.tolist()}")

    # Batching
    # xb, yb = get_batch(train_data)
    # print()
    # print("inputs")
    # print(xb.shape)
    # print(xb)
    # print("targets")
    # print(yb.shape)
    # print(yb)

    ##### BiGramModel
    bigram_model = BiGramLanguageModel(vocab_size, n_embed)
    bigram_model.to(device)
    # print()
    # out, loss = bigram_model(xb, yb)
    # print(out.shape, loss)

    # # testing generate
    # print("generate:")
    # idx = torch.ones(1, 1, dtype=torch.long)
    # print(decode(bigram_model.generate(idx, 100)[0].tolist()))

    print(next(bigram_model.parameters()).device)
    print(train_data.device)
    # assert next(bigram_model.parameters()).device == train_data.device
    # train
    print()
    train(bigram_model, train_data, val_data)
