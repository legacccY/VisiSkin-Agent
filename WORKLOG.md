# 工作日志

## 当前状态

- **阶段**：阶段一（环境初始化）进行中
- **上次完成**：
  - 新建 conda 环境 `visiskin`（Python 3.11）
  - 创建项目目录骨架：`project/configs/`、`project/tests/`、`log/`
  - 写好 `configs/default.yaml`、`pyproject.toml`、`tests/test_smoke.py`、`README.md`
  - 非 torch 依赖安装中（wandb/ruff/pytest/omegaconf/tqdm/loguru）
  - PyTorch 2.6 + CUDA 12.4 安装中（新窗口下载）
- **下一步**：
  1. PyTorch 装完后补装 timm，运行 `pytest tests/ -v` 冒烟测试
  2. `wandb login`（需用户手动在终端执行）
  3. commit push 阶段一成果
- **待确认**：无

## 最后更新

2026-05-06 10:10（北京时间）
