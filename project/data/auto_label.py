"""弱监督质量标注：PSNR + SSIM + BRISQUE → 5 维归一化评分 → quality_labels.csv"""
import argparse
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import piq
import torch
from skimage.metrics import structural_similarity as calc_ssim
from tqdm import tqdm

# 5 维质量评分：清晰度 / 光照 / 完整度 / 色温 / 对比度
SCORE_COLS = ["sharpness", "brightness", "completeness", "color_temp", "contrast"]


def calc_sharpness(img_gray: np.ndarray) -> float:
    """拉普拉斯方差（越高越清晰）"""
    lap = cv2.Laplacian(img_gray, cv2.CV_64F)
    return float(lap.var())


def calc_brightness_score(img_gray: np.ndarray) -> float:
    """均值亮度归一化到 [0,1]，过暗/过亮都差"""
    mean = img_gray.mean() / 255.0
    return float(1.0 - abs(mean - 0.5) * 2)


def calc_completeness(img: np.ndarray, ref: np.ndarray) -> float:
    """SSIM（需要参考图，越高越完整）"""
    h, w = ref.shape[:2]
    img_resized = cv2.resize(img, (w, h))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    return float(calc_ssim(ref_gray, img_gray, data_range=255))


def calc_color_temp_score(img_bgr: np.ndarray) -> float:
    """R/B 通道比，偏色严重时分低"""
    b = img_bgr[:, :, 0].mean()
    r = img_bgr[:, :, 2].mean()
    ratio = r / (b + 1e-6)
    # 比值接近 1.0 为中性，偏差越大越差
    return float(1.0 - min(abs(ratio - 1.0) / 2.0, 1.0))


def calc_contrast_score(img_gray: np.ndarray) -> float:
    """直方图标准差，低对比度图像方差小"""
    std = img_gray.std()
    return float(min(std / 80.0, 1.0))  # 80 为经验饱和值


def calc_brisque_score(img_bgr: np.ndarray) -> float:
    """BRISQUE 无参考质量分数（0=最好，100=最差），转换为 [0,1] 高=好"""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    t = torch.from_numpy(img_rgb).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    try:
        score = piq.brisque(t, data_range=1.0).item()
        return float(max(0.0, 1.0 - score / 100.0))
    except Exception:
        return 0.5


def label_pair(degraded_path: Path, original_path: Path) -> dict:
    deg = cv2.imread(str(degraded_path))
    ref = cv2.imread(str(original_path))
    if deg is None or ref is None:
        return {}

    deg_gray = cv2.cvtColor(deg, cv2.COLOR_BGR2GRAY)
    h, w = ref.shape[:2]
    deg_resized = cv2.resize(deg, (w, h))

    raw_sharpness = calc_sharpness(cv2.cvtColor(deg_resized, cv2.COLOR_BGR2GRAY))
    sharpness = min(raw_sharpness / 1000.0, 1.0)  # 1000 为经验饱和值

    return {
        "degraded_path": str(degraded_path),
        "original_path": str(original_path),
        "sharpness": round(sharpness, 4),
        "brightness": round(calc_brightness_score(deg_gray), 4),
        "completeness": round(calc_completeness(deg, ref), 4),
        "color_temp": round(calc_color_temp_score(deg), 4),
        "contrast": round(calc_contrast_score(deg_gray), 4),
    }


def label_single(img_path: Path) -> dict:
    """无参考版本（原始图片自标注）"""
    img = cv2.imread(str(img_path))
    if img is None:
        return {}
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    raw_sharpness = calc_sharpness(img_gray)
    sharpness = min(raw_sharpness / 1000.0, 1.0)

    return {
        "image_path": str(img_path),
        "sharpness": round(sharpness, 4),
        "brightness": round(calc_brightness_score(img_gray), 4),
        "completeness": round(calc_brisque_score(img), 4),
        "color_temp": round(calc_color_temp_score(img), 4),
        "contrast": round(calc_contrast_score(img_gray), 4),
    }


def label_paired_dataset(paired_root: Path, original_root: Path, output_csv: Path) -> None:
    """对所有退化档位批量标注，写入 quality_labels.csv"""
    rows = []
    levels = ["light", "medium", "heavy"]

    for level in levels:
        level_dir = paired_root / level
        if not level_dir.exists():
            print(f"[WARN] {level_dir} 不存在，跳过")
            continue

        deg_paths = sorted(level_dir.glob("*.jpg")) + sorted(level_dir.glob("*.png"))
        for deg_path in tqdm(deg_paths, desc=f"标注 {level} 档"):
            orig_path = original_root / deg_path.name
            if orig_path.exists():
                row = label_pair(deg_path, orig_path)
            else:
                row = label_single(deg_path)
            if row:
                row["level"] = level
                rows.append(row)

    df = pd.DataFrame(rows)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"[INFO] 写入 {len(df)} 条记录到 {output_csv}")
    print(df[SCORE_COLS].describe().round(3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--paired", type=Path, default=Path("D:/YJ-Agent/data/paired_dataset"))
    parser.add_argument("--original", type=Path, default=Path("D:/YJ-Agent/data/raw/isic2020"))
    parser.add_argument("--output", type=Path, default=Path("D:/YJ-Agent/data/quality_labels.csv"))
    args = parser.parse_args()

    label_paired_dataset(args.paired, args.original, args.output)
