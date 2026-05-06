"""可视化：退化对比图 + 质量分布图"""
import argparse
import random
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

ORIGINAL_ROOT = Path("D:/YJ-Agent/data/raw/isic2020/train-image/image")
PAIRED_ROOT = Path("D:/YJ-Agent/data/paired_dataset")
LABELS_CSV = Path("D:/YJ-Agent/data/quality_labels.csv")
OUTPUT_DIR = Path("D:/YJ-Agent/data/viz")
SCORE_COLS = ["sharpness", "brightness", "completeness", "color_temp", "contrast"]


def plot_degradation_grid(n_samples: int = 6, seed: int = 42, save: bool = True) -> None:
    """原图 vs light / medium / heavy 对比网格"""
    random.seed(seed)
    orig_paths = sorted(ORIGINAL_ROOT.glob("*.jpg"))
    samples = random.sample(orig_paths, min(n_samples, len(orig_paths)))

    fig, axes = plt.subplots(n_samples, 4, figsize=(14, n_samples * 3.2))
    fig.suptitle("ISIC 2020 Degradation Levels", fontsize=14, y=1.01)

    col_titles = ["Original", "Light", "Medium", "Heavy"]
    for ax, title in zip(axes[0], col_titles):
        ax.set_title(title, fontsize=11, fontweight="bold")

    for row, orig_path in enumerate(samples):
        imgs = [cv2.cvtColor(cv2.imread(str(orig_path)), cv2.COLOR_BGR2RGB)]
        for level in ["light", "medium", "heavy"]:
            p = PAIRED_ROOT / level / orig_path.name
            img = cv2.imread(str(p))
            imgs.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if img is not None else np.zeros((256, 256, 3), dtype=np.uint8))

        for col, img in enumerate(imgs):
            axes[row, col].imshow(img)
            axes[row, col].axis("off")
        axes[row, 0].set_ylabel(orig_path.stem[:12], fontsize=8, rotation=0, labelpad=60, va="center")

    plt.tight_layout()
    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUTPUT_DIR / "degradation_grid.png"
        plt.savefig(out, dpi=120, bbox_inches="tight")
        print(f"[OK] saved: {out}")
    plt.show()


def plot_label_distributions(save: bool = True) -> None:
    """5 维质量评分分布（按退化档位分色）"""
    import pandas as pd

    if not LABELS_CSV.exists():
        print(f"[WARN] {LABELS_CSV} 不存在，跳过标注分布图")
        return

    df = pd.read_csv(LABELS_CSV)
    colors = {"light": "#2ecc71", "medium": "#f39c12", "heavy": "#e74c3c"}

    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    fig.suptitle("Quality Score Distributions by Degradation Level", fontsize=13)

    for ax, col in zip(axes, SCORE_COLS):
        for level, color in colors.items():
            sub = df[df["level"] == level][col].dropna()
            ax.hist(sub, bins=40, alpha=0.5, color=color, label=level, density=True)
        ax.set_title(col, fontsize=10)
        ax.set_xlabel("score")
        ax.set_xlim(0, 1)
        if col == SCORE_COLS[0]:
            ax.legend(fontsize=8)

    plt.tight_layout()
    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUTPUT_DIR / "label_distributions.png"
        plt.savefig(out, dpi=120, bbox_inches="tight")
        print(f"[OK] saved: {out}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["degrade", "labels", "all"], default="all")
    parser.add_argument("--n", type=int, default=6)
    args = parser.parse_args()

    if args.mode in ("degrade", "all"):
        plot_degradation_grid(n_samples=args.n)
    if args.mode in ("labels", "all"):
        plot_label_distributions()
