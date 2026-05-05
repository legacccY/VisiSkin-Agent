# 阶段二：数据流水线

## 目标

下载全部公开皮肤图像数据集，构建"低质量 → 高质量"配对数据集，并生成用于训练 VisiScore-Net 的弱监督质量标签。

---

## 前置条件

- 阶段一完成：Python 环境就绪，目录结构已建立
- Kaggle 账号 + API Token（用于下载 ISIC 数据集）
- 磁盘剩余 ≥ 150GB（原始数据 ~100GB + 处理后数据）

---

## 本阶段工具

| 工具 | 用途 |
|------|------|
| kaggle CLI | 下载 ISIC 2020 / 2024 数据集 |
| Pillow / opencv-python | 图像读写和基础操作 |
| albumentations | 图像退化模拟（模糊/低光/色偏/裁切/JPEG 压缩） |
| scikit-image | 计算 PSNR / SSIM（有参考质量指标） |
| piq | 计算 BRISQUE（无参考质量指标） |
| pandas | 管理 quality_labels.csv |
| tqdm | 批量处理进度条 |

---

## 关键技术决策点

1. **ISIC 年份选择**：只用 2020（33k 张）/ 只用 2024（400k 张）/ 两者都要。影响训练数据规模和磁盘占用
2. **降质档位设计**：3 档（轻/中/重）/ 5 档 / 连续值。影响配对数据多样性和训练难度
3. **弱标注策略**：纯算法标注（PSNR/SSIM/BRISQUE）/ 算法 + 少量人工标注（500 张）。影响标签质量

---

## 交付物清单

| 文件 | 用途 |
|------|------|
| `data/download.py` | Kaggle API 下载 ISIC + DermNet 爬虫 |
| `data/degrade.py` | 图像退化模拟（高斯模糊/低光/裁切/色偏/JPEG 压缩） |
| `data/dataset.py` | PyTorch Dataset/DataLoader，加载配对数据 |
| `data/auto_label.py` | 弱监督质量标注，输出 5 维评分 |
| `data/paired_dataset/` | 生成的配对数据集（原始 + 退化版本） |
| `data/quality_labels.csv` | 每张图的 5 维质量评分（清晰度/光照/完整度/色温/对比度） |

---

## 工作步骤

1. **配置 Kaggle API**：验证 API Token，测试下载小文件
2. **下载数据集**：按确认的年份下载 ISIC，下载 DermNet 和 FitzPatrick17k
3. **图像退化模拟**：为每张原始图生成对应退化版本（配对）
4. **弱监督标注**：用 PSNR/SSIM/BRISQUE 等算法为所有图片生成初始质量评分
5. **DataLoader 验证**：确认配对加载正常，批次数据形状符合预期

---

## 验收标准

- DataLoader 可正常迭代，`next(iter(dataloader))` 返回 `(degraded_img, original_img, quality_label)` 形状正确
- `quality_labels.csv` 存在，包含 5 列评分，数值分布合理（非全为极值）
- 至少完成一个降质类型的配对数据生成

---

## 硬件/资源约束

- 下载阶段无 GPU 需求，主要是网络和磁盘 I/O
- 退化模拟为 CPU 操作，可并行处理
- 磁盘使用预估：ISIC 2024 原始 ~80GB，退化版本另需 ~80GB（可考虑动态生成减少磁盘占用）

---

## 注意事项

- ISIC 2024 体积极大，下载前确认磁盘空间，考虑先下载 2020 版本验证流程
- 退化模拟参数（模糊程度、光照范围）需要记录到 `configs/default.yaml`，保证可复现
- DermNet 爬虫需遵守 robots.txt 规则，控制爬取速度
- 弱标注的 BRISQUE 分数是无参考质量指标，可能与人类主观判断有偏差，后续可能需少量人工校正
- 为 `data/degrade.py` 和 `data/auto_label.py` 写 pytest 单元测试（数据处理层最容易出静默 bug）
