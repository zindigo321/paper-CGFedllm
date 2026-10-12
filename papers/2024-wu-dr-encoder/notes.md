# DR-Encoder: Encode Low-rank Gradients with Random Prior for Large Language Models Differentially Privately

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 完整题名 | DR-Encoder: Encode Low-rank Gradients with Random Prior for Large Language Models Differentially Privately |
| 作者 | Huiwen Wu, Deyi Zhang, Xiaohan Li, Xiaogang Xu, Jiafei Wu, Zhe Liu（PDF p. 1；AAAI 正式记录同序） |
| 正式发表 | Proceedings of the AAAI Conference on Artificial Intelligence，39(26)，27706–27714，2025-04-11；AAAI-25 Special Track on AI Alignment |
| 正式 DOI | [10.1609/aaai.v39i26.34985](https://doi.org/10.1609/aaai.v39i26.34985) |
| 实际阅读版本 | 用户上传的 arXiv:2412.17053v1，提交日期 2024-12-22，文档日期 2024-12-24；17 页完整预印本，p. 1 脚注称已被 AAAI-25 接收；不是本次取得的正式出版 PDF |
| 预印本 DOI | [10.48550/arXiv.2412.17053](https://doi.org/10.48550/arXiv.2412.17053) |
| 官方来源 | [AAAI 出版页](https://ojs.aaai.org/index.php/AAAI/article/view/34985)；[arXiv v1](https://arxiv.org/abs/2412.17053v1) |
| PDF 与引用 | [本地原始 PDF](paper.pdf)；[官方 v1 PDF](https://arxiv.org/pdf/2412.17053v1)；[citation.bib](citation.bib)；[许可与校验值](source.md) |

页码均为**上传 PDF 的物理页码**。下面的数值与方法依据上传预印本，不宣称与 AAAI 正式版逐项一致。元数据核对日期：2026-10-11；PDF 为 CC BY-NC-ND 4.0，按非商业、原样、有署名和来源的条件分享。

## 摘要

DR-Encoder 研究 federated LLM 微调中，梯度压缩器预训练和后续梯度交换造成的信息泄漏与通信成本。它收集各层低秩梯度的均值、标准差，用 Gaussian random prior 合成梯度训练 AutoEncoder；在微调阶段编码、裁剪、加入 Gaussian noise、聚合并解码，用 GDP 和 RDP 分析隐私。Qwen-7B / MMLU 在  $`\epsilon=4`$  时得分 56.20，直接带噪 LoRA 为 25.50；其“端到端隐私”是作者主张，统计信息发布和部分算子定义仍需进一步核实（pp. 2–7、14–15）。

## 背景、已有方法不足与贡献

- **泄漏途径（原文）**：发送真实梯度训练压缩器可能导致梯度重建 / membership inference；真实梯度的信息可进入 AutoEncoder 权重，产生 model inversion 风险；微调阶段继续发送梯度也会泄漏（p. 3）。
- **已有方法不足（原文）**：informative-prior gradient compression 使用真实梯度，压缩 / 去噪有效，但压缩器预训练阶段本身缺少本文所针对的保护（pp. 2–3、9）。
- **贡献（原文）**：统计量驱动的 random-prior AutoEncoder 预训练；低秩压缩梯度的 DP 微调；GDP / RDP 隐私分析与效用、通信实验（pp. 2–6）。

## 两阶段方法与核心公式

**阶段一：RandomPrior（pp. 3–4，算法 1）。** 客户端按层、epoch 收集低秩梯度部分  $`A,B`$  的均值  $`m`$ 、标准差  $`s`$ ，发送统计量；服务端据此生成 Gaussian synthetic gradients，训练重建 AutoEncoder，再将 encoder 发给客户端，保留 decoder。

可将重建目标归纳为（整理者用统一符号表述算法 1）：

$$
\hat G\sim\mathcal N(m,s^2),\qquad
\min_{\mathrm{Enc},\mathrm{Dec}}
\mathbb E_{\hat G}\left[\lVert\mathrm{Dec}(\mathrm{Enc}(\hat G))-\hat G\rVert_2^2\right].
$$

这里  $`\hat G`$  代表低秩梯度部分的合成样本， $`s`$  是标准差，因此用  $`s^2`$  明示方差；原文写  $`\mathcal N(m,s)`$ ，其第二参数与方差 / 标准差的记号需实现时核对。统计量更新超参数为  $`\beta_1=0.99`$ 、 $`\beta_2=0.9`$ 、 $`h_1=10^{-5}`$ 、 $`h_2=10^{-3}`$ （p. 3）。上述统一公式不是作者提供的可直接运行实现。

**阶段二：私有联邦微调（pp. 3–5，算法 2；p. 14，式 (8)）。** 以算法 2 和附录算子次序为准：

$$
\mathcal M=\mathrm{Dec}\circ\mathrm{Aggregation}\circ
\mathrm{Noise}\circ\mathrm{Clip}\circ\mathrm{Enc}.
$$

客户端先编码低秩梯度，再裁剪与加噪后上传；服务端聚合、解码、更新权重并下发。正文 p. 2 对加噪 / 编码、encoder / decoder 部署的描述与算法 2 不完全一致，不能据此自行确定另一套实现。

原文给两个低秩部分的噪声方差为  $`4\sigma_A^2/K^2`$  与  $`4\sigma_B^2/K^2`$ ，且取  $`\sigma_A=\sigma_B=\sigma`$ （p. 4，式 (3)–(4)）。 $`K`$  为选中客户端数量， $`M`$  为总客户端数量， $`p=K/M`$  为采样率， $`T`$  为迭代数， $`\sigma`$  为 noise multiplier， $`C`$  为裁剪阈值。原文梯度记作  $`G_i^t\approx A_i^tB_i^t`$ （pp. 3、5），服务端更新为  $`W_{t+1}=W_t-\eta^tG_t`$ （p. 4，式 (6)）。

GDP 渐近组合形式（p. 6，式 (7)；pp. 14–15）：

$$
p\sqrt T\longrightarrow\nu,
\qquad
\mu=\nu\sqrt{e^{1/\sigma^2}-1}.
$$

 $`\mu`$  是 GDP 参数，再转换为  $`(\epsilon,\delta)`$ -DP。这里有渐近前提，不能把该表达式直接当作任意有限轮训练的无条件精确保证。正文表 3 同时给 GDP 与 RDP 的预算，后续实验主要使用 GDP 的  $`\epsilon`$ （p. 9）。

## 实验设置

| 项目 | 原文信息与出处 |
| --- | --- |
| 模型、任务 | Qwen-7B 用 MMLU 数据微调并用 MMLU 评估；LLaMA-7B 用 Databricks-dolly-15k 微调并用 C-Eval 评估（pp. 7–8、13） |
| 数据划分 | Dolly 分为 100 个客户端段，category Dirichlet；MMLU 随机分为 3 段；Dirichlet 系数原文未给出（p. 13） |
| LoRA rank、学习率 | 都为  $`r=8`$ ；LLaMA  $`1.5\times10^{-4}`$ ；Qwen  $`3\times10^{-4}`$ （pp. 6、13，表 1 / 6） |
| 客户端采样 | LLaMA 0.05；Qwen 1.0（同上） |
| 通信轮数 | LLaMA 20；Qwen 主文表 1 为 4、附录表 6 为 8，待核实，不能任选后用于隐私核算 |
| local batch / micro-batch / epochs | LLaMA 32 / 16 / 1；Qwen 8 / 4 / 2（p. 13，表 6） |
| 对比方法 | Base、Cent、LoRA、FedCG（informative prior）、DR-Encoder（random prior），pp. 7–9 |
| 环境与统计 | Ubuntu 22.04、PyTorch 2.2.1、CUDA 12.4、24 GB NVIDIA GPU；具体 GPU 型号、随机种子数量、误差条原文未提供（p. 13） |
| DP 配置 |  $`\epsilon\in\{0.25,0.5,1,2,4,8\}`$ ；实际采用的  $`\delta`$  未被明确完整记录，p. 15 的常见  $`10^{-5}`$  不能自动等同于本实验设置 |

这些是单机模拟联邦训练 / 离线 benchmark；不代表部署在真实异构设备上的通信时延或实时吞吐。

## 主要结果与范围

| 模型、评估、预算 | Base | 非私有 LoRA | 同预算带噪 LoRA | DR-Encoder | 来源 |
| --- | --- | --- | --- | --- | --- |
| Qwen-7B，MMLU Average， $`\epsilon=\infty`$  | 56.07 | 56.77 | 不适用 | 56.13 | p. 6 表 2；p. 7 表 4 |
| Qwen-7B，MMLU Average， $`\epsilon=0.25`$  | 56.07 | 56.77 | 25.22 | 51.23 | p. 7，表 4 |
| Qwen-7B，MMLU Average， $`\epsilon=1`$  | 56.07 | 56.77 | 25.09 | 53.48 | 同上 |
| Qwen-7B，MMLU Average， $`\epsilon=4`$  | 56.07 | 56.77 | 25.50 | 56.20 | 同上 |
| Qwen-7B，MMLU Average， $`\epsilon=8`$  | 56.07 | 56.77 | 25.67 | 56.48 | 同上 |
| LLaMA-7B，C-Eval Average， $`\epsilon=\infty`$  | 22.8 | 25.8 | 不适用 | 26.2 | p. 6，表 2 |
| LLaMA-7B，C-Eval Average， $`\epsilon=0.25`$  | 22.8 | 25.8 | 原文未提供 | 26.1 | p. 7，表 4 |
| LLaMA-7B，C-Eval Average， $`\epsilon=0.5`$  | 22.8 | 25.8 | 原文未提供 | 23.3 | 同上 |
| LLaMA-7B，C-Eval Average， $`\epsilon=8`$  | 22.8 | 25.8 | 25.4 | 26.1 | 同上 |

Qwen 结果体现压缩器在带噪设置下的效用；**DR-Encoder 非私有得分并未超过非私有 LoRA**。LLaMA 随预算变化并不单调，不能把 Qwen 的趋势当作所有模型均成立（整理者归纳）。

通信结果严格限于 **AutoEncoder 预训练前的梯度 / 统计量收集阶段**（p. 9，表 5）：FedCG 传输 167,772,160 个数值，DR-Encoder 为 10,240；数值个数之比为  $`6.10\times10^{-5}`$ 。原表同时标 160 MB / 0.078 MB，但未清楚给出数值精度，两个字节数与个数比例也不一致。本笔记保留原表声明、不按它推断实际网络字节或全程总通信压缩倍数。

噪声核算示例：Qwen  $`\sigma=1.63`$  时 RDP / GDP 的  $`\epsilon`$  为 4.66 / 4.00；LLaMA  $`\sigma=0.52`$  时为 5.57 / 4.00（p. 6，表 3）。不同 accountant 的数值不能互换，也不能只比较  $`\epsilon`$  而不比较采样率、轮数和  $`\delta`$ 。

## 消融、局限性与作者后续工作

**原文比较 / 消融**：FedCG 的 informative prior 与 random prior 比较、多个隐私预算、GDP 与 RDP 预算比较（pp. 6–9）。附录尝试不同 Uformer / 采样层数量，称选择 7 downsampling + 6 Uformer + 7 upsampling 来平衡效率与效用，但未提供逐配置消融数值（p. 15）。因此不能补造完整架构消融表。

**整理者审慎推断，需复现核实**：

1. p. 3–4 分享的均值 / 标准差来自私有梯度，未给出这些统计量发布的 DP 随机机制及其预算组合。用合成梯度训练压缩器本身，不能自动证明此前公开统计量没有泄漏。
2. p. 3 式 (1)–(2) 的裁剪写成范数乘标量，与后续矩阵算子的类型关系存在疑点；p. 4 式 (5) 对两个带噪因子做乘积，而 p. 14 用 Gaussian mechanism / post-processing 证明，需核对实际高斯机制作用对象和先后次序，不能直接实现一个猜测版本。
3.  $`K,N,M`$  与客户端 / 样本采样记号不完全统一，Qwen 轮数冲突； $`\delta`$ 、encoder 训练 epoch / learning rate / latent size 等关键复现项未完整给出。
4. 表 2 的非私有 MMLU 得分和表 4 不支持“任何预算都超过非私有 baseline”的泛化主张；未提供攻击实验来直接验证声称防止的所有攻击。

**作者明确后续工作**：推广到 Large Vision Model 和 Large Multimodal Model（p. 10，结论）。

## 官方代码、数据与复现信息

官方代码：上传 PDF 未提供作者 DR-Encoder 实现地址；本次公开检索也未核实可归属于作者的官方仓库。文中引用的其他 FedLLM / 压缩器项目不等于本文官方实现。

数据：[Databricks-dolly-15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k)、[MMLU](https://github.com/hendrycks/test)、[C-Eval 官方仓库](https://github.com/hkust-nlp/ceval)。这些是数据 / benchmark 来源，不包含本文全部划分、统计量和模型 checkpoint。AutoEncoder 的 Uformer 表 7 在 p. 14，流程在 p. 13 图 3，隐私证明在 pp. 14–15。没有实际运行训练，未声称复现成功。

## 阅读总结

**原文解决的问题**：用随机先验合成梯度替代真实梯度收集训练压缩器，并将压缩与带噪联邦微调结合，降低预处理通信成本和部分带噪微调的效用损失。

**值得借鉴（整理者归纳）**：统计量驱动的合成训练与任务模型训练分阶段设计，以及同时记录通信收益和隐私 accountant。若用于实际私有系统，首先需补齐统计量发布机制、邻接定义和完整组合核算，再判断“端到端”保证是否覆盖所有发布内容。

## 与 CG-FedLLM 扩展版的阅读联系

2026-10-12 新增的 [CG-FedLLM v3 扩展版笔记](../2025-wu-cg-fedllm/notes.md) 基于 2025 年 27 页上传件，不改动本篇 2024 年 v1 的阅读范围和原核对日期。该比较为整理者归纳：CG 的 TGAP 收集真实时间序列梯度训练 AutoEncoder（CG pp. 4–5、19）；本篇 RandomPrior 用均值 / 标准差和 Gaussian 合成梯度（本篇 pp. 3–4、9）。

CG 的二维 CR 1.56% 是 FAF 编码输出 / 输入的元素比（CG pp. 4–5），本篇  $`6.10\times10^{-5}`$  是预训练收集阶段统计量 / 梯度的数值个数比（本篇 p. 9）；两者阶段和分母不同，不能直接排名。CG 的真实梯度收集隐私与本篇统计量发布隐私均应单独核查。CG 正文 / 附录的加噪与编码次序不一致（CG pp. 8–9、20–21），也不能据其重新解释本篇算法。

本篇 informative-prior / FedCG 对照提供了方法类别上的联系，但尚未核实其实现与 CG 上传 v3 完全一致；不依据年份或相似架构推断具体继承关系。进一步比较应锁定代码、模型、数据划分、聚合方式、采样、轮数、delta、噪声参数和预训练发布范围。

## 单光子 LiDAR 参数

不适用。论文没有单光子探测器、阵列规模、测距 / 速度、SNR/SBR、每像素光子数、采集时间、成像帧率、空间分辨率或定位误差实验；这里的通信轮数和 GPU 显存不是 LiDAR 参数。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [原始 PDF](paper.pdf)
