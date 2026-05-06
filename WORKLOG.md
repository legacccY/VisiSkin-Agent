# 工作日志

## 当前状态

- **阶段**：阶段一完成，准备进入阶段二
- **上次完成**：
  - 新建 conda 环境 `visiskin`（Python 3.11 + PyTorch 2.5.1 + CUDA 12.4）
  - 建立项目骨架：`project/configs/default.yaml`、`pyproject.toml`、`tests/test_smoke.py`、`README.md`
  - ruff check 通过，pytest 6/6 冒烟测试全过，推送到 GitHub
- **下一步**：开始阶段二——数据流水线（下载 ISIC/DermNet/FitzPatrick17k，生成配对数据集）
- **待确认**：`wandb login` 尚未执行，阶段三训练前需要手动跑一次

## 最后更新

2026-05-06 11:00（北京时间）
