# Improving LoRA in Privacy-preserving Federated Learning

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 完整题名 | Improving LoRA in Privacy-preserving Federated Learning |
| 作者 | Youbang Sun, Zitao Li, Yaliang Li, Bolin Ding（PDF p. 1；ICLR 正式记录同序） |
| 发表渠道与年份 | The Twelfth International Conference on Learning Representations，ICLR 2024 |
| 实际阅读版本 | arXiv:2403.12313v1，2024-03-18；17 页，页眉明确 Published as a conference paper at ICLR 2024；有完整正文、参考文献、附录；属于 arXiv 托管的会议论文版本，不声称与 proceedings 文件逐字节一致 |
| DOI | 会议 DOI：所核对官方记录未提供；arXiv DOI：[10.48550/arXiv.2403.12313](https://doi.org/10.48550/arXiv.2403.12313)，不是独立会议 DOI |
| 官方来源 | [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/4e243e95c913b367775d71d7182b99d9-Abstract-Conference.html)；[OpenReview](https://openreview.net/forum?id=NLPzL6HWNl)；[arXiv v1](https://arxiv.org/abs/2403.12313v1) |
| PDF、引用与许可 | [本地原始 PDF](paper.pdf)；[官方 v1 PDF](https://arxiv.org/pdf/2403.12313v1)；[citation.bib](citation.bib)；[source.md](source.md)；上传版许可为 CC BY 4.0 |

页码均指上传 PDF 的物理页码。元数据与许可核对日期：2026-10-11。以下明确区分作者结论与整理者的推断。

## 摘要

FFA-LoRA（Federated Freeze A LoRA）研究 LoRA 在 privacy-preserving cross-silo FL 中的不稳定性：客户端联合优化两个因子，但服务器分别平均因子，可能产生聚合不匹配；两个因子同时带噪还引入噪声乘积；缩放因子  $`\alpha`$  影响优化。方法共享并冻结随机初始化的  $`A_0`$ ，只训练、传输和聚合零初始化的  $`B`$ ，使适配器聚合对权重更新保持线性。在 3-client、强异质性、客户端 DP-SGD 的 RoBERTa-Large / MNLI-m 实验中， $`\epsilon=6`$  时从 LoRA 的  $`39.46\pm14.3\%`$  提高到  $`78.81\pm0.8\%`$ ；这些数值是特定条件下 20 次实验的均值和标准差（pp. 4–7，表 1）。

## 背景、不足与贡献

- **原文问题**：非 IID 数据和多步本地更新、DP 噪声、 $`\alpha`$  选择同时影响 LoRA 的联邦优化（pp. 2、4–5）。
- **聚合不足（原文）**：平均  $`A`$ 、平均  $`B`$  再相乘，一般不等于平均  $`BA`$ ；局部等价的低秩表示也可能在聚合后产生差异（p. 4）。
- **贡献（原文）**：分析上述三种 discordance；提出 Freeze-A 修改；给出聚合、噪声和平滑性 / 动态关系论证，并在语言和视觉任务验证（pp. 2、5–9、13–17）。

## 方法流程与核心公式

1. 初始化冻结的预训练权重  $`W_0`$ ，在所有客户端使用**共同**的随机非零  $`A_0`$ ，令  $`B_0=0`$ 。
2. 客户端只对  $`B`$  做 SGD 或 DP-SGD；分类头保持冻结。
3. 将  $`B`$  上传服务端并用 FedAvg 平均，再下发继续本地训练。无需每轮交换  $`A_0`$ （pp. 5–7）。

基本参数化（p. 5）：

$$
W=W_0+BA_0,
\qquad B\in\mathbb R^{d\times r},\quad A_0\in\mathbb R^{r\times k}.
$$

 $`r`$  是适配器秩， $`d,k`$  是权重输出 / 输入维度。实验也使用 LoRA 的缩放  $`\alpha/r`$ ；以上省略常数缩放以对应方法描述。只有  $`B`$  可训练；共同的  $`A_0`$  是以下线性聚合成立的条件：

$$
\left(\sum_i p_iB_i\right)A_0=\sum_i p_i(B_iA_0),
\qquad \sum_i p_i=1.
$$

这是对 p. 5 式 (4) 两客户端例子的整理者推广。它消除的是**低秩因子单独聚合导致的额外误差**，不意味着所有 client drift 或非 IID 优化问题都消失。

LoRA 带噪乘积与冻结后对照（pp. 4、6）：

$$
(B+\xi_B)(A+\xi_A)=BA+\xi_BA+B\xi_A+\xi_B\xi_A,
$$

$$
(B+\xi_B)A_0=BA_0+\xi_BA_0.
$$

 $`\xi_A,\xi_B`$  为更新中的噪声；冻结  $`A`$  去掉了双噪声乘积项。这里是论文的局部分析，不能据此推导所有超参数下的效用保证。

DP-SGD 机制（p. 3，用统一记号）：

$$
\bar g=\frac1{|\mathcal B|}
\left[\sum_{x\in\mathcal B}\operatorname{Clip}(\nabla\ell_x,C)
+z\right],
\qquad z\sim\mathcal N(0,\sigma^2C^2I).
$$

 $`\mathcal B`$  为 batch， $`C`$  为 per-sample clipping threshold， $`\sigma`$  为 noise multiplier。邻接定义为相差一条记录；每个客户端发布的更新已通过本地 DP-SGD 处理，不依赖服务器可信（p. 3；p. 16，A.5）。这与 FLASC 的服务端 client-level DP 不同，也不能笼统写成同一 DP 设置。

平滑性结果：若原损失对  $`W`$  是  $`L`$ -smooth、固定  $`A_0`$  的范数不超过  $`C_A`$ ，则对  $`B`$  的损失可给出  $`LC_A^2`$  平滑上界；若两个因子都训练，仅原损失 smooth 不足以推出全局同类保证（p. 13，定理 2）。 $`C_A`$  是这里为避免与 DP 裁剪阈值混淆而重命名的常数。

**参数 / 通信量（整理者计算）**：LoRA 为  $`r(d+k)`$ ，FFA-LoRA 为  $`rd`$ ，仅当  $`d=k`$  时是恰好一半；非方阵比例为  $`d/(d+k)`$ 。作者实验报告的适配器参数约减半，不应宣称总模型计算量或完整系统时间必然减半。

## 实验设置

| 设置 | 原文信息 |
| --- | --- |
| 主模型与任务 | RoBERTa-Large，355M，MNLI、SST-2、QQP、QNLI；LLaMA-7B / GSM8K；附录 ViT / Food-101（pp. 6–9、14、17） |
| 联邦场景 | 3-client cross-silo；主分类实验 1000 communication rounds，每轮 10 local steps，batch size 200，sequence length 128（p. 7） |
| 强异质性 | 二分类客户端标签比例 [0.1,0.9] / [0.9,0.1] / [0.5,0.5]；三分类 [0.9,0.05,0.05] 的三种轮换（p. 7） |
| 优化与适配 | SGD / DP-SGD；attention 与 feed-forward 层均加 adapter；分类头冻结；主实验  $`r=8,\alpha=8`$ （p. 7） |
| 学习率搜索 | LoRA：0.01 / 0.02 / 0.05 / 0.1；FFA：0.1 / 0.2 / 0.5 / 1，分别报告最佳（p. 7） |
| DP |  $`\delta=10^{-5}`$ ， $`\epsilon=6,3,1`$ ；Opacus 计算噪声； $`C\in\{2,5,10\}`$  搜索（p. 7） |
| 环境、统计 | NVIDIA Tesla A100，half precision；表 1 为 20 runs 的均值 ± 标准差（pp. 6–7） |

这是模拟联邦微调的离线任务评估；原文没有真实网络传输时延测量。本文 full / mild / severe heterogeneity 的分布与 FLASC 的 Dirichlet cross-device 分布不同。

## 主要定量结果

下面取 p. 7 表 1，全部为 Accuracy (%)、20 runs 的均值 ± 标准差：

| 隐私条件 | MNLI-m LoRA | MNLI-m FFA-LoRA | QNLI LoRA | QNLI FFA-LoRA |
| --- | --- | --- | --- | --- |
| 非私有 | 82.03 ± 10.7 | 85.05 ± 1.1 | 88.95 ± 6.7 | 90.35 ± 1.9 |
|  $`\epsilon=6`$  | 39.46 ± 14.3 | 78.81 ± 0.8 | 84.99 ± 1.1 | 87.27 ± 1.0 |
|  $`\epsilon=3`$  | 35.82 ± 8.9 | 77.42 ± 0.8 | 83.94 ± 0.6 | 86.18 ± 1.7 |
|  $`\epsilon=1`$  | 33.80 ± 1.6 | 75.05 ± 1.3 | 78.93 ± 6.8 | 81.53 ± 1.4 |

SST-2 的同表  $`\epsilon=6`$  时 LoRA / FFA 为  $`93.70\pm0.5`$  /  $`93.73\pm0.3`$ ，差距很小。MNLI 大幅提升不能当成所有任务均同等受益。

GSM8K：LLaMA-7B 上 FFA 17.12%，本文 LoRA 最佳 15.68%，整理者计算提高 1.44 个百分点（pp. 9、14）；该实验的完整训练配置主要引用另一篇 FS-LLM 工作，不能只凭这个数字声称已复现。

同参数预算比较须谨慎：p. 9 表 3 mild heterogeneity 下 LoRA  $`r=8`$  和 FFA  $`r=16`$  均约 1.57M 参数，MNLI-m 分别 87.01 / 85.82，SST-2 为 93.55 / 95.30。说明“冻结一定更好”不是逐任务、逐预算的普遍结论。

## 消融、适用条件与局限性

- **异质性（原文）**：非私有 MNLI-m 的 iid / mild / severe 条件下，LoRA 为 86.90 / 87.01 / 82.03，FFA 为 87.13 / 87.04 / 85.05（p. 8，表 2）。强异质性时差距增大。
- **秩与 DP（原文）**：QNLI， $`\epsilon=1`$ ， $`r=2`$  时 LoRA / FFA 为 58.15 / 82.64（p. 9，表 4）；也存在其他预算下 LoRA 更高的单元格，不能概括成逐格优胜。
- **缩放（原文）**：调整 learning rate 后，FFA 的不同  $`\alpha`$  配置较稳定；LoRA 的同种 scaling 可能明显退化，但重新搜索学习率仍能恢复较高准确率（p. 17，表 7）。“不依赖  $`\alpha`$ ”有对应学习率 / 初始化 / 轨迹条件，不等于固定学习率任意换  $`\alpha`$  都不变（pp. 6、13–14）。
- **初始化（原文）**：QNLI 的 Kaiming / orthogonal / SVD 初始化均值为 91.84 / 92.16 / 91.50；作者认为差距不足以给出确定结论（p. 17，表 9）。
- **QVP 探索（原文）**：冻结两个随机投影，只训练中间  $`V`$  的  $`W=W_0+Q_0VP_0`$  可进一步减小参数量，但同预算不及 FFA 等方法（pp. 14、16）。
- **适用条件（整理者归纳）**：共享固定非零  $`A_0`$ 、跨机构数据异质性、多步更新、客户端 DP-SGD；随机投影子空间能覆盖任务所需更新时较合适。
- **局限性（整理者推断）**：冻结  $`A_0`$  缩小可学习子空间，可能损害某些任务效用；参数减少不自动减少同等比例的主干前向 / 反向计算；跨设备 central client-level DP 的结果不能从此论文直接推出。
- **作者明确后续工作**：更少参数的 adapters、orthogonal 等替代初始化、与 random kernel methods 的理论联系（p. 9；pp. 14、16–17）。

## 官方代码、数据与复现信息

**官方实现**：上传 PDF 未提供专属官方代码地址；本次检索未核实作者发布的 FFA-LoRA 官方仓库。社区库包含 FFA-LoRA 不能据此认定为官方实现，因此此处不虚构代码链接。

数据为 GLUE（MNLI / SST-2 / QQP / QNLI）、GSM8K、Food-101。模型初始化来自 Hugging Face；DP engine 为 Opacus（p. 7、p. 16）。原文未完整给出实验依赖锁文件、所有 seed / 客户端划分文件、全部 checkpoint，以及每个任务最优 learning rate / noise scale 的完整列表。复现应对每个客户端数据量单独计算采样率、累计本地 DP 步数，不能只用 communication rounds 当 DP steps（p. 16，A.5）。

上传件的视觉扩展也需谨慎：p. 17 表 8 最后两列分别标 “FL iid LoRA” 与 “FL non-iid FFA-LoRA”，不能把 81.33% / 82.10% 作为同条件的严格方法对比；表 9 的 dispersion 列标为 variance，本笔记不擅自转换成 standard deviation。

## 阅读总结

**原文解决的问题**：让 LoRA 的参数化与 FedAvg 聚合、客户端 DP-SGD 更相容，减少双因子交互导致的额外问题。

**值得借鉴（整理者归纳）**：共享固定基底使因子聚合与权重更新建立线性关系；检查参数化是否与分布式聚合和噪声机制相容。应用时应先匹配隐私保护粒度、实际参数预算、异质性和优化器，再判断是否值得冻结；与 FLASC 的不同结论可以由实验条件差异解释，不能直接互相否定。

## 单光子 LiDAR 参数

不适用。Food-101 视觉分类扩展不涉及单光子 LiDAR 探测器、阵列、测距、光子统计、采集 / 重建时间或定位误差。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [原始 PDF](paper.pdf)
