import torch
from torch import nn
from torch.nn import functional as F

device = "mps" if torch.backends.mps.is_available() else "cpu"
device = "cuda" if torch.cuda.is_available() else "cpu"
dropout = 0.2


class Head(nn.Module):
    def __init__(self, n_embed, head_size, block_size):
        super().__init__()
        self.key = nn.Linear(n_embed, head_size, bias=False)
        self.query = nn.Linear(n_embed, head_size, bias=False)
        self.value = nn.Linear(n_embed, head_size, bias=False)
        self.dropout = nn.Dropout(dropout)

        # part of the module, but not a parameter
        self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)

        # attention scores ("affinities")
        w = q @ k.transpose(-2, -1) * C**-0.5  # norm by 1/head_size
        w = w.masked_fill(self.tril[:T, :T] == 0, float("-inf"))  # B, T, T
        w = F.softmax(w, dim=-1)  # B, T, T
        w = self.dropout(w)

        # weighted agg of values
        val = self.value(x)  # B, T, C

        return w @ val  # (B,T,T) @ (B,T,C) --> B, T, C


class MultiHeadedAttention(nn.Module):
    def __init__(self, n_heads, n_embed, head_size, block_size):
        super().__init__()

        self.heads = nn.ModuleList(
            [Head(n_embed, head_size, block_size) for _ in range(n_heads)]
        )
        self.projection = nn.Linear(n_heads * head_size, n_embed)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.projection(x)
        out = self.dropout(x)
        return out


class FF(nn.Module):
    def __init__(self, n_embed):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embed, 4 * n_embed),
            nn.ReLU(),
            nn.Linear(4 * n_embed, n_embed),  # projection
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    def __init__(self, n_heads, n_embed, block_size):
        super().__init__()
        head_size = n_embed // n_heads
        self.sa = MultiHeadedAttention(n_heads, n_embed, head_size, block_size)
        self.ffwd = FF(n_embed)
        self.ln1 = nn.LayerNorm(n_embed)
        self.ln2 = nn.LayerNorm(n_embed)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class NanoGPT(nn.Module):
    def __init__(self, vocab_size, block_size, n_embed):
        super().__init__()

        self.token_embedding_table = nn.Embedding(vocab_size, n_embed)
        self.position_embedding_table = nn.Embedding(block_size, n_embed)
        # self.sa_head = Head(n_embed, n_embed, block_size)

        n_heads = 6
        n_blocks = 6
        self.blocks = nn.Sequential(
            *[Block(n_heads, n_embed, block_size) for _ in range(n_blocks)]
        )

        self.lnorm = nn.LayerNorm(n_embed)
        self.lm_head = nn.Linear(n_embed, vocab_size)

        self.block_size = block_size

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tkn_emb = self.token_embedding_table(idx)  # (Batch, Time, Channel) tensor
        pos_emb = self.position_embedding_table(torch.arange(T, device=device))  # (T, C)
        x = tkn_emb + pos_emb
        x = self.blocks(x)
        x = self.lnorm(x)
        logits = self.lm_head(x)  # (Batch, Time, n_embed) tensor

        if targets is not None:
            B, T, C = logits.shape
            logits = logits.view(B * T, C)
            targets = targets.view(B * T)
            loss = F.cross_entropy(logits, targets)
        else:
            loss = None
        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size :]
            # get the predictions
            logits, loss = self(
                idx_cond
            )  # you don't need to pass in whole context... it's just a bigram model
            # focus only on the last time step
            logits = logits[:, -1, :]  # becomes (B, C)

            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1)  # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)

        return idx
