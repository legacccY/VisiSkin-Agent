"""PyTorch Dataset：加载配对数据，返回 (degraded, original, quality_label)"""
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

SCORE_COLS = ["sharpness", "brightness", "completeness", "color_temp", "contrast"]

_DEFAULT_TRANSFORM = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


class SkinPairedDataset(Dataset):
    def __init__(
        self,
        csv_path: str | Path,
        img_size: int = 256,
        transform=None,
        levels: list[str] | None = None,
    ):
        self.df = pd.read_csv(csv_path)
        if levels:
            self.df = self.df[self.df["level"].isin(levels)].reset_index(drop=True)
        self.img_size = img_size
        self.transform = transform or _DEFAULT_TRANSFORM

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        row = self.df.iloc[idx]

        deg_key = "degraded_path" if "degraded_path" in row else "image_path"
        degraded = self._load(row[deg_key])

        if "original_path" in row and pd.notna(row["original_path"]):
            original = self._load(row["original_path"])
        else:
            original = degraded.clone()

        label = torch.tensor(row[SCORE_COLS].values.astype(np.float32))
        return degraded, original, label

    def _load(self, path: str) -> torch.Tensor:
        img = cv2.imread(path)
        if img is None:
            img = np.zeros((self.img_size, self.img_size, 3), dtype=np.uint8)
        img = cv2.resize(img, (self.img_size, self.img_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self.transform(img)


def build_dataloader(
    csv_path: str | Path,
    batch_size: int = 32,
    num_workers: int = 4,
    img_size: int = 256,
    levels: list[str] | None = None,
    shuffle: bool = True,
) -> DataLoader:
    ds = SkinPairedDataset(csv_path, img_size=img_size, levels=levels)
    return DataLoader(
        ds,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True,
    )
