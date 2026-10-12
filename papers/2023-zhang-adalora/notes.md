# AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 上传版本完整题名 | AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning |
| 上传版本作者，按原文顺序 | Qingru Zhang, Minshuo Chen, Alexander Bukharin, Nikos Karampatziakis, Pengcheng He, Yu Cheng, Weizhu Chen, Tuo Zhao（PDF p. 1） |
| 发表渠道、年份 | ICLR 2023；上传件页眉标注 Published as a conference paper at ICLR 2023 |
| 实际阅读版本 | arXiv:2303.10512v2，2023-12-20，17 页；有完整正文、参考文献、附录 |
| 正式会议记录的差异 | 作者官方代码仓库的会议 BibTeX 题名为 **Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning**，作者列表为七人，不含 Nikos Karampatziakis；保留此差异，不静默合并两版作者 |
| DOI | 会议 DOI：官方所核对记录未提供；arXiv DOI：[10.48550/arXiv.2303.10512](https://doi.org/10.48550/arXiv.2303.10512)，属于预印本记录 |
| 官方来源 | [上传版本的 arXiv 页](https://arxiv.org/abs/2303.10512v2)；[ICLR / OpenReview 记录](https://openreview.net/forum?id=lq62uWRJjiY)；[作者代码与会议引用](https://github.com/QingruZhang/AdaLoRA) |
| PDF | [官方 v2 全文](https://arxiv.org/pdf/2303.10512v2)；公开仓库未收录本地 `paper.pdf`，原因与上传件校验值见 [source.md](source.md) |
| 引用文件 | [citation.bib](citation.bib)，分别记录会议版与上传预印本版 |

本文所有页码均指**用户上传 PDF 的物理页码**，不是网页段落。下文“原文”指该版本的结论；“整理者归纳 / 推断 / 计算”不代表作者声明。元数据与来源核对日期：2026-10-11。

## 摘要

传统 LoRA 给不同层和模块分配相同秩，忽略了它们对下游任务贡献的差异。AdaLoRA 将可训练的权重增量写成类似 SVD 的三因子形式，通过敏感度与不确定性估计对奇异三元组打分，在总秩预算内动态保留重要方向，避免每一步显式计算大型矩阵的 SVD。它在 DeBERTaV3-base 的 GLUE、SQuAD 和 BART-large 的摘要生成实验中改善了参数效率；例如 SQuAD v2.0 的 0.08% 参数预算下 F1 为 88.7，LoRA 为 87.5，即提高 1.2 个百分点（原文 PDF pp. 3–8，表 2；百分点为整理者换算）。

## 背景、不足与贡献

- **问题依据（原文）**：固定 0.28M 可训练参数的实验表明，选择不同模块或层会得到不同 MNLI-m 准确率，FFN 和较高层较重要（p. 2，图 1）。这不是所有模型、所有任务的普遍定理。
- **现有方法不足（原文）**：均匀 LoRA 秩可能浪费预算；非结构化 diff pruning 需维护大增量矩阵并更新很多元素；反复对每个增量显式求 SVD 成本高（pp. 2–4）。
- **本文贡献（原文）**：可学习 SVD 形式、奇异三元组重要性评分、全局预算调度；只屏蔽奇异值而保留向量，使误删的方向有机会在后续重新激活（pp. 3–6）。

## 方法流程、模块与核心公式

1. 冻结预训练权重，初始化非零随机  $`P,Q`$  与零对角矩阵  $`\Lambda`$ 。
2. 用任务损失与正交正则更新三个因子。
3. 计算每个参数的敏感度、平滑敏感度和不确定性，再组合成三元组分数。
4. 每隔  $`\Delta T`$  步，在所有适配矩阵的三元组中全局保留预算允许的高分方向，屏蔽其他奇异值。
5. 初期保持较大预算，中期逐渐减小，末期固定秩分布继续训练（pp. 4–6，算法 1）。

权重参数化与正交正则（p. 4，式 (3)–(4)）：

$$
W=W^{(0)}+P\Lambda Q,
\qquad
R(P,Q)=\lVert P^\top P-I\rVert_F^2+\lVert QQ^\top-I\rVert_F^2.
$$

 $`W^{(0)}\in\mathbb R^{d_1\times d_2}`$  是冻结权重； $`P\in\mathbb R^{d_1\times r}`$ 、 $`Q\in\mathbb R^{r\times d_2}`$  是可训练方向； $`\Lambda`$  对角元素  $`\lambda_i`$  控制方向强度； $`r`$  是初始秩； $`I`$  为单位矩阵， $`\lVert\cdot\rVert_F`$  为 Frobenius 范数。训练目标为任务损失加  $`\gamma\sum_k R(P_k,Q_k)`$ 。这里是**模仿 SVD 的可学习参数化**，不是每步计算严格 SVD（p. 4）。

敏感度及其平滑、不确定性（p. 5，式 (8)–(11)）：

$$
I_t(w)=\lvert w\nabla_w\mathcal L\rvert,
\quad
\bar I_t(w)=\beta_1\bar I_{t-1}(w)+(1-\beta_1)I_t(w),
$$

$$
\bar U_t(w)=\beta_2\bar U_{t-1}(w)+(1-\beta_2)\lvert I_t(w)-\bar I_t(w)\rvert,
\qquad s_t(w)=\bar I_t(w)\bar U_t(w).
$$

第  $`k`$  个矩阵的第  $`i`$  个三元组分数（p. 5，式 (7)）：

$$
S_{k,i}=s(\lambda_{k,i})+
\frac1{d_1}\sum_{j=1}^{d_1}s(P_{k,ji})+
\frac1{d_2}\sum_{j=1}^{d_2}s(Q_{k,ij}).
$$

 $`\beta_1,\beta_2`$  是指数移动平均系数； $`b(t)`$  表示**全局保留奇异值数量 / 总秩**，不直接等于参数个数或 GPU 显存。式 (6) 对所有  $`S_{k,i}`$  做 Top- $`b(t)`$  选择；未选中的  $`\lambda_{k,i}`$  置零。不同形状矩阵每个秩的参数代价可能不同（后一说明为整理者推断）。

原文使用初始预算约为目标的 1.5 倍、warm-up / cubic decay / 固定预算三阶段（p. 6）。附录式 (12) 中间段分子写作  $`t-t_i-t_f`$ （p. 14），与阶段衔接的直观描述存在疑点；本笔记不静默修正该式。2026-10-11 核对作者 [RankAllocator 实现](https://github.com/QingruZhang/AdaLoRA/blob/main/loralib/loralib/adalora.py) 后，确认当前代码 `schedule_threshold` 的中段系数为  $`1-(t-t_i)/(T-t_i-t_f)`$ ；复现应锁定代码版本，保留 PDF 与当前代码的这个差异。

## 实验设置与主要定量结果

实验是离线 NLP 微调与评估，没有 LiDAR 采集或实测成像实验。

| 设置 | 原文信息 |
| --- | --- |
| 模型与任务 | DeBERTaV3-base：GLUE 开发集、SQuAD v1.1/v2.0；BART-large：XSum、CNN/DailyMail（pp. 6–8） |
| 对比方法 | Full fine-tuning、BitFit、Houlsby / Pfeiffer Adapter、推广到更多权重矩阵的 LoRA，而非只在 query/value 上应用的原始配置（pp. 6–7） |
| 指标 | GLUE：任务各自 Accuracy、Matthews correlation、F1、相关系数；QA：EM / F1；摘要：ROUGE-1/2/L（pp. 7–8） |
| 统计 | GLUE 表 1 是 5 个随机种子的均值；正文称实验增益通过  $`p<0.05`$  显著性检验，但未逐格给出检验方法与 p 值（pp. 6–7） |
| 计算环境 | PyTorch、Hugging Face Transformers，NVIDIA V100（p. 6） |

以下数字直接抄自相应表格，指标为原表使用的百分制分数：

| 数据集、指标、预算 | LoRA | AdaLoRA | 条件与出处 |
| --- | --- | --- | --- |
| GLUE All Ave.，约 0.3M 参数 | 88.15（0.33M） | 88.86（0.32M） | DeBERTaV3-base，开发集，表 1，p. 7；平均混合不同任务指标 |
| RTE Accuracy，同一预算组 | 85.56 | 87.36 | 表 1，p. 7；增加 1.80 个百分点，整理者计算 |
| GLUE All Ave.，约 1.2M 参数 | 88.34（1.33M） | 89.31（1.27M） | 表 1，p. 7；不是精确相同参数数目 |
| SQuAD v2.0 EM / F1，0.08% | 84.7 / 87.5 | 85.6 / 88.7 | 表 2，p. 8；比例相对于 full fine-tuning 参数量 |
| SQuAD v1.1 EM / F1，0.08% | 86.4 / 92.8 | 87.2 / 93.4 | 表 2，p. 8 |
| XSum R-1 / R-2 / R-L，1.10% | 43.40 / 20.20 / 35.20 | 44.35 / 21.13 / 36.13 | BART-large，表 3，p. 8 |
| CNN/DailyMail R-1 / R-2 / R-L，0.13% | 43.68 / 20.63 / 40.71 | 43.94 / 20.83 / 40.96 | 表 3，p. 8 |

训练成本：MNLI、0.08% 预算、单 V100 时，LoRA / AdaLoRA 分别为 105 / 116 min per epoch、11.094 / 11.104 GB GPU memory（p. 17，表 15）。这体现额外训练成本，不等于节省同等比例的计算量。

## 消融、适用条件与局限性

- **参数化消融（原文）**：0.08% 预算下，CoLA 的 Prune LoRA / AdaLoRA 为 66.71 / 70.21；屏蔽奇异值优于将 LoRA 双因子对应组全部置零（p. 9，表 4）。
- **重要性消融（原文）**：同一 CoLA 设置，敏感度单项 66.71、单纯奇异值幅度 67.67、完整 AdaLoRA 70.21；不意味着完整评分在每个单元格都严格最佳（p. 9，表 4）。
- **模块消融（原文）**：仅 SVD 形式、仅正交约束、无正交约束的 AdaLoRA 均不能整体复现完整方法的优势（p. 10，表 5）。
- **适用条件（整理者归纳）**：需要可微任务损失与梯度重要性估计，适用于对冻结 Transformer 权重进行任务微调并控制适配器预算。
- **局限性（整理者推断）**：评分、初始秩、调度和正交正则增加超参数及训练开销；保留被屏蔽方向的训练状态意味着最终有效参数量不能直接代表训练时内存；原文未验证联邦通信、DP 保证或任意更大 LLM 的普遍收益。
- **作者后续工作**：结论节未给出明确的具体后续研究路线（p. 10）；本笔记不补造。

## 复现资料与待核实项

官方代码：[QingruZhang/AdaLoRA](https://github.com/QingruZhang/AdaLoRA)，PDF p. 1 明确给出。数据集是 GLUE、SQuAD v1.1/v2.0、XSum 和 CNN/DailyMail；统计及配置位于附录 B–E（pp. 14–16）。原文未提供本次实验全部 checkpoint / 环境锁文件的下载链接。

可按 SQuAD v2.0 低预算配置起步： $`b(T)=72`$ 、最终平均秩 1、初始秩 2，batch size 16，AdamW，learning rate  $`10^{-3}`$ ，12 epochs， $`\gamma=0.1`$ ， $`t_i=5000`$ 、 $`\Delta T=100`$ 、 $`t_f=50000`$ （pp. 8、15，表 9–10）。实现前应核对步数定义，保存采样种子、数据版本与代码 commit。

上传件存在下列不一致，不能当作已解决：p. 9 叙述将 XSum 1.10% 的 LoRA R-2 写为 19.89，而表 3 同档为 20.20；p. 8 说摘要训练 15 epochs，p. 16 表 13 的 XSum 为 25；p. 16 表 12 的预算档与主文摘要表 3 不同；p. 16 训练成本文字写 SQuADv2，p. 17 表 15 行标签写 SST-2。本笔记分别保留表格出处，不将这些值拼成一个配置。

## 阅读总结

**原文解决的问题**：在有限适配器参数预算下，按任务重要性分配不同层 / 模块的低秩容量，而非均匀分配。

**值得借鉴（整理者归纳）**：把“学习方向”和“选择方向”分开，保留可恢复的方向；以全局预算和任务敏感度控制资源分配。将它迁移到 federated LoRA 时，还需额外处理不同客户端的方向对齐、聚合、隐私预算及实际传输代价；这些是推断出的研究问题，本文没有验证。

## 与 ISER 的阅读联系

[ISER](../2026-park-iser/notes.md) 在图像 codec 的每实例 TTFT 中借用重要性 / 全局秩预算，限制在 decoder SV，并用时间二阶差调节剪枝和停止（ISER pp.11–14）。本篇 pp.4–6 的 AdaLoRA 在训练中动态更新评分与预算，不是 ISER p.11 所宽泛概括的“开始时一次分配”。可比较 task-level 与 instance-level、调度和适配范围；本文 LLM 参数预算与 ISER 图像 bpp / SV overhead 不同。未验证两法在相同 TTFT / 联邦条件的组合或排名。

## 单光子 LiDAR 参数

不适用。本文不涉及探测器类型、阵列规模、探测距离、目标速度、SNR/SBR、每像素光子数、采集时间、重建帧率、空间分辨率或定位误差；NLP 模型训练 / 评估时间不等于成像采集或实时重建时间。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [版本与版权](source.md)
