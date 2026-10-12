# Federated LoRA with Sparse Communication

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 上传版完整题名 | Federated LoRA with Sparse Communication |
| 作者 | Kevin Kuo, Arian Raje, Kousik Rajesh, Virginia Smith（PDF p. 1） |
| 实际阅读版本 | arXiv:2406.05233v1，2024-06-07；文档日期 2024-06-11；20 页，正文 12 页、参考文献和附录完整；p. 1 明示 Preprint. Under review. |
| 上传版 DOI | [10.48550/arXiv.2406.05233](https://doi.org/10.48550/arXiv.2406.05233)，预印本 DOI |
| 后续正式发表 | **FLASC: Federated LoRA with Sparse Communication**，Proceedings of the ACM Conference on AI and Agentic Systems（CAIS 2026），2026-05-26，pp. 990–1008 |
| 正式版 DOI | [10.1145/3786335.3813151](https://doi.org/10.1145/3786335.3813151)，由出版社提交的 Crossref 元数据确认；[官方注册记录](https://api.crossref.org/works/10.1145/3786335.3813151)；[ACM 出版页](https://dl.acm.org/doi/10.1145/3786335.3813151) |
| 全文与 BibTeX | [官方 v1 PDF](https://arxiv.org/pdf/2406.05233v1)；[arXiv 版本页](https://arxiv.org/abs/2406.05233v1)；[citation.bib](citation.bib)；[上传件与许可记录](source.md) |

**范围声明**：本次已逐页读取的是用户上传的 **2024 年 v1 全文**。2026 正式版元数据已核实，但正式版全文未取得，不能将新版本的算法、结果或页码写入本笔记。目录固定为上传阅读版本的 2024 年。公开仓库未收录此上传版 `paper.pdf`，因为它的 arXiv 非独占分发许可未明确授权本仓库再分发；2026 正式版的 CC BY 许可不能自动转用于 v1。

下文页码均指上传 PDF 的物理页码。元数据 / 官方代码链接核对日期：2026-10-11。

## 摘要

FLASC 在通信受限的 cross-device federated learning 中，将 LoRA 的本地训练与传输稀疏化分开：客户端下载稀疏权重，但本地可更新整个 LoRA 模块，上传时再对更新做 Top-K 稀疏化。服务端保留稠密状态，上下行可使用不同密度，下载掩码可逐轮变化。它在四个图像 / 文本任务中，以约 3–10 倍更少的通信达到 dense LoRA 的效用；在某个理想带宽模型下，上行进一步稀疏可使达到 20NewsGroups 70% 准确率的通信时间约减少 16 倍（pp. 2–7）。这些收益不等于端到端训练时间加速。

## 背景、不足与贡献

- **背景（原文）**：LoRA 已减少联邦训练需要交换的参数，但较大适配器或慢速网络仍可能成为瓶颈，尤其上行较慢（pp. 1–2）。
- **现有方法不足（原文）**：将 centralized sparse adapter pruning 直接搬到 FL，会因冻结权重损害效用；固定掩码限制上下行独立选择；LoRA 相对主干很小，非结构化稀疏还依赖专门计算支持，冻结小适配器未必带来可观计算收益（pp. 2、4–5）。
- **贡献（原文）**：提出只在通信时稀疏化的 FLASC；比较通信、数据异质性、系统异质性、DP 情况；提供可复现实验代码（pp. 2、5–12、19）。

## 方法流程与核心公式

LoRA 表示  $`W=W_0+BA`$ ，冻结主干  $`W_0`$ ； $`B\in\mathbb R^{d\times r}`$ 、 $`A\in\mathbb R^{r\times k}`$ ； $`r`$  为 LoRA 秩。将所有层的  $`A,B`$  展平并拼接为向量  $`P`$ ，使用**全局**而非逐层 Top-K 掩码（pp. 4–5）。

定义  $`\mathrm{Top}_d(P)`$  保留幅度最高的  $`d`$  比例元素。 $`d_{\mathrm{down}}`$  与  $`d_{\mathrm{up}}`$  为保留的**密度**，不是删去比例。第  $`t`$  轮（按 p. 5 算法 1 统一记号）：

$$
P_i^t=P^t\odot M_{\mathrm{down}}^t,
\quad
M_{\mathrm{down}}^t=\mathrm{Top}_{d_{\mathrm{down}}}(P^t),
$$

$$
P_i^{t\prime}=\mathrm{LocalSGD}(P_i^t,D_i),
\quad
\Delta P_i^t=P_i^t-P_i^{t\prime},
\quad
\widetilde{\Delta P_i^t}=\Delta P_i^t\odot
\mathrm{Top}_{d_{\mathrm{up}}}(\Delta P_i^t),
$$

$$
g_t=\frac1n\sum_{i=1}^{n}\widetilde{\Delta P_i^t},
\qquad
P^{t+1}=\mathrm{AdamUpdate}(P^t,g_t).
$$

 $`D_i`$  为客户端数据， $`n`$  为本轮参与客户端数， $`\odot`$  为逐元素乘法。注意算法的 delta 是“下载权重减本地训练后权重”，作为 server Adam 的 pseudo-gradient；若反过来定义 delta，服务端符号也必须相应变化（p. 5；附录 A，p. 18）。

每轮顺序是：服务端对稠密 LoRA 状态选下载掩码 → 抽样客户端 → 客户端以稀疏值初始化并**更新所有适配器参数** → 计算 delta → 独立选择上传掩码 → FedAdam 聚合 → 保持稠密服务端状态。没有把被置零参数永久冻结，也没有在算法 1 中给出 error-feedback 状态；不要自行补入（pp. 3–5）。

## 实验设置与指标

所有结果来自离线 / 单机模拟 federated training，不是实际多设备网络测量（p. 19）。

| 数据集 | 任务 / 指标 | 划分、客户端规模 | 模型与主要条件 |
| --- | --- | --- | --- |
| CIFAR10 | 图像分类 / Accuracy | Dirichlet，500 clients，50K examples，10 类 | ViT-B-16，85M 参数；224×224 图像 |
| 20NewsGroups | 序列分类 / Accuracy | Dirichlet，350 clients，20K examples，20 类 | GPT2-Small，124M 参数；sequence length 128 |
| Reddit | next-token prediction / Accuracy | 按用户自然划分，32K clients，1.1M examples | GPT2-Small；sequence length 25 |
| FLAIR | 图像多标签任务 / F1 | 按用户自然划分，41K clients，345K examples，17 coarse labels | ViT-B-16；表 1 将任务写为 Object Detection，本笔记保留原标签，不推断检测框 mAP |

上述数据来自 pp. 5–6，表 1。FLAIR 每轮 200 clients、2 local epochs、最多 5000 rounds；其他三个数据集每轮 10 clients、1 local epoch、最多 200 rounds；local batch size 都为 16（p. 6）。模型主干预先在客户端可用，此初始化分发成本不等于每轮 LoRA 通信成本（p. 4）。

对比：Dense LoRA、Adapter LTH、SparseAdapter；冻结消融还包括 Federated Select；系统异质性比较 Heterogeneous LoRA；隐私比较 full fine-tuning 与 FFA-LoRA。服务端 FedAdam，客户端 SGD（momentum 0.9），多个 server / client learning rate 配置搜索， $`\beta_1=0.9,\beta_2=0.999`$ （pp. 6–11、19–20）。

## 主要定量结果及统计口径

| 实验 | 原文结果 | 适用范围与出处 |
| --- | --- | --- |
| 四任务通信曲线 | FLASC 以 3–10× 更少通信匹配 LoRA 效用 |  $`r=16`$ ，FLASC / SparseAdapter 密度 1/4；3 seeds，阴影为 min / mean / max，不是置信区间；图 2、pp. 6–7 |
| 20NewsGroups 达到 70% Accuracy | 对称 1/4 密度约 4× 更少通信时间；上行密度 1/64 时约 16× 更快通信 | 下行密度 1/4，上行 / 下行速度比 1、1/4、1/16；理想无噪声固定带宽模型，仅传输时间；图 3、p. 7 |
| 强标签异质性 20NewsGroups |  $`r=16`$  约 75%，full FT 与较小秩约 70%；同通信成本下稀疏通信保留较高秩更有利 | Dirichlet  $`\alpha=0.01`$ ；近似读数来自作者正文，不能补成精确小数；图 5、pp. 8–9 |
| FLAIR，无噪声 | full FT / LoRA / FLASC / FFA-LoRA：78.70 / 78.28 / 78.18 / 77.79 F1 | 图 7，p. 10 |
| FLAIR， $`\epsilon=2`$  | full FT / LoRA / FLASC / FFA-LoRA：67.85 / 68.96 / 68.33 / 66.05 F1 |  $`\sigma=0.34`$ ，图 7，p. 10；FLASC 与 FFA 均在 LoRA 基础上减少约 50% 通信 |

图 2 的不同任务准确率不能相互排名；通信时间的 16× 数字也不能当作实测训练总时间。稀疏索引编码、协议开销、实际网络丢包和端到端 wall-clock 的完整成本没有在上传版中量化（整理者归纳）。

## 隐私实验必须区分的条件

论文使用 **global / central client-level DP-FedAdam**：服务器裁剪、聚合客户端更新，再加入噪声；邻接数据集差异为一个客户端的数据集合加入 / 移除（pp. 10–11）。上传件讨论 FFA-LoRA 在客户端执行 DP-SGD 的不同设置，不能只按相同  $`\epsilon`$  直接比较两个论文。

更重要的是，报告的 privacy budget 使用**较大模拟 cohort**，实际每轮训练样本数较少：Reddit 实际 10 clients、模拟 1000；FLAIR 实际 200、模拟 5000（pp. 11、20，B.4）。噪声缩放用于可行的实验模拟，报告预算不是对实际小 cohort 部署的直接同条件保证。

Reddit 的  $`\sigma\in\{0,0.013,0.072,0.58\}`$ ， $`C=10^{-4}`$ ，client learning rate  $`5\times10^{-4}`$ ；FLAIR 的  $`\sigma\in\{0,0.34\}`$ ， $`C=5\times10^{-3}`$ ，client learning rate  $`10^{-2}`$ （p. 20）。完整  $`\delta`$ 、accountant 版本和全部训练结果 checkpoint 在上传 PDF 中未明确提供。

## 消融、适用条件与局限性

- **冻结消融（原文）**：全局固定 SparseAdapter 掩码与允许服务端变掩码但客户端仍冻结的 Federated Select，均弱于允许稠密本地训练的 FLASC（pp. 7–8，图 4）。
- **秩、异质性与密度（原文）**：比较  $`r\in\{1,4,16\}`$  与密度 1/4、1/16； $`\alpha\in\{100,1,0.01\}`$ ；秩与通信稀疏度应共同考虑，不能把所有任务都降到最低秩（pp. 8–9、20）。
- **系统异质性（原文）**：用 2 / 4 个预算 tier、按 4 的幂设置通信能力；几种方法表现接近，不能宣称 FLASC 每个配置都严格最优（pp. 9–10，图 6）。
- **隐私秩消融（原文）**：Reddit 从秩 1 到 256；较大秩在非私有设置更好，较小秩在带噪设置更有利；冻结并非所有情况下都能提升效用（p. 11，图 8）。
- **适用条件（整理者归纳）**：模型主干已可用、LoRA 本身有效、通信是主要瓶颈，且客户端仍能完成稠密适配器训练。
- **局限性（整理者推断）**：适配器仍需稠密训练和服务端状态；通信收益不自动转为算力 / 内存收益；实验主干仅 ViT-B-16 与 GPT2-Small，未验证 7B / 更大 LLM；DP 设置与系统条件需逐项匹配。
- **作者后续工作**：将 local training time、client availability 等更广泛瓶颈纳入考虑；研究 LoRA 不足时的更大模型联邦微调（p. 12）。

## 官方代码、数据与复现信息

官方代码：[imkevinkuo/flasc](https://github.com/imkevinkuo/flasc)，p. 19 明确提供。当前作者 README 要求 Python 3.10.14、CUDA 11+，使用 PyTorch / Hugging Face Transformers；入口 `train_sparse_lora_dp.py` 与 `train_sparse_lora_het.py`。这是 2026-10-11 核对到的 README 信息，不等于上传版实验的锁定依赖版本。

README 提供 CIFAR10 / 20NewsGroups 自动下载工具，Reddit / FLAIR 的完整数据处理细节仍未在 README 中补齐。复现需保存数据划分、采样种子、模型权重、rank、上下行密度、learning rates、privacy cohort / noise scaling 和稀疏编码方式。PDF p. 19 报告使用 GeForce 1080 Ti “12 GB memory”；这一容量表述待核实，不把它当作最低硬件要求。未运行训练。

## 阅读总结

**原文解决的问题**：在不永久冻结适配器参数的条件下，让 LoRA 适应非对称、低带宽的跨设备联邦通信。

**值得借鉴（整理者归纳）**：针对瓶颈压缩传输表示，同时保持本地训练自由度；独立设计上下行密度；用达到目标效用所需的累计通信衡量方法，而非只比较每轮参数量。若与 FFA-LoRA / AdaLoRA 组合，需重新核查冻结、秩分配和 DP 下的效用，本文没有验证这些组合。

## 单光子 LiDAR 参数

不适用。这里的 224×224 是输入图像预处理尺寸，不能当作探测器阵列；模型通信时间和推理 / 训练速度不等于光子采集时间、重建帧率或探测距离等 LiDAR 参数。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [全文与版本说明](source.md)
