import dgl
from dgl.data import FraudDataset
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import torch
from torch.nn import functional as F
import pytorch_lightning as pl
import dgl.nn.pytorch as gnn
from torchmetrics import F1Score
from dgl.dataloading import DataLoader
from pytorch_lightning.loggers import MLFlowLogger
import matplotlib.pyplot as plt


class GCN(pl.LightningModule):
    # class GCN(nn.Module):
    def __init__(self, g, in_feats, h_feats, num_classes, rel_names, batch_size=1):
        super().__init__()
        # len(output_nodes) = batch_size

        self.labels = g.ndata["label"]
        self.train_mask = g.ndata["train_mask"].to(bool)
        self.val_mask = g.ndata["val_mask"].to(bool)
        self.test_mask = g.ndata["test_mask"].to(bool)

        if False:
            self.f1 = F1Score("binary").to("cuda")
        else:
            self.f1 = F1Score("binary")

        self.conv0 = gnn.HeteroGraphConv(
            {rel: gnn.SAGEConv(in_feats, h_feats, "mean") for rel in rel_names}
        )
        self.conv1 = gnn.HeteroGraphConv(
            {rel: gnn.SAGEConv(h_feats, num_classes, "mean") for rel in rel_names}
        )
        # self.conv0 = gnn.HeteroGraphConv(
        #     {
        #         "net_rsr": gnn.GraphConv(in_feats, h_feats),
        #         "net_rtr": gnn.GraphConv(in_feats, h_feats),
        #         "net_rur": gnn.GraphConv(in_feats, h_feats),
        #     },
        #     aggregate="sum",
        # )
        # self.conv1 = gnn.HeteroGraphConv(
        #     {
        #         "net_rsr": gnn.GraphConv(h_feats, num_classes),
        #         "net_rtr": gnn.GraphConv(h_feats, num_classes),
        #         "net_rur": gnn.GraphConv(h_feats, num_classes),
        #     },
        #     aggregate="sum",
        # )

    def forward(self, g, in_feat):
        h = self.conv0(g, in_feat)
        h = F.relu(h["review"])
        h = self.conv1(g, {"review": h})
        return h

    def training_step(self, batch, batch_idx):
        # mini batch training -- https://docs.dgl.ai/en/latest/guide/minibatch-node.html#guide-minibatch-node-classification-sampler
        # Forward
        input_nodes, output_nodes, blocks = batch

        # fwd pass
        h = blocks[0].ndata["feature"]
        h = self.conv0(blocks[0], h)
        h = F.relu(h["review"])
        logits = self.conv1(blocks[1], {"review": h})["review"]

        # Compute prediction
        pred = logits.argmax(1).to(torch.int8)

        # Compute loss
        loss = F.cross_entropy(
            logits,
            self.labels[output_nodes],
        )

        # Compute accuracy on training/validation/test
        train_acc = (pred == self.labels[output_nodes]).float().mean()

        self.log(
            "loss", loss, prog_bar=True, on_epoch=True, batch_size=len(output_nodes)
        )
        self.log(
            "acc",
            train_acc,
            prog_bar=True,
            on_epoch=True,
            batch_size=len(output_nodes),
        )
        return {"loss": loss, "acc": train_acc}

    def validation_step(self, batch, batch_idx):
        # Forward
        input_nodes, output_nodes, blocks = batch

        # fwd pass
        h = blocks[0].ndata["feature"]
        h = self.conv0(blocks[0], h)
        h = F.relu(h["review"])
        logits = self.conv1(blocks[1], {"review": h})["review"]

        # Compute prediction
        pred = logits.argmax(1).to(torch.int8)

        # Compute loss
        loss = F.cross_entropy(
            logits,
            self.labels[output_nodes],
        )

        # Compute accuracy on training/validation/test
        val_acc = (pred == self.labels[output_nodes]).float().mean()
        f1 = self.f1(pred, self.labels[output_nodes]).item()

        self.log(
            "val_loss",
            loss,
            prog_bar=True,
            on_epoch=True,
            batch_size=len(output_nodes),
        )
        self.log(
            "val_acc",
            val_acc,
            prog_bar=True,
            on_epoch=True,
            batch_size=len(output_nodes),
        )
        self.log(
            "val_f1", f1, prog_bar=True, on_epoch=True, batch_size=len(output_nodes)
        )
        return {"val_loss": loss, "val_acc": val_acc, "val_f1": f1}

    def test_step(self, batch, batch_idx):
        # Forward
        input_nodes, output_nodes, blocks = batch

        # fwd pass
        h = blocks[0].ndata["feature"]
        h = self.conv0(blocks[0], h)
        h = F.relu(h["review"])
        logits = self.conv1(blocks[1], {"review": h})["review"]

        # Compute prediction
        pred = logits.argmax(1).to(torch.int8)

        # Compute loss
        loss = F.cross_entropy(
            logits,
            self.labels[output_nodes],
        )

        # Compute accuracy on training/validation/test
        test_acc = (pred == self.labels[output_nodes]).float().mean()
        f1 = self.f1(pred, self.labels[output_nodes]).item()

        self.log(
            "test_loss",
            loss,
            prog_bar=True,
            on_epoch=True,
            batch_size=len(output_nodes),
        )
        self.log(
            "test_acc",
            test_acc,
            prog_bar=True,
            on_epoch=True,
            batch_size=len(output_nodes),
        )
        self.log("f1", f1, prog_bar=True, on_epoch=True, batch_size=len(output_nodes))
        return {"test_loss": loss, "test_acc": test_acc, "f1": f1}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.01)


