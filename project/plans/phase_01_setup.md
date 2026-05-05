# 阶段一：项目环境初始化

## 目标

搭建可运行的 Python 项目骨架，确保 CUDA + PyTorch 环境就绪，建立标准化的目录结构和配置体系。

---

## 前置条件

- NVIDIA 驱动已安装（RTX 4070）
- Git 已配置
- 无需上一阶段输出

---

## 关键技术决策点

在开始前需要与用户确认：

1. **Python 环境管理工具**：conda / uv / venv（影响后续所有依赖安装方式）
2. **项目根目录路径**：代码放在哪里（如 `D:\VisiSkin-Agent\`）
3. **CUDA 版本**：当前安装的 CUDA 是哪个版本（影响 PyTorch 安装命令）

---

## 本阶段工具

| 工具 | 用途 | 安装 |
|------|------|------|
| PyTorch 2.x | 深度学习主框架 | 官网按 CUDA 版本选命令 |
| timm | Backbone 模型库 | `pip install timm` |
| wandb | 实验追踪 | `pip install wandb` → `wandb login` |
| ruff | 代码 lint + 格式化 | `pip install ruff` |
| pytest | 单元测试 | `pip install pytest` |
| OmegaConf | YAML 配置加载 | `pip install omegaconf` |
| tqdm | 进度条 | `pip install tqdm` |
| loguru | 日志 | `pip install loguru` |

---

## 交付物清单

```
<项目根目录>/
├── data/               # 数据相关脚本（后续阶段填充）
├── models/             # 模型定义（后续阶段填充）
├── agent/              # Agent 系统（后续阶段填充）
├── benchmark/          # 评测基准（后续阶段填充）
├── paper/              # 论文文件（后续阶段填充）
├── tests/              # pytest 单元测试
├── configs/
│   └── default.yaml    # 全局配置模板（路径/超参/设备）
├── pyproject.toml      # 依赖声明 + ruff 配置
└── README.md           # 项目简介 + 快速开始
```

- `configs/default.yaml`：数据路径、训练超参默认值、设备配置、wandb 项目名
- `pyproject.toml`：依赖清单 + ruff 规则（行宽 120）+ pytest 配置

---

## 工作步骤

1. **确认环境**：验证 CUDA 版本、Python 版本、可用磁盘空间
2. **创建项目结构**：建立上述目录骨架，初始化 git 仓库，连接 GitHub remote
3. **安装依赖**：根据确认的 CUDA 版本安装对应 PyTorch，再安装其他依赖，生成 `pyproject.toml`
4. **配置代码风格**：在 `pyproject.toml` 写入 ruff 规则，确认 `ruff check .` 和 `ruff format .` 可用
5. **配置 wandb**：`wandb login`，在 `configs/default.yaml` 写入项目名
6. **验证环境**：运行验证脚本确认 GPU 可用，写第一个 pytest 冒烟测试

---

## 验收标准

- `python -c "import torch; print(torch.cuda.is_available())"` 输出 `True`
- `python -c "import torch; print(torch.cuda.get_device_name(0))"` 显示 RTX 4070
- `ruff check .` 无报错，`pytest tests/ -v` 通过冒烟测试
- `wandb login` 已完成，`import wandb; wandb.init(project="visiskin")` 不报错
- GitHub 仓库已建，`git push origin main` 成功

---

## 硬件/资源约束

- 此阶段不涉及训练，无显存压力
- 确认磁盘剩余 ≥ 150GB（为后续数据阶段预留）

---

## 注意事项

- PyTorch 版本与 CUDA 版本必须严格对应，安装前先查官网兼容表
- 不要把数据集路径硬编码进脚本，统一放在 `configs/default.yaml`
- ruff 的行宽设为 120（研究代码行较长），在 `pyproject.toml` 的 `[tool.ruff]` 中配置 `line-length = 120`
- 第一次 `git push` 之前先确认 `.gitignore` 已排除 `data/`、`checkpoints/`、`.env`、`wandb/`（体积大或含密钥）
