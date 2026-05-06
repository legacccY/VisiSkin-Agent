"""阶段二单元测试：退化模拟 + 标注逻辑 + Dataset 接口"""
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pytest

from data.auto_label import calc_brightness_score, calc_contrast_score, calc_sharpness, label_single
from data.dataset import SCORE_COLS, SkinPairedDataset
from data.degrade import degrade_image


def _make_image(h: int = 128, w: int = 128) -> np.ndarray:
    rng = np.random.default_rng(0)
    return rng.integers(0, 256, (h, w, 3), dtype=np.uint8)


# ── degrade.py ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("level", ["light", "medium", "heavy"])
def test_degrade_output_shape(level):
    img = _make_image()
    result = degrade_image(img, level, target_size=256)
    assert result.shape == (256, 256, 3), f"{level} 档退化输出形状错误：{result.shape}"


def test_degrade_heavy_differs_from_original():
    """重度退化后图片应与原始有明显差异"""
    img = _make_image(256, 256)
    result = degrade_image(img, "heavy", target_size=256)
    diff = np.abs(img.astype(float) - result.astype(float)).mean()
    assert diff > 1.0, f"重度退化差异过小：mean_diff={diff:.2f}"


# ── auto_label.py ────────────────────────────────────────────────────────────

def test_sharpness_returns_positive():
    gray = cv2.cvtColor(_make_image(), cv2.COLOR_BGR2GRAY)
    score = calc_sharpness(gray)
    assert score >= 0.0


def test_brightness_score_range():
    gray = cv2.cvtColor(_make_image(), cv2.COLOR_BGR2GRAY)
    score = calc_brightness_score(gray)
    assert 0.0 <= score <= 1.0


def test_contrast_score_range():
    gray = cv2.cvtColor(_make_image(), cv2.COLOR_BGR2GRAY)
    score = calc_contrast_score(gray)
    assert 0.0 <= score <= 1.0


def test_label_single_with_temp_file():
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        tmp = Path(f.name)
    img = _make_image(128, 128)
    cv2.imwrite(str(tmp), img)
    row = label_single(tmp)
    tmp.unlink()
    assert all(col in row for col in SCORE_COLS), f"缺少列：{set(SCORE_COLS) - set(row.keys())}"
    for col in SCORE_COLS:
        assert 0.0 <= row[col] <= 1.0, f"{col} 分数超出范围：{row[col]}"


# ── dataset.py ───────────────────────────────────────────────────────────────

def test_dataset_getitem():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        # 创建假图片
        img_path = tmpdir / "test.jpg"
        cv2.imwrite(str(img_path), _make_image(256, 256))

        # 创建假 CSV
        csv_path = tmpdir / "labels.csv"
        pd.DataFrame([{
            "image_path": str(img_path),
            "sharpness": 0.8,
            "brightness": 0.7,
            "completeness": 0.9,
            "color_temp": 0.6,
            "contrast": 0.5,
            "level": "light",
        }]).to_csv(csv_path, index=False)

        ds = SkinPairedDataset(csv_path, img_size=256)
        assert len(ds) == 1
        deg, orig, label = ds[0]
        assert deg.shape == (3, 256, 256)
        assert orig.shape == (3, 256, 256)
        assert label.shape == (5,)