if __name__ == "__main__":
    dataset = FraudDataset("yelp")
    g = dataset[0]
    print(g.etypes)
    print(g.ntypes)
    print(g.ndata)
    print(g.ndata.keys())
    print()
    print(g.ndata["feature"])

    mask = g.ndata["train_mask"].to(bool)
    l = {0: 0, 1: 0}

    for x in g.ndata["label"][mask].numpy():
        l[x] += 1
    print(l, l[0] / (mask.sum()))

    mask = g.ndata["val_mask"].to(bool)
    l = {0: 0, 1: 0}

    for x in g.ndata["label"][mask].numpy():
        l[x] += 1
    print(l, l[0] / (mask.sum()))

    mask = g.ndata["test_mask"].to(bool)
    l = {0: 0, 1: 0}

    for x in g.ndata["label"][mask].numpy():
        l[x] += 1
    print(l, l[0] / (mask.sum()))

    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    batch_size = len(g.ndata["train_mask"])
    train_idx = torch.tensor(
        [i for i, x in enumerate(g.ndata["train_mask"]) if x > 0]
    ).to(device)
    val_idx = torch.tensor([i for i, x in enumerate(g.ndata["val_mask"]) if x > 0]).to(
        device
    )
    test_idx = torch.tensor(
        [i for i, x in enumerate(g.ndata["test_mask"]) if x > 0]
    ).to(device)

    g = g.to(device)
    sampler = dgl.dataloading.MultiLayerFullNeighborSampler(2)
    dataloader = DataLoader(g, train_idx, sampler, batch_size=batch_size)
    val_set = DataLoader(g, val_idx, sampler, batch_size=len(val_idx))
    test_set = DataLoader(g, test_idx, sampler, batch_size=len(test_idx))

    mlf_logger = MLFlowLogger()
    accel = "gpu" if torch.cuda.is_available() else "cpu"
    model = GCN(g, g.ndata["feature"].shape[1], 16, dataset.num_classes, g.etypes)
    trainer = pl.Trainer(
        max_epochs=5_000,
        accelerator=accel,
        log_every_n_steps=1,
        logger=mlf_logger,
    )
    trainer.fit(model, dataloader, val_dataloaders=val_set)
    trainer.test(model, dataloaders=test_set)

    features = {"review": g.ndata["feature"].to(device)}
    model = model.to(device)
    logits = model(g.to(device), features)["review"]
    test_mask = g.ndata["test_mask"].cpu().to(bool)
    labels = g.ndata["label"][test_mask].cpu()
    pred = logits.argmax(1)[test_mask].cpu()

    cm = confusion_matrix(labels, pred)
    cm = ConfusionMatrixDisplay(cm)
    cm.plot(cmap="Blues")
    plt.savefig("conf_mat.png")
