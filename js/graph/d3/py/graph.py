import json
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("edges.csv")[["src", "tgt"]]
src = 1375238007  # df.sample(1)["src"].to_numpy()[0]
print(src)
df = df.loc[df["src"] == src]
df = df.astype(str)
print(df.head())
g = nx.Graph()
g.add_edges_from(df.to_numpy())

nx.draw(g)
plt.savefig("g.png")

out = {
    "nodes": [{"id": 0, "name": x} for x in df["src"].unique().tolist()],
    "links": [],
}

i = 1
for r in df.to_numpy():
    out["nodes"].append({"id": i, "name": r[1]})
    out["links"].append({"source": 0, "target": i})
    i += 1

with open("../src/edges.json", "w") as fout:
    json.dump(out, fout, indent=2)
