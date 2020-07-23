import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel
import pytorch_lightning as pl


class CoolDataset(Dataset):

    def __len__(self):
        return 128 * 128

    def __getitem__(self, idx):
        return torch.tensor([1, 2, 3, 4] * 128 * 8), torch.tensor([1, 1, 1, 1] * 128 * 8)


class CoolSystem(pl.LightningModule):

    def __init__(self):
        super().__init__()

        self.model = AutoModel.from_pretrained('allenai/longformer-base-4096')
        # self.model = AutoModel.from_pretrained('roberta-base')

    def forward(self, x, y):
        return self.model(x, attention_mask=None)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x, y)
        loss = y_hat[0].sum()
        return {'loss': loss}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

    def train_dataloader(self):
        loader = DataLoader(CoolDataset(), batch_size=1, num_workers=0)
        return loader


if __name__ == '__main__':
    model = CoolSystem()
    trainer = pl.Trainer(progress_bar_refresh_rate=1, max_epochs=10, num_sanity_val_steps=0, gpus=0, num_tpu_cores=1)
    trainer.fit(model)
