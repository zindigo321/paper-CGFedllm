# CG-FedLLM: How to Compress Gradients in Federated Fune-tuning for Large Language Models

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 上传版题名 | CG-FedLLM: How to Compress Gradients in Federated **Fune-tuning** for Large Language Models；首页另标 **Extended Version**。保留原文拼写，不将其静默改成正式版题名 |
| 作者，按上传版顺序 | Huiwen Wu, Xiaogang Xu, Deyi Zhang, Xiaohan Li, Jiafei Wu, Zhe Liu（PDF p. 1；arXiv v3 与出版社提交的 Crossref 记录同序） |
| 实际阅读版本 | arXiv:2405.13746v3；提交日期 2025-11-17，PDF 日期 2025-11-18；27 页，含正文、参考文献、附录 A–E 和末尾图页；初版发表于 arXiv 的 2024 年不作为本目录年份 |
| 正式出版记录 | **CG-FedLLM: How to Compress Gradients in Federated Fine-Tuning for Large Language Models**，ECAI 2025，第 28 届；Frontiers in Artificial Intelligence and Applications。卷 413、pp. 4257–4264 由 IOS 出版页核实，并与第一作者主页页码及上传版 p. 13 参考文献 [55] 对照 |
| 日期与页面差异 | Crossref 的 published / published-print 为 2025-10-21，IOS 页 citation_online_date 和第一作者主页为 2025-10-22；当前 SAGE 页面列在线日期 2026-08-25，仍归入 ECAI 2025，页面标题显示 `CG-FedLL How...`。分别记录，不据此改写会议年。PDF p. 1 脚注写第 26 届，与正式渠道的第 28 届不同 |
| 正式 / 预印本 DOI | [ECAI: 10.3233/FAIA251320](https://doi.org/10.3233/FAIA251320)；[arXiv: 10.48550/arXiv.2405.13746](https://doi.org/10.48550/arXiv.2405.13746)，两者用途分开 |
| 官方来源 | [arXiv v3](https://arxiv.org/abs/2405.13746v3)；[出版社提交的 Crossref 元数据](https://api.crossref.org/works/10.3233/FAIA251320)；[IOS 出版页](https://ebooks.iospress.nl/DOI/10.3233/FAIA251320)；[第一作者论文页](https://shi.buaa.edu.cn/wuhuiwen/en/lwcg/231598/content/34102.htm)；[当前出版社页面](https://journals.sagepub.com/doi/full/10.3233/FAIA251320) |
| PDF、引用、许可 | [原始上传 PDF](paper.pdf)；[官方 v3 PDF](https://arxiv.org/pdf/2405.13746v3)；[citation.bib](citation.bib)；[source.md](source.md)。上传版为 **CC BY-NC-SA 4.0**，正式版 Crossref / 出版页为 CC BY-NC 4.0，不能互换 |

**范围声明**：页码均为实际上传 PDF 的物理页码；分析与数值依据 v3 扩展版。正式出版元数据和网页入口已核对，正式 PDF 未取得，也未逐段审读正式版 HTML，不宣称完成两版内容对照。目录固定为 `2025-wu-cg-fedllm`。核对日期：2026-10-12。

## 摘要

CG-FedLLM 在联邦 LoRA 微调中，用客户端 encoder 压缩低秩因子，服务端 decoder 重建后更新模型。TGAP（Temporal-ensemble Gradient-Aware Pre-training）先收集目标模型不同时间步的真实梯度 / LoRA 因子并训练 AutoEncoder；FAF（Federated AutoEncoder Fine-tuning）再使用预训练压缩器参与联邦微调，不同时训练压缩器。二维 ResNet / Uformer 的编码元素保留比例报告为 1.56%，Qwen-7B / MMLU 在作者报告的 GDP 预算  $`\epsilon=0.25`$  下得分 56.37，带噪 LoRA 为 25.22（pp. 4–10，表 1–2）。这些是特定模拟和离线评估结果；真实梯度预训练的隐私、完整 DP 配置、通信成本边界和若干正文 / 附录冲突仍需核实。

## 背景、已有方法不足与贡献

- **背景（原文）**：FL 不集中交换原始训练数据，但大量 LLM 参数使梯度 / 更新传输昂贵；LoRA 减少可训练参数后仍有较高通信负担（pp. 1–2）。FL 本身不等同于已经获得差分隐私保证。
- **已有方法不足（原文）**：固定量化可能丢失信息；一维学习压缩器不易适配 LLM 的大规模因子；随目标模型同时训练压缩器增加计算成本，且动态梯度数据让拟合困难（pp. 2–4）。
- **贡献（原文）**：构造跨时间梯度训练集并先训练 AutoEncoder；在 FAF 中压缩和重建低秩因子；比较通信表示大小、计算开销、C-Eval / MMLU 效用、噪声、架构和跨数据集泛化（pp. 2–10）。
- **扩展版范围（原文）**：p. 3 称相对于先前 ECAI 工作增加多模型 / 数据集实验、评价指标和消融。没有取得并完整审读会议版，故不逐项断言某张表一定只存在于扩展版。

## 两阶段方法、模块与核心公式

### TGAP：先收集时间序列，再训练压缩器

先用数据集  $`D_1`$  对目标模型进行训练，收集客户端  $`i`$ 、时间步  $`t`$  的低秩梯度信息  $`G_i^t`$ ，组成固定训练集；另用  $`D_2`$  做后续 FAF。作者认为跨时间和客户端的梯度分布具有可利用的相似性，用预训练避开动态联合训练的拟合问题（pp. 2、4；p. 10）。这是实验支持的设计假设，不是任意模型 / 数据分布上的分布恒等定理。

原文压缩与重建（p. 4，式 (1)–(2)）、损失（p. 5，式 (3)）：

$$
F_i=\operatorname{Enc}(G_i),\qquad
\widetilde G_i=\operatorname{Dec}(F_i),\qquad
\mathcal L_{\mathrm{recons}}=\lVert G-\widetilde G\rVert_2^2.
$$

AutoEncoder 为 1D-CNN、二维 ResNet 或 Uformer 结构；Adam 学习率为  $`2\times10^{-4}`$  （pp. 5、14–16，表 5–7）。正文损失写平方范数，附录称 MSE，是否平均、按何种张量 / 样本归一化未完全说明。FAF 使用预训练后的 encoder / decoder，原文不要求继续优化压缩器参数（pp. 2、5–6）。

LLaMA-7B 的 32 个 Transformer blocks，每块 Q/K/V/O 各有两个 rank-8 因子；附录 D.1 给出  $`A\in\mathbb R^{8\times4096}`$ 、 $`B\in\mathbb R^{4096\times8}`$  ，原文写  $`G=BA`$  （p. 19）。每轮 LoRA 因子元素数为（p. 5）：

$$
4096\times8\times2\times4\times32=8{,}388{,}608.
$$

附录 B.2（p. 14）写拼接  $`A^\top,B`$  后构成  $`2048\times4096`$  输入，但该处对转置方向的叙述与上述维度不完全一致；p. 19 的尺寸下，形成该布局应核对具体转置 / 展平方式。文中将这些对象称为 gradients，同时描述为 LoRA 本地训练得到的矩阵；未充分说明它们究竟是因子权重、参数增量还是因子梯度，复现不能自动将其等同于完整权重的直接梯度。

### FAF：客户端编码，服务端逐客户端解码后聚合

算法 1（p. 5）和第 3.3 节（p. 6）的顺序为：抽样客户端并下发全局模型 → 本地 LoRA 训练 → 编码  $`[A_i,B_i]`$  → 上传压缩表示 → 服务端分别解码 → 分别聚合两类因子 → 更新模型并下发。基本版不是先在 latent space 平均，再只解码一次。

按原算法保留其求和与更新符号：

$$
[\bar A_i,\bar B_i]=\operatorname{Enc}([A_i,B_i]),\qquad
[\widetilde A_i,\widetilde B_i]=\operatorname{Dec}([\bar A_i,\bar B_i]),
$$

$$
\widetilde A=\sum_i\widetilde A_i,\quad
\widetilde B=\sum_i\widetilde B_i,\quad
W_{\mathrm{global}}^{t+1}=W_{\mathrm{global}}^t+eta\widetilde B\widetilde A.
$$

 $`\eta`$  为步长，参与集合为  $`I_t`$ 。原算法没有明确给出按客户端数据量加权、平均系数或 LoRA scaling 的完整处理；不能自行替换成另一种 FedAvg / 聚合实现后仍称其为原文算法。两个因子分别求和再相乘通常含交叉客户端项，与 [FFA-LoRA](../2024-sun-ffa-lora/notes.md) 讨论的聚合不匹配有关，详见下文。

## 压缩、重建与计算成本

CR 的分母是输入张量元素数、分子是 encoder 输出元素数（p. 5），**越小代表保留越少**。表 1（p. 4）报告值与按形状重新计算如下，重新计算均为整理者计算：

| AutoEncoder | 原表输入 / 输出形状 | 输入 / 输出元素数 | 原文 CR | 形状计算的保留比例 | 原文误差平方量 / SNR |
| --- | --- | --- | --- | --- | --- |
| 1D-CNN | `[128,1,32768]` / `[128,4,256]` | 4,194,304 / 131,072 | 3.21% | **3.125%**，与报告值不同 |  $`8.94\times10^{-4}`$  /  $`1.60\times10^4`$  |
| ResNet | `[1,4096,2048]` / `[64,64,32]` | 8,388,608 / 131,072 | 1.56% | 1.5625% |  $`5.06\times10^{-12}`$  /  $`2.82\times10^{12}`$  |
| Uformer | `[8,1024,1024]` / `[1,256,512]` | 8,388,608 / 131,072 | 1.56% | 1.5625% |  $`1.04\times10^{-11}`$  /  $`1.37\times10^{12}`$  |

表 1 各列均列信号平方量 14.29；SNR 按其信号量除以误差量，属于**线性比值，不是 dB**（pp. 4、10）。1D 与二维列的输入元素数不同，不能假定所有列是完全相同输入布局 / 样本批次的直接比较。

仅在等位宽且忽略附加信息时，二维输入 / latent 元素数之比为 64，即有效载荷元素压缩约 64 倍（整理者计算）。这不包含 TGAP 真实梯度收集、压缩器训练和分发、下行全局模型、索引 / 序列化 / 协议等成本，也不是实测端到端网络加速。

表 3（p. 8）原文计算开销如下：

| 模块 | FLOPs | 原文 GPU memory | 原文 inference GPU time |
| --- | --- | --- | --- |
| Encoder | 0.81 G | 0.94 MB | 14.01 ms |
| Decoder | 1.80 G | 0.94 MB | 8.25 ms |
| LLM | 48.23 G | 6,809.71 MB | 33,601.13 ms |

第 4.2 节称时间取 10,000 个样本平均，但未完整说明 batch、输入长度、计时边界、memory 定义与模型配置；不可把该表当作完整训练峰值显存或模型吞吐。结论称压缩器训练约几分钟，未报告全部 TGAP 数据收集与系统开销的可复核时间账单（p. 10）。

## 实验设置与评价范围

| 项目 | 原文信息与出处 |
| --- | --- |
| 模型 | 主文为 LLaMA-7B、Alpaca-7B、Qwen-7B（p. 7）；附录表 4 另列 ChatGLM + C-Eval 配置，主结果表未对应给出完整 ChatGLM 结果，不补造 |
| 数据 | Dolly-15k 八类；C-Eval-dev 的 260 个带解释示例；从 MMLU 训练集合随机取 600 个 FAF 示例（pp. 7–8） |
| 非 IID 与客户端 | 正文：Dolly 按 Dirichlet  $`\alpha=0.5`$  分 100 段，LLaMA / Alpaca 各 100 clients、抽样比例 0.05；Qwen 为 3 clients、比例 1.0（p. 8） |
| 附录划分差异 | A.3：Dolly 等量分给 **10 clients**，C-Eval-dev 等量分给 3 clients（p. 14）；与正文 100-client / Dirichlet 说明不一致，不能合成一个确定配置 |
| TGAP / FAF 数据划分 | 第 4.8 节：同数据集 30% / 70%；跨数据集先称 C-Eval → MMLU，后又称 C-Eval → Dolly（p. 10），详见下文 |
| 环境 | NVIDIA RTX 4090、24 GB，Ubuntu 22.04、PyTorch 2.2.1、CUDA 12.4（p. 13）。联邦训练为计算环境中的模拟，未给真实多设备网络实验 |
| 评价 | C-Eval / MMLU 选择题分数；52 学科得分描述统计；Matrix Entropy；CNN/DailyMail 摘要的 Qwen API 四维打分（pp. 8、16–20） |
| 不确定性 | 未给主结果的多训练 seed 均值 / 置信区间；表 8 标准差是跨学科得分分散程度，表 13 为 API 评价分数分散程度，不能当作多随机种子训练方差 |

附录表 4（p. 14）的配置逐列保留：

| 模型 / 微调数据 | 通信轮数 | 客户端选择比例 | batch / micro-batch | learning rate | rank | local epochs |
| --- | --- | --- | --- | --- | --- | --- |
| ChatGLM / C-Eval | 5 | 1.0 | 24 / 8 |  $`3\times10^{-4}`$  | 16 | 3 |
| LLaMA / C-Eval | 5 | 1.0 | 24 / 8 |  $`2\times10^{-4}`$  | 16 | 3 |
| Alpaca / Dolly | 20 | 0.05 | 32 / 16 |  $`1.5\times10^{-4}`$  | 8 | 1 |
| LLaMA / Dolly | 20 | 0.05 | 32 / 16 |  $`1.5\times10^{-4}`$  | 8 | 1 |
| Qwen / MMLU | 8 | 1.0 | 8 / 4 |  $`3.5\times10^{-4}`$  | 8 | 2 |

这些为附录配置，因划分描述有冲突，不保证每个主表单元格都唯一对应上述配置。客户端选择比例与 Dirichlet 参数都用  $`\alpha`$  ，含义不同。

## 主要结果与适用边界

表 2（p. 7）选取 **Average** 分数；C-Eval 的 Qwen 行与 MMLU 行分开：

| 模型 / 评价 / 原表组 | Base | Cent | LoRA | Compress | 条件与解释 |
| --- | --- | --- | --- | --- | --- |
| LLaMA / C-Eval，组 1 | 22.8 | 24.9 | 25.8 | **26.6** | 整理者计算，相对 Base / Cent / LoRA 增加 3.8 / 1.7 / 0.8 个百分点 |
| Alpaca / C-Eval，组 2 | 25.9 | 25.7 | 25.8 | 26.8 | 非私有；并非每学科都最高，例如 Humanities 的 Cent 27.3 高于 Compress 27.1 |
| LLaMA-CEval / C-Eval，组 3 | 22.8 | 26.0 | 25.1 | 26.4 | 与组 1 标签 / 数据配置不同，不能混为同一提升 |
| Qwen / C-Eval，组 4 | 33.9 | 47.0 | 45.6 | 48.3 | 相对 Cent / LoRA 增加 1.3 / 2.7 个百分点，整理者计算 |
| Qwen / MMLU，组 8 | 56.07 | **56.60** | 56.33 | 56.44 | Compress 比 LoRA 高 0.11、比 Cent 低 0.16 个百分点，整理者计算 |
| Generalize-Compress-Qwen / MMLU，组 8 | 同上 | 56.60 | 56.33 | 56.37 | 跨数据集配置存在正文矛盾，不据标签填补；得分低于同表 Cent |

**同名配置与文字冲突**：表 2 组 7 的基本 Compress-FT-LLaMA 为 26.2，客户端 decoder 变体 D-Compress 为 26.6；组 1 同名 Compress 则为 26.6。p. 8 第 4.3 节文字和 p. 17 表 8 的 Compress 均值为 26.2。应保留组号 / 表号，不能静默用一个数字覆盖另一处。摘要“平均提升约 3 分”不能据此推广成相对 CL 和 FL 在所有模型 / 指标上的共同幅度。

DP-Qwen / MMLU，表 2 组 9–10（p. 7），预算为作者报告的 GDP  $`\epsilon`$ ，完整  $`\delta`$  和噪声配置未列明：

| 作者报告预算 | DP-LoRA | DP-Compress | 同表非私有 LoRA / Compress / Cent |
| --- | --- | --- | --- |
|  $`\epsilon=0.25`$  | 25.22 | 56.37 | 56.33 / 56.44 / 56.60 |
|  $`\epsilon=2`$  | 25.21 | 56.55 | 同上 |
|  $`\epsilon=8`$  | 25.67 | 56.31 | 同上 |

该表体现带噪实验的效用优势；DP-Compress 得分不随预算单调上升，且不是每个预算都超过非私有 LoRA。数值本身不能替代完整隐私核算，也不能证明抵御所有梯度重建攻击。

附录表 13（p. 20）在 CNN/DailyMail 摘要上使用 Qwen API，原文均值 ± 标准差：

| 维度 | Cent-LLaMA | Compress-FT-LLaMA | LoRA-FT-LLaMA |
| --- | --- | --- | --- |
| Relevance | 3.505 ± 0.562 | 3.462 ± 0.684 | 3.395 ± 0.850 |
| Fluency | 4.022 ± 0.209 | 3.835 ± 0.560 | 3.769 ± 0.576 |
| Coherence | 3.077 ± 0.425 | 2.989 ± 0.584 | 2.934 ± 0.708 |
| Consistency | 3.527 ± 0.561 | 3.396 ± 0.709 | 3.308 ± 0.821 |

Compress 四维均值高于 LoRA、低于 Cent；不能把第 C.3 节末尾的“与 Cent 相当”当作统计等效性证明。未完整说明评审模型 revision、评审 prompt、重复请求、API 温度与样本数量。Matrix Entropy 表 12（p. 19）中，各微调方法按给定位数相同：LLaMA 的 a/b/c 为 0.557/0.025/0.029，Alpaca 为 0.560/0.025/0.031；它不是本文方法显著优于其他微调的独立证据。

## 消融、泛化与噪声实验

- **Uformer（原文）**：0/1/2/3 blocks 的 LLaMA C-Eval Average 为 26.4 / 26.2 / 23.1 / 23.1（p. 17，表 9）。该实验支持较少 Uformer blocks 更有效，不代表完全取消所有卷积编码 / 解码。
- **ResNet（原文）**：0/1/2/3 blocks 为 22.9 / 23.9 / 22.8 / 26.2（p. 18，表 10）。3 blocks 最好，但 1 → 2 并不单调提高，不能改写成“block 越多必然越好”。
- **上下采样（原文）**：表 2 组 6 的 1/2/4 标签配置平均分为 26.2 / 26.2 / 26.4（p. 7）；标签、层数与配置映射需结合表 6–7 / 作者实现核实。
- **收敛（原文）**：Compress-Alpaca Epoch 10 / 17 / 19 平均分为 25.5 / 26.8 / 26.9；Uformer-1 Epoch 10 / 17 / 19 为 26.2 / 24.7 / 24.6（p. 18，表 11）。继续训练不保证每个配置都改善，客户端 local epochs、全局 rounds 与表中 Epoch 的关系需复现时锁定。
- **泛化冲突**：第 4.8 节先称 TGAP 用 C-Eval、FAF 用 600 个 MMLU 示例，后称 Generalize 用 C-Eval → Dolly；文字称结果在表 2 的“第七部分”，实际标签在第八组；还称泛化超过 Cent，但 56.37 < 56.60（pp. 7、10）。本笔记列出矛盾，不自行决定训练数据或改动数字。
- **小噪声与较大噪声（原文）**：表 14 中 LLaMA Compress 的 C-Eval Average 在  $`\sigma=5\times10^{-4}`$  为 26.4、无噪声为 26.2、 $`\sigma=5\times10^{-1}`$  为 24.6（p. 20）。相应 LoRA 无噪声 25.8、 $`5\times10^{-4}`$  为 24.4； $`5\times10^{-2}`$  的 24.3 标有星号、仅评估 Epoch 4，因为后续出现 NaN。p. 21 随后又对“同样噪声”描述第一轮 NaN，需核实所指配置；不能把所有结果当成完全相同训练轮次。
- **去噪误差与 SNR（原文）**：表 15 的 ResNet-3 在  $`\sigma=5\times10^{-2}`$  时，Compress MSE / SNR 为  $`5.24\times10^{-7}`$  /  $`2.73\times10^7`$ ，LoRA 为  $`2.50\times10^{-3}`$  /  $`5.72\times10^3`$  （p. 21）。但最小噪声  $`5\times10^{-5}`$  时 Compress MSE  $`4.59\times10^{-7}`$  高于 LoRA 的  $`2.50\times10^{-9}`$  ；并非任意噪声下重建误差都更低。表 1 与表 15 的误差量 / 归一化不同，不能直接混合排名。

## 隐私分析：机制顺序、假设与未覆盖范围

**威胁模型（原文）**：服务器 honest，客户端 semi-honest / curious；主要讨论梯度传输。基本版服务器持有 decoder，扩展上下行版本给客户端 decoder（p. 6，第 3.4 节；p. 9，第 4.4 节）。学习压缩与 decoder 部署限制并没有给出密钥体系或密码学安全证明，原文使用的 encrypted 不能据此等同于加密。基本版关于其他客户端没有 decoder 的论据，也不能直接套用到给客户端 decoder 的变体。

第 4.5 节（p. 9，式 (4)–(5)）写：

$$
\mathcal M=\operatorname{Aggre}\circ\operatorname{Noise}\circ\operatorname{Clip},\qquad
\widetilde{\mathcal M}=\operatorname{Dec}\circ\mathcal M\circ\operatorname{Enc}.
$$

即先编码，然后裁剪、加噪、聚合、解码。该顺序也与基本 FAF 中“逐客户端先解码再聚合”不同（pp. 5–6）。第 4.4 节和附录 D.2 则描述在低秩因子上先裁剪 / 加噪，再编码上传（pp. 8、20–21）。不能将两套次序拼成一个已确定的实现或隐私证明。

原文裁剪为  $`\operatorname{Clip}(A,C)=A\min(1,C/\lVert A\rVert_2)`$  ，加噪写  $`A+n_A,\ n_A\sim\mathcal N(0,\sigma I)`$  （p. 9）；附录 D.2 称先裁剪使敏感度为 1（p. 20）。第 4.5 节定义 add/remove-client 邻接；Lemma 1 给出  $`C/K`$  敏感度，其中  $`K`$  是选中客户端数。均值聚合的分母、裁剪作用于原因子还是 latent、非线性 decoder 的作用及动态  $`K`$  情况没有完全说明；其表达式不能被直接当作任意解码后更新的已验证敏感度。

GDP 公式保留原文渐近条件（p. 9，式 (6)–(7)）：

$$
p\sqrt T\longrightarrow\nu,\qquad
\mu=\nu\sqrt{e^{1/\sigma^2}-1},
$$

$$
\delta(\epsilon)=\Phi\!\left(-\frac\epsilon\mu+\frac\mu2\right)
-e^\epsilon\Phi\!\left(-\frac\epsilon\mu-\frac\mu2\right).
$$

 $`\Phi`$  是标准正态分布 CDF， $`T`$  是步骤数， $`p=K/M`$  是采样率， $`M`$  在该定理指总客户端数。原文称“Poisson sampling without replacement”，采样实现仍需核对；该渐近公式不是任意有限步训练的无条件精确 accountant。PDF 噪声分布写  $`\sigma I`$  ，GDP 式和表 15 的 MSE 又涉及  $`\sigma^2`$  ，方差 / 标准差 / noise multiplier 的含义需统一。完整实验  $`\delta`$  、裁剪阈值、各预算实际  $`\sigma`$  及 A/B 两次发布的联合预算未明确给出。

**整理者归纳 / 待核实**：TGAP 收集真实梯度并训练 encoder / decoder，是额外的信息发布 / 数据使用阶段；FAF 的 DP 声明不自动覆盖这一阶段，数据依赖的压缩器权重是否可视为固定公开后处理也需说明。去噪后处理可以改善已私有化输出的效用，但去噪性能不是端到端 DP 或抵御重建攻击的证明。论文未提供覆盖所有上述发布内容的完整组合核算及攻击验证。

## 与已有五篇论文的关系

以下为整理者基于各篇已读版本的比较，数字与隐私预算不能跨条件直接排名。

| 论文 | 与 CG-FedLLM 的联系与区别 |
| --- | --- |
| [DR-Encoder](../2024-wu-dr-encoder/notes.md) | CG 的 TGAP 用真实时间序列梯度；DR 的 RandomPrior 传输均值 / 标准差并合成梯度训练 AutoEncoder（DR pp. 3–4、9）。DR 笔记中的 informative-prior / FedCG 对照有助于理解设计差别，但不能把 DR 所用对照自动认作本上传 v3 的完全相同实现。DR 统计量发布本身的隐私也仍待核实；两篇年份先后不证明未经文献支持的继承关系 |
| [FLASC](../2024-kuo-flasc/notes.md) | CG 学习低维 latent 并重建；FLASC 对适配器更新做 Top-K 传输、保持稠密本地训练和服务端状态。两者保留比例、TGAP 成本、模型规模与上下行设置不同（FLASC pp. 4–7）；不能将 64 倍元素比与累计通信 3–10 倍直接排名 |
| [FFA-LoRA](../2024-sun-ffa-lora/notes.md) | CG 算法 1 分别聚合两个可训练因子；FFA 共享冻结 A，使聚合对权重增量线性（FFA pp. 4–6）。CG 压缩器改善单客户端重建，不自动消除因子聚合产生的跨客户端项；也不自动解决双因子噪声乘积 |
| [AdaLoRA](../2023-zhang-adalora/notes.md) | AdaLoRA 控制可学习增量的方向 / 秩预算，CG 压缩联邦传输表示。不同客户端采用动态秩时，布局、基底对齐和固定 AutoEncoder 输入需另设计；未验证二者组合（AdaLoRA pp. 4–6） |
| [SVD-LLM](../2025-wang-svd-llm/notes.md) | SVD-LLM 压缩模型主干权重并恢复精度，CG 主要压缩微调时传输的因子，不因此缩小推理主干；校准输出误差与梯度重建误差不同（SVD-LLM pp. 3–5） |

以两客户端为例，CG 算法所写的因子求和满足（整理者代数展开，CG p. 5 / FFA p. 4）：

$$
(B_1+B_2)(A_1+A_2)
=B_1A_1+B_2A_2+B_1A_2+B_2A_1.
$$

平均或按数据量加权同样一般不使因子平均的乘积等于权重增量的平均。需要对齐实际 scaling、初始化与聚合定义后才可评价误差；这不是已经复现并证明 CG 在某个任务失效的结论。冻结共享因子、稀疏传输、自适应秩或主干低秩化与学习压缩器的联合方案均为**未验证研究设想**。

## 官方代码、数据与复现信息

上传 PDF 没有给出 CG-FedLLM 专属作者实现地址；2026-10-12 的题名 / 作者检索也未核实可归属于作者的官方仓库。第 4.1 节使用 FedIT，参考文献 [57] 的 [FederatedGPT-Shepherd](https://github.com/JayZhang42/FederatedGPT-Shepherd) 是所引用联邦框架，不能当作已经验证的 CG-FedLLM 官方实现。

数据 / benchmark 来源：[Dolly-15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k)、[C-Eval](https://github.com/hkust-nlp/ceval)、[MMLU](https://github.com/hendrycks/test)。附录 A–B 为环境和架构，附录 C 为扩展评价，D 为梯度分布 / 噪声，E 为 BA 可视化（pp. 13–27）。

复现前需取得或明确：目标模型 / tokenizer revision、数据划分文件和 seed、每轮采样与 step 定义、TGAP 收集量及 AutoEncoder 训练 epochs / checkpoint、张量转置与展平、重建损失归一化、聚合权重 / scaling、上下行消息内容、裁剪 / 加噪顺序、delta 和联合 accountant、Qwen API 评审配置。表 6–7 的首个 decoder 行写 `deconv1` 且通道 4 → 32，后续又从 64 → 32，需核对架构连接（pp. 15–16）；不将疑似排版错误改造成猜测实现。没有运行模型训练、隐私攻击、网络通信或复现实验。

## 阅读总结与局限

**原文解决的问题**：以预先训练的学习压缩器，降低 federated LoRA 更新的传输表示规模，并在若干带噪 / 非私有实验中保持或改善效用。

**值得借鉴（整理者归纳）**：将压缩器学习与目标模型联邦微调分阶段；同时检查输入布局、重建误差与下游任务；把表示元素数、全流程通信、计算开销和隐私发布范围分开记账。

**适用条件与局限（整理者推断）**：依赖目标模型梯度分布和布局的稳定性；非 IID / 域迁移、动态秩和新模型可能需要重新训练压缩器。压缩器增加收集、训练、分发及编解码成本；实验未覆盖真实网络端到端收益。隐私和聚合的关键实现仍有歧义，结果无完整多 seed 统计。作者明确提出后续研究更高效的 AutoEncoder 架构和训练策略（p. 10）。

## 单光子 LiDAR 参数

不适用。本文 SNR 是梯度重建误差对应的信号功率比，不是光子信号 / 背景统计；GPU 推理时间、通信轮数、模型张量尺寸不能替换单光子探测器阵列、距离、目标速度、每像素光子数、采集时间、成像帧率或定位误差。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [原始 PDF](paper.pdf) · [来源与许可](source.md)
