"""下载 ISIC 2020 数据集（需要 ~/.kaggle/kaggle.json）"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

# 实际使用：256x256 预缩放版本，624MB，33126 张
# 原始路径：train-image/image/*.jpg
ISIC2020_DATASET = "nischaydnk/isic-2020-jpg-256x256-resized"


def check_kaggle_token() -> bool:
    token_path = Path.home() / ".kaggle" / "kaggle.json"
    if not token_path.exists():
        print(f"[ERROR] Kaggle token 未找到：{token_path}")
        print("请前往 https://kaggle.com → Settings → API → Create New Token")
        print(f"将下载的 kaggle.json 放到 {token_path}")
        return False
    # kaggle 要求权限 600
    if sys.platform != "win32":
        os.chmod(token_path, 0o600)
    return True


def download_isic2020(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    kaggle_exe = Path(sys.executable).parent / "Scripts" / "kaggle.exe"
    if not kaggle_exe.exists():
        kaggle_exe = "kaggle"

    print(f"[INFO] 下载 ISIC 2020 到 {output_dir} ...")
    cmd = [
        str(kaggle_exe),
        "datasets",
        "download",
        ISIC2020_DATASET,
        "--path",
        str(output_dir),
        "--unzip",
    ]
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"[ERROR] 下载失败，退出码 {result.returncode}")
        sys.exit(1)
    print("[INFO] 下载完成")


def main() -> None:
    parser = argparse.ArgumentParser(description="下载皮肤病数据集")
    parser.add_argument(
        "--dataset",
        choices=["isic2020"],
        default="isic2020",
        help="要下载的数据集",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("D:/YJ-Agent/data/raw/isic2020"),
        help="输出目录",
    )
    args = parser.parse_args()

    if not check_kaggle_token():
        sys.exit(1)

    if args.dataset == "isic2020":
        download_isic2020(args.output)


if __name__ == "__main__":
    main()
