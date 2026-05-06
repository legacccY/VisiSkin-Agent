"""阶段二验收：退化 → 标注 → DataLoader 一键验证"""
import sys
from pathlib import Path

PAIRED_ROOT = Path("D:/YJ-Agent/data/paired_dataset")
ORIGINAL_ROOT = Path("D:/YJ-Agent/data/raw/isic2020/train-image/image")
LABELS_CSV = Path("D:/YJ-Agent/data/quality_labels.csv")


def check_paired_dataset() -> bool:
    print("\n[1/3] 检查配对数据集...")
    ok = True
    for level in ["light", "medium", "heavy"]:
        level_dir = PAIRED_ROOT / level
        count = len(list(level_dir.glob("*.jpg"))) if level_dir.exists() else 0
        status = "OK" if count > 0 else "FAIL"
        print(f"  [{status}] {level}: {count} zhang")
        if count == 0:
            ok = False
    return ok


def run_auto_label() -> bool:
    print("\n[2/3] shengcheng zhiliangbiaoqian...")
    import subprocess
    result = subprocess.run(
        [
            sys.executable,
            "data/auto_label.py",
            "--paired", str(PAIRED_ROOT),
            "--original", str(ORIGINAL_ROOT),
            "--output", str(LABELS_CSV),
        ],
        check=False,
    )
    if result.returncode != 0:
        print("  [FAIL] auto_label.py shibai")
        return False
    print(f"  [OK] xierufin {LABELS_CSV}")
    return True


def check_dataloader() -> bool:
    print("\n[3/3] yanzheng DataLoader...")
    from data.dataset import build_dataloader

    loader = build_dataloader(LABELS_CSV, batch_size=8, num_workers=0, shuffle=False)
    degraded, original, label = next(iter(loader))

    shape_ok = (
        degraded.shape == (8, 3, 256, 256)
        and original.shape == (8, 3, 256, 256)
        and label.shape == (8, 5)
    )
    print(f"  degraded:  {tuple(degraded.shape)}")
    print(f"  original:  {tuple(original.shape)}")
    print(f"  label:     {tuple(label.shape)}")
    print(f"  label range: min={label.min():.3f}  max={label.max():.3f}")

    if shape_ok and 0.0 <= label.min() and label.max() <= 1.0:
        print("  [OK] DataLoader pass")
        return True
    else:
        print("  [FAIL] shape or value range error")
        return False


if __name__ == "__main__":
    import os
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))

    results = []
    results.append(check_paired_dataset())

    if results[0]:
        results.append(run_auto_label())
    else:
        print("\npaired dataset incomplete, run degrade.py first")
        sys.exit(1)

    if results[1]:
        results.append(check_dataloader())

    print("\n" + ("=" * 40))
    if all(results):
        print("Phase 2 PASSED")
    else:
        print("FAILED - check errors above")
        sys.exit(1)
