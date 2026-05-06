# VisiSkin-Agent

面向自拍皮肤照片的视觉质量引导与智能分诊 Agent。

**核心创新**：AI 先评估照片质量，质量不达标时引导重拍，再进行病灶分析。投稿目标：MICCAI 2027。

## 快速开始

```bash
# 激活环境
conda activate visiskin

# 安装依赖（首次）
pip install -e ".[dev,data]"

# 验证 GPU 环境
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"

# 运行测试
pytest tests/ -v
```

## 目录结构

```
project/
├── configs/          # YAML 配置（default.yaml 为全局模板）
├── tests/            # pytest 单元 + 冒烟测试
├── data/             # 数据处理脚本（阶段二）
├── models/           # 模型定义（阶段三）
├── agent/            # ReAct Agent 系统（阶段五）
├── benchmark/        # ITB 评测基准（阶段六）
└── pyproject.toml    # 依赖声明 + ruff + pytest 配置
```

## 实验运行

```bash
# 在 Claude Code 里，用 /loop 触发实验流水线（监控 + 自动修复）
/loop /run-experiment src/train_visiscore.py configs/default.yaml
```

## 硬件

RTX 4070 Laptop 8GB · CUDA 12.9 · Python 3.11
