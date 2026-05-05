# 阶段七：论文写作

## 目标

基于前六个阶段的实验结果，撰写 MICCAI 2027 格式的 8 页论文初稿，确保 LaTeX 可编译，图表完整，内容覆盖三大创新点。

---

## 前置条件

- 阶段六完成：ITB 实验数据、对比表格、可视化图表全部就绪
- 所有模型性能指标已确认
- MICCAI 2027 的 LaTeX 模板（.cls 文件）已下载

---

## 本阶段工具

| 工具 | 用途 |
|------|------|
| LaTeX + MiKTeX / TeX Live | 本地编译 MICCAI 格式论文 |
| MICCAI .cls 模板 | 官方格式模板，投稿必须使用 |
| Zotero | 文献管理，一键导出 BibTeX |
| draw.io | 绘制系统架构图（免费，导出 PDF 矢量图） |
| matplotlib | 结果对比图（由 analyze_results.py 直接生成，保持与数据一致） |
| Overleaf（可选） | 在线 LaTeX 编辑，适合多人协作修改 |

---

## 关键技术决策点

1. **论文标题**（选一个）：
   - *VisiSkin-Agent: Quality-Guided Visual Triage for Skin Lesion Analysis*
   - *Iterative Quality-Aware Triage: An Agent Framework for Dermatology Screening*
   - *Ask Before Diagnose: A Quality-Gated Agent for Skin Lesion Triage*

2. **作者顺序**：一作 / 通讯作者 / 合作者姓名和单位需要提前确认

3. **MICCAI .cls 模板**：需要提前下载官方模板，确认投稿系统接受的格式版本

---

## 交付物清单

| 文件 | 用途 |
|------|------|
| `paper/main.tex` | 完整论文正文（8 页 MICCAI 格式） |
| `paper/figures/arch.pdf` | 系统架构图（矢量图） |
| `paper/figures/examples.pdf` | 质量引导交互示例图 |
| `paper/figures/results.pdf` | 主要实验对比图 |
| `paper/references.bib` | 参考文献（BibTeX 格式） |

---

## 论文结构规划

| 章节 | 篇幅 | 核心内容 |
|------|------|---------|
| Abstract | ~250 词 | 问题/方法/三大创新/主要结果 |
| Introduction | ~1 页 | 动机 + 现有方法局限 + 我们的贡献 |
| Related Work | ~0.5 页 | IQA、皮肤病分析、Medical Agent |
| Method | ~2 页 | VisiScore-Net + QAD + Agent 系统架构 |
| Experiments | ~2 页 | ITB 基准 + 对比实验 + Ablation Study |
| Conclusion | ~0.3 页 | 总结 + 局限性 + 未来工作 |
| References | ~0.5 页 | 15-25 篇参考文献 |

---

## 工作步骤

1. **确认论文标题和作者**：与合作者对齐，确认贡献点表述
2. **撰写 Method 章节**：最先写，基于代码和实验设计，细节最清楚
3. **撰写 Experiments 章节**：直接引用 ITB 结果，填写表格和图表
4. **撰写 Introduction 和 Related Work**：基于前两章内容反过来写动机
5. **生成论文图表**：架构图用 draw.io 绘制导出 PDF，结果图由 `analyze_results.py` 直接生成 PDF
6. **整合 LaTeX + 编译验证**：确保无报错，页数符合要求，参考文献格式正确

---

## 验收标准

- `pdflatex main.tex` 编译无错误，生成 8 页 PDF
- 图表清晰，文字可读，无图文压缩失真
- 所有表格中的数字与 `itb_results.csv` 完全一致
- 参考文献格式符合 MICCAI 要求

---

## 硬件/资源约束

- 此阶段为写作工作，无 GPU 需求
- LaTeX 编译在本机即可完成

---

## 注意事项

- MICCAI 2027 投稿截止日期需要提前确认，预留 2-4 周审稿前缓冲时间
- 论文中的诊断术语使用要谨慎，不能夸大临床价值，强调"辅助工具"而非"诊断系统"
- Ablation Study 至少包含三组对比：① 无质量过滤 ② 有质量过滤但无 Agent 追问 ③ 完整系统
- 架构图是 MICCAI 审稿人第一眼关注的地方，投入足够时间设计清晰的系统图
- 如果某阶段实验结果不理想，在 Limitation 章节诚实说明，不要隐瞒
