# FedALA-WR: personalized federated learning with adaptive local aggregation and weighted replay

## 文献信息与阅读对象

| 项目 | 记录 |
| --- | --- |
| 完整英文题名 | FedALA-WR: personalized federated learning with adaptive local aggregation and weighted replay |
| 作者，按上传版顺序 | Tinku Singh、Nguyen Khoa、Bhawnesh Kumar、Taehong Kim；保留官方的 Nguyen Khoa 顺序 |
| 正式出版 / 实际阅读 | **Cluster Computing 2026, 29(9), article 580**；上传期刊版 PDF **17 页**，含完整正文和参考文献，无另列附录 |
| 出版日期 | Received 2025-10-28；Revised 2026-05-14；Accepted 2026-07-03；Published online / Version of record **2026-07-24** |
| PDF 文档日期 | Creation / ModDate 为 2026-08-21，详情见 source；不是论文首次发表日期 |
| DOI / 官方记录 | [10.1007/s10586-026-06366-5](https://doi.org/10.1007/s10586-026-06366-5)；[Springer](https://link.springer.com/article/10.1007/s10586-026-06366-5)；[出版社提交的 Crossref](https://api.crossref.org/works/10.1007/s10586-026-06366-5) |
| 许可 / PDF 入库 | © The Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature 2026；未确认第三方公开再分发许可，仓库保留来源 / 笔记 / 引用，**不复制 paper.pdf** |
| 关联前作 | 本文扩展 FedALA（AAAI 2023，Jianqing Zhang 等），两篇是不同作者 / 不同论文，不是同一篇的预印本与正式版 |
| 引用 | [citation.bib](citation.bib) 的 `singh2026fedalawr_cluster` 为阅读期刊版；`zhang2023fedala_aaai` 仅用于核对前作方法 / 正式书目，不计作另一个已读上传件 |
| 核对日期 / 范围 | 2026-10-12；阅读全文 17 页，以下均用上传 **PDF 物理页码**。未运行作者训练或复现实验 |

以下区分**原文报告**、**整理者归纳**、**整理者计算**、**代码静态观察**和**待核实**。出版社网页是 subscription preview；全文来自用户附件，未从订阅入口获取正式 PDF 做字节比对，不宣称官方服务器文件与附件相同。

## 摘要

**整理者归纳，PDF pp. 1–2、5–9。** 本文研究 personalized federated learning（pFL）的 non-IID 数据异质性与 intra-round forgetting：客户端在同一通信轮中依次训练本地 mini-batch，早期 batch 的知识可能被后续更新削弱。FedALA-WR 使用客户端记忆缓冲区，选取预测熵较高的样本，配合当前数据 / replay 的加权目标；服务端按逐层相似度计算 attention 权重聚合客户端模型，并讨论提前结束全局训练。

实验是 4-layer CNN 的图像分类和单机联邦模拟，没有 LLM、LoRA、梯度 AutoEncoder 或 DP accountant。相对 FedALA 的准确率提升多数较小，主要是稳定性和训练轮数方面的动机；不能把不增加 replay 消息的说法写成“已压缩模型更新”。已核实作者代码，但其 replay 梯度、相似度符号和停止实现与正文有关键差异，见后文。

## 背景、已有方法不足与贡献

**原文，pp. 1–5。** 全局统一模型在异质客户端上的局部效用有限。pFL 可通过 meta-learning、regularization、共享 / 私有参数划分或 personalized aggregation 改善局部适配，但聚合机制未必处理轮内的 sequential mini-batch forgetting。本文将局部回放稳定性与轮末聚合质量联系起来，定位为 federated optimization extension，而不是提出新的 continual-learning 原理（pp. 2、16）。

**原文贡献，p. 2：** 熵选样保留容易遗忘的样本；一个 $`\lambda`$ 统一控制回放采样比例和 loss 权重；逐层 similarity 比全模型 flattened similarity 更细；在不同数据集、异质性和客户端规模下评估精度、遗忘与收敛。

**整理者限定：** p. 10 的数据是固定 private datasets 的非 IID 划分，不是显式逐轮引入新类别 / 新任务的 continual FL。轮内遗忘、轮间 model drift、长期 class-incremental forgetting 不能互相代替。服务端相似度是参数关系的 heuristic，尚没有定义能保证“信息价值”“鲁棒性”或真实 semantic representation 一致性的统计量。

### FedALA 前作的机制必须单独核对

本文 p. 2 和 p. 4 将 FedALA 概括为服务端 cosine-update attention；但 p. 3 又正确提及**客户端学 element-wise 权重，把下载全局模型和本地模型按本地目标融合**。原 FedALA [AAAI 官方摘要](https://ojs.aaai.org/index.php/AAAI/article/view/26330)及[作者仓库](https://github.com/TsingZ0/FedALA)支持后者：ALA 是训练前客户端初始化模块，而非本文式 (1)–(2) 的同义名称。作者 FedALA-WR 仓库继承的 `clientala.py` / `utils/ALA.py` 也保留客户端 ALA。

因此以下先记录**本文定义的** server attention，再记录代码中的 local ALA；不将前作改写成 cosine-softmax 服务端算法，也不因为保留参数 $`s,p`$ 就认为两个聚合实现相同。论文正文、前作和公开实现的关系需要作者说明。

## 客户端与服务器方法、核心公式

### 一轮训练流程

**原文算法 1，p. 6；细节 pp. 7–9。** 服务端分发全局模型并随机选参与客户端；客户端根据自己的数据更新记忆、构造当前 / replay batch、训练本地模型，发送模型 / 更新；服务端计算 attention 并聚合，必要时 auto-stopping。全局与客户端模型都保留完整 CNN 参数，原文未定义 LoRA 因子、动态秩或压缩 latent。

注意：算法在轮开始先更新 $`M_k^t`$ ，p. 7 式 (5) 则在轮末用当前模型生成下一轮 $`M_k^{t+1}`$ 。哪一轮的 buffer 用哪次权重评分、第一轮 buffer 怎样填充、一次参与跨间隔客户端如何维护状态，需明确执行顺序，不能擅选一种填补。

### 熵选样、batch 比例与回放目标

原式 (4)–(7)，p. 7。客户端 k 的 C 类预测熵：

$$
H(x)=-\sum_{c=1}^{C}p(c\mid x;\Phi_k^t)\log p(c\mid x;\Phi_k^t).
$$

$$
M_k^{t+1}=\mathrm{Top}_{x\in D_k}\left(H(x),\lvert M_k\rvert\right).
$$

按熵选本地数据 $`D_k`$ 中最高的 $`\lvert M_k\rvert`$ 个样本。熵衡量预测不确定性，不直接衡量过去学过的类别、遗忘程度或真实标签价值。式 (5) 的候选集是当前 $`D_k`$ ，没有明确定义旧 buffer 与持续新增数据的 union / replacement；固定本地数据下 buffer 可能重复选取同一批难样本。

原文 batch 构成与权重：

$$
B_k=B_k^{\mathrm{new}}\cup B_k^{\mathrm{replay}},\qquad
\lvert B_k^{\mathrm{new}}\rvert=(1-\lambda)\lvert B_k\rvert,\qquad
\lvert B_k^{\mathrm{replay}}\rvert=\lambda\lvert B_k\rvert.
$$

$$
\mathcal L_k^t=(1-\lambda)\mathcal L_{\mathrm{task}}(\Phi_k^t;D_k)+\lambda\mathcal L_{\mathrm{replay}}(\Phi_k^t;M_k^t).
$$

两项均用 supervised cross-entropy， $`\lambda\in[0,1]`$ 。**整理者归纳：** 这是改变本地优化分布的 mixture objective；对 mixture unbiased 不代表对原始本地 uniform risk unbiased，更不代表全局非 IID 客户端目标无偏。

**需保留的细节差异：**

- p. 7 前半按比例组成每个 batch，同页又称两个 loss 在 equal-size batches 上算；当 batch size 10、 $`\lambda=0.05`$ 时公式给出 replay 样本数 0.5，整数取整 / 跨 batch 随机规则未列。
- pp. 6–8 说明 replay loss **once per communication round**，并在 task updates 后对轮末解做 corrective regularizer；算法 / mixture mini-batch 描述未给该纠正步骤的具体 optimizer update。
- 若分别对 current / replay 子批求平均再按 $`\lambda`$ 加权，才能直接对应给定 mixture；若已按混合比例抽样又不恰当重复加权，会改变目标。本文需补齐 estimator 和归一化，不能仅凭“单一 lambda”断言实现正确。
- 数据可同时属于 $`D_k`$ 和 buffer；union 是概念表达，不保证样本去重，实际抽样 / 重复次数会改变权重。

### 逐层 similarity、attention 与聚合

**原文 pp. 4、8。** 前置式 (1)–(2) 用 local update 与平均 update 的 cosine-softmax；实际方法式 (8) 则比较客户端**参数**和上一轮全局**参数**，并减去逐层 L2 距离。保留区别，不能把这两种 cosine 的对象当作相同：

$$
\mathrm{sim}(\Phi_k^t,\Phi^{t-1})=
\sum_{l=1}^{L}\left[\mathrm{cos}(\Phi_k^{t(l)},\Phi^{t-1(l)})-
\left\lVert\Phi_k^{t(l)}-\Phi^{t-1(l)}\right\rVert_2\right].
$$

$$
a_k^t=\frac{\exp\left(\gamma\mathrm{sim}(\Phi_k^t,\Phi^{t-1})\right)}{
\sum_{j\in\mathcal K_t}\exp\left(\gamma\mathrm{sim}(\Phi_j^t,\Phi^{t-1})\right)}.
$$

$$
\Phi^t=\sum_{k\in\mathcal K_t}a_k^t\Phi_k^t.
$$

以上分别对应原式 (8)–(10)。式 (8) 的距离是 **L2 norm**，不是 squared norm；p. 8 已目视核对。 $`\gamma=1.0`$ 在全部实验固定；原文叫 temperature，但位于指数乘法位置，数学效果更接近 inverse temperature，数值越大越尖锐。不同层 norm 的大小 / 参数尺度可能主导 similarity，文中未列归一化、层权重或 zero-vector cosine 的处理；attention-weighted 平均也不等同按客户端样本量加权的 FedAvg。

正文有 $`\Phi^t`$ / $`\Phi^{t+1}`$ 、model / update 的轮号切换（pp. 4、6、8）。本笔记按原式保留，执行时须统一“下载、训练、聚合”的时间索引，不能静默把所有式子改写成另一协议。

### 停止、优化论证与隐私符号

**原文 p. 9：** 服务端观察相邻全局模型变化 / similarity threshold，稳定后结束通信。没有给出阈值、patience、归一化或伪代码。pp. 13–15 又说 FedALA 与 WR 都用 auto-break，需区分共同框架功能与新方法贡献。

原式 (11)–(12) 假设 L-smooth、本地 stochastic gradient 方差有界：

$$
\mathbb E\left[\left\lVert g_k-\nabla\widetilde F_k(w)\right\rVert^2\right]\leq\sigma^2,
\qquad \mathbb E[g_k]=\nabla\widetilde F_k(w).
$$

这只是 mixture SGD 的局部解释；作者明确说**完整 non-IID 联邦收敛证明不在本文范围内**。没有列 attention 自适应引入偏差的界、学习率 / 客户端采样约束或 global convergence rate。 $`\sigma`$ 表示梯度方差上界，不是 DP noise multiplier。所有结果的隐私预算 $`\epsilon,\delta`$ **不适用 / 未提供**。

## 实验设置

**原文报告，pp. 9–11。**

| 项目 | 条件 |
| --- | --- |
| 模型 / 任务 | 4-layer CNN，MNIST / CIFAR-10 / CIFAR-100 / Tiny-ImageNet 分类；没有 7B LLM / LoRA |
| 数据划分 | 原 train 与 test 合并，再按客户端分配，每客户端 75% train / 25% private test；不是官方原 test split 的统一全局评估 |
| Pathological | MNIST / CIFAR-10 每客户端两个类，CIFAR-100 每客户端十个类；原文“non-overlapping class distributions”与 20 客户端设置下可重复类别的关系需说明，不能推成所有客户端类别两两不交 |
| Practical | Dirichlet $`\beta=0.10`$ 为主要默认；HPO 用 0.05；Tiny-ImageNet 异质性比较 0.01 / 0.5；更小 beta 是更强类分布偏斜 |
| 客户端 / 本地训练 | 主表 20 clients，扩展 50 / 100；mini-batch 10；每轮 1 local epoch；CNN 学习率 0.005，MNIST0.1；正文未列完整参与率 / dropout 配置 |
| 轮数 / 停止 | 最多 1000 轮，计时 / 曲线启用 auto-break；实际每组停止轮数未完整给出 |
| HPO | memory size BS=10 / 20 / 50 / 100；lambda=0.05 / 0.10 / 0.20；s / p 保留 FedALA default，正文未直接列数值；gamma=1.0 |
| 指标 / 重复 | private local test accuracy 的平均；pFL 使用 best local models；五次重复报告 mean±std，种子列表未给；图 4 又称 global accuracy，需要核对是否同一聚合口径 |
| 硬件 / 环境 | 单节点：2×RTX3080（各 10GiB）、Threadripper3960X24-core、251GiB RAM；Ubuntu24.04.1、Python3.11.11、PyTorch2.0.1、CUDA11.7 |
| 计时 / 通信边界 | wall-clock 含计算和调度，不含 wide-area network latency；参数计数不是字节或完整协议成本；replay 保存在客户端 |
| 基线 | FedAvg、FedProx、SCAFFOLD、FedFomo、FedAMP、FedPHP、APPLE、FedALA；不直接与仓库联邦 LLM / DP 方法排序 |

数据划分用原 train+test 之后重新切分，在训练 / private test 样本不重叠时不能直接判定泄漏；但它与标准官方 test benchmark 的可比性不同。HPO 是否另设 validation、best local models 是否由同一 private test 选取、计时是否五次相同停止规则，均需补充；不能将 private test 最优分数当新客户端 / 独立最终测试表现。

## 主要结果与适用边界

### 相对 FedALA 的增量效用

前三数值列为**原文报告**，末列为**整理者计算**；p. 12 表 3，4-layer CNN、20 clients、最多 1000 轮、无 DP；±为五次重复的 std，不是置信区间。选择 FedAvg 和直接前作作为必要对照，不复制全套基线表。

| 数据集 / non-IID | FedAvg 准确率% | FedALA 准确率% | FedALA-WR 准确率% | WR−FedALA，百分点 |
| --- | --- | --- | --- | --- |
| MNIST / pathological | 97.90±0.06 | 99.60±0.02 | 99.88±0.01 | +0.28 |
| CIFAR-10 / pathological | 60.87±0.26 | 91.46±0.15 | 91.83±0.11 | +0.37 |
| CIFAR-100 / pathological | 28.67±0.35 | 67.25±0.36 | 68.02±0.35 | +0.77 |
| CIFAR-10 / Dir(0.10) | 62.37±0.51 | 91.25±0.14 | 91.40±0.25 | +0.15 |
| CIFAR-100 / Dir(0.10) | 32.52±0.39 | 56.99±0.19 | 57.53±0.15 | +0.54 |
| Tiny-ImageNet / Dir(0.10) | 17.77±0.26 | 44.70±0.52 | 45.33±0.19 | +0.63 |

在这些列中 WR 的点估计最高，但没有配对 seed 结果 / 显著性检验，尤其 CIFAR-10 practical 的 0.15 百分点不能单独证明统计显著。相对 FedAvg 的大差距包含 pFL / 个性化评价设定，不全来自新 replay 模块。

**正文 / 表格错位需保留：** pp. 12–13 写 FedAvg CIFAR-100 practical 为 28.67，而表 3 的 practical 实为 32.52，28.67 属于 pathological；写 FedALA / WR 的 CIFAR-10 practical 为 91.46 / 91.83，而表格 practical 为 91.25 / 91.40。笔记依据明确表头分列，不将文字中的移列数值换进另一实验。

### 客户端规模与异质性

**原文报告，p. 13 表 4；4-layer CNN、无 DP、均值±std；末列为整理者计算。**

| 配置 | FedALA 准确率% | FedALA-WR 准确率% | 差，百分点 |
| --- | --- | --- | --- |
| CIFAR-100 Dir(0.10)，20 clients | 56.99±0.19 | 57.53±0.15 | +0.54 |
| 同上，50 clients | 58.51±0.57 | 58.91±0.48 | +0.40 |
| 同上，100 clients | 57.21±0.46 | 57.46±0.53 | +0.25 |
| Tiny-ImageNet Dir(0.01) | 58.70±0.40 | 59.01±0.52 | +0.31 |
| Tiny-ImageNet Dir(0.5) | 29.81±0.12 | 30.58±0.34 | +0.77 |

原文在“Scalability”段写 FedALA 56.99%–57.21%，未包括表中 50 客户端 58.51%；应保留全表结果。强异质性下 private-test 分数反而更高可与客户端局部类别更集中 / 个性化目标有关，不能直接写成跨客户端泛化更强或消除 non-IID。100 clients 的评估不等于异构设备实测、持续新客户端泛化或大规模公网扩展验证。

## 消融、遗忘指标与收敛

**原文报告，pp. 10–12 表 1–2、图 3。** 表 1 是 Dir(0.05)、1000 轮下的 BS / lambda 网格，无 error bar：CIFAR-10 最优 86.30%（BS10、lambda0.05）；CIFAR-10057.78%（BS100、0.10）；Tiny-ImageNet45.80%（BS100、0.05）。这些分数不能与表 3 Dir(0.10) 当同一条件比较；正文未明确每个主表是否采用对应网格最优、参与率和全部 seed。

| 检查 | 原文报告 / 解释 | 出处 |
| --- | --- | --- |
| Buffer 选样 | CIFAR-100、Dir(0.10)、20 clients：random replay loss increase0.173、accuracy66.41±0.47%；entropy replay0.142、68.02±0.35% | p.11 表 2；68.02 对应表 3 的 pathological 列，却表 2 标 Dir(0.10)，与表 3 该列 57.53 不一致，需原配置解释 |
| 遗忘度量 | early mini-batch 刚处理后 loss，与同轮结束后的同批 loss 之差，按客户端 / 轮平均；越低越少遗忘 | p.12；不是 task-incremental forgetting accuracy 或 backward transfer |
| 图 3 | 对前 50 个 local mini-batches 看轮末 loss，显示 WR 更平稳 | p.11 图 3；没有完整数据 / uncertainty，勿从曲线读额外精确小数 |
| lambda=0 | 原文说禁用 replay 恢复 FedALA-style training | p.11；表 1 列只有 0.05 / 0.10 / 0.20，没有报告 0 的完整网格结果；服务端 attention 又已改变，不等于严格恢复原 FedALA |
| 组件消融边界 | 改 buffer / lossweight 和 random vsentropy，不含完整客户端 replay / server similarity 独立 factorial 对照 | pp.11–12；固定 gamma 不意味着排除聚合改变的影响 |
| 收敛 | 图 4 展示多个数据集的 accuracy 轨迹，启用 auto-break，WR 更早停止 | pp.13–14；未列每组实际轮数、完整停止参数；单机模拟曲线不能推出真实链路时间 |

p.12 的文字说表 2 含 FedAvg / FedALA / WR 遗忘对照，但实际表 2 只有 random / entropy 两种 WR buffer。图 3 确有 FedAvg / FedALA 对照，不能替表 2 补不存在的数字。

## 计算、通信与内存口径

**原文报告，p.15 表 5；Tiny-ImageNet、4-layer CNN、单节点 2GPU、启用 auto-break、无 DP。** $`T`$ 为总轮数， $`E`$ 为 localepochs， $`\Sigma`$ 为传输参数个数，exh 为初始 ALA 额外训练次数；下表通信项是整个 T 尺度的参数计数，而非“每轮 T×Σ”。

| 方法 | 训练 / local aggregation 计数 | 上行 / 下行参数计数 | 每 trial 分钟，原文 |
| --- | --- | --- | --- |
| FedAvg | TE / 0 | TΣ / TΣ | 194.71±0.454 |
| FedAMP | TE / T | TΣ / TΣ | 147.20±0.207 |
| FedALA | E(2T−1)+exh / 2T+exh−1 | TΣ / TΣ | 182.43±5.340 |
| FedALA-WR | E(2T−1)+exh / 2T+exh−1 | TΣ / TΣ | 175.56±5.340 |

**整理者计算：** 相对 FedALA，WR 快 6.87min，比例 $`(182.43-175.56)/182.43\times100\%=3.77\%`$ 。同表 FedAMP147.20min 更短，因此 WR 不是全部基线中最快；两个方法 std 均 5.340，未提供配对检验，不将 3.77%写成确定或显著收益。

**通信与计算边界：**

- Replay 样本不发给服务端，所以按模型消息格式不额外增加 samplepayload；仍上下行完整 CNN 参数。累计字节还需实际停止轮数、参与客户端数、位宽、协议和数据结构，本文没完整报告。
- 表 5 相同 ALA / WR 理论计数并未逐项表达熵推理 / 排序 / bufferloss 的 FLOPs；wall-clock 含这些操作和调度，二者不要求线性比例。不能用计数相同判定新增计算为零。
- 表 5 SCAFFOLD 上行写 T×E，与“Communication(params)”的参数单位不一致；未用该疑点列做精确字节比较。
- p.15 说 buffer 仅存 raw samples，BS10–100 约数百 KB 到 1–2MB；具体 dtype、resolution、labels 和 tensoroverhead 未列。**条件化整理者计算：** 若 100 张 Tiny-ImageNet64×64RGB 为 float32，仅像素 $`100\times64\times64\times3\times4=4{,}915{,}200`$ bytes（约 4.69MiB）；uint8 则约 1.17MiB。原文上界不能不注明存储类型直接迁移到公开代码 tensorbuffer 或所有 edge 设备。
- 单节点 GPU 调度时间未包含 wide-area latency，不是通信带宽实测或可直接部署到医疗 / IoT 的端到端计时。

## 隐私分析与局限

**原文范围，pp.1、15–16；整理者归纳：** 未共享 rawdata 是 FL 设计，未给出 DP / 加密 / secureaggregation。buffer 在客户端保留原始输入和标签，熵筛选不去标识化；服务端仍获取数据相关完整模型 / updates。replay 改变 record 被重复使用的次数，若另加 DP-SGD，需要重新核算采样、重复访问、HPO / 停止和最终发布；不能直接沿用 CG / DR 的预算。

| 局限 / 待核实 | 证据与影响 |
| --- | --- |
| 论文方法内部不一致 | FedALA localALA 与 serverattention 的混写；buffer 更新轮号；mini-batch 混合与 round-end 纠正；model / update 与索引切换；不能补造完整协议 |
| 理论范围 | p.9 只有 mixtureSGD 假设，作者明确没有 non-IID 全局收敛证明；不提供 DP 或拜占庭鲁棒性证明 |
| 评估选择 | private localtest / bestmodels、HPO validation 和图 4globalaccuracy 口径不够清楚；没有 unseenclient 独立测试 |
| 配置 / 结果冲突 | 表 2 的 68.02 在 Dir0.1 下与表 3 的 57.53 不同；正文多处引用 pathological 数字为 practical；保留全部出处，待配置 / 日志核对 |
| 不确定性 | 有五次重复 mean±std 但 seed / pairedlogs 不全；微小差值不自动显著；HPO 表缺 std |
| 数据 / 模型 / 部署 | 静态 non-IID、浅 CNN、最多 100clients、单机 GPU；无 LLM、真实公网设备、连续任务序列或攻击验证 |
| 作者后续方向 | p.16：adversarial / poisoning defense、continualFL、distillation、quantization / sparsification、真实 healthcare / IoT；均是未来工作，不能写成已实现 |

## 官方代码与复现审计

**已核实，2026-10-12：** PDF p.16 与 Springer“Code availability”都指向 [tinku1984/FedALA_WR](https://github.com/tinku1984/FedALA_WR)。公开快照 [90b5038](https://github.com/tinku1984/FedALA_WR/commit/90b5038a4b48220d0e4912e0ef9e37a7b145fd09)，2025-10-25；论文投稿前的公开代码日期不表示已经覆盖 2026 修订的全部定义。根许可为 GPL-2.0，部分继承文件 header 为 GPLv2-or-later；README 说将来改 Apache-2.0，不把承诺当当前许可。代码许可不授权复制 SpringerPDF。

读取 README、`clientala_pp.py` / `serverala_pp.py`、继承 clientALA、ALA 模块、serverbase、main 和配置，仅作**静态审计**。入口名为 **FedALA_PP / FedALA++**，并非新增同名 FedALA-WR 分支；README 主要保留 PFLlib 说明，不能把其通用示例当本文全实验复现指令。

| 项目 | 公开代码观察 | 与论文关系 / 影响 |
| --- | --- | --- |
| 回放梯度 | `compute_replay_loss`返回平均 loss 后 **detach()**；train 在 localepochs 循环前算一次常量，每个 currentbatch 的 loss 加该常量 | p.7 式(7)的 replay 梯度及 p.8“轮末纠正”未由此实现；不是每轮完整 replay 优化 |
| 采样比例 | trainloader 仍是 currentdata；没有按 lambda 构造 new/replay 混合 mini-batch | 与 p.7 式(6)不一致；buffer 用于常量 loss 而非该混合抽样路径 |
| 学习率 | 子类重新建立 SGD、硬编码 lr0.01 | 与 p.10 CNN0.005 / MNIST0.1 不同；须确认实际 runoverride / 对应版本 |
| 熵 buffer | train 结束后计算本地 softmaxentropy，按降序取 buffer_size，存 CPU 样本 / 标签 | 与 p.7 轮末填下一轮 buffer 一致；与算法 1 先填当前 buffer 的叙述不同 |
| Similarity 距离符号 | `compute_update_similarity`对每个 parameter tensor 累加 **cosine + norm** | 原式(8)为 cosine **− norm**；公开快照反而给较远参数更大分数的潜在效应，需修订版本核对 |
| Attention / 上传内容 | softmax similarities；`get_significant_updates(top_percent=100)`返回全部 modelparameters | 没有实现 Fisher 信息选择 / 稀疏传输；相关 docstring 不能替代执行逻辑；temperature 有效为 1 |
| ClientALA 继承 | 下载全局模型后调用 learned element-wise ALA 初始化，高层按 localobjective 学习权重 | 与原 FedALA 客户端机制相符，不等同正文式(1)的 servercosine 定义；个性化共享 / 私有边界未在本文完整公式化 |
| 停止 | `serverala_pp`调用`check_done(acc_lss=[rs_test_acc], top_cnt=100)`；检查 besttestaccuracy 多久未提升 | 与 p.9“相邻全局模型变化阈值”不同；stop 依赖 testseries，需独立 validation 协议 |
| 默认参数 / 搜索 | main 的 s=80、p=2、memorydefaults 等来自代码；另有 outerlambda 搜索 / testaccuracy 选择逻辑 | 正文未列数值者只能标“代码默认”，不是论文配置已核实；repositoryconfig.yaml 还含不同 FL 策略，不能盲用 |

`detach` 的效果依据 [PyTorch 官方说明](https://docs.pytorch.org/docs/2.14/generated/torch.Tensor.detach.html)：返回张量不在当前梯度图中。**整理者的静态代数推断**：该 train 分支 buffer 非空、replay 值为常量时，模型梯度为

$$
\nabla_{\Phi}\mathcal L_{\mathrm{code}}=(1-\lambda)\nabla_{\Phi}\mathcal L_{\mathrm{task}}.
$$

因此该路径不会从 bufferloss 获得参数梯度，lambda 主要缩放当前 taskgradient。这个结论仅针对已读公开快照和该分支，不证明论文报告用了该版本，也没有运行训练验证准确率。不能因“论文给代码链接”写成“实现与全部公式相符”或“复现成功”。

复现前最需要作者确认：修订论文对应 commit、可微 replay 更新的确切顺序、距离符号、客户端 ALA 和 attention 是否同时启用、local / globaltest 定义、data splits、HPO validation、实际停止轮数、全参数 / 位宽通信账本与 seed 日志。本文公开代码未在本仓库执行或修改，未下载数据 / 权重、测时或跑攻击。

## 与仓库其他论文的关系

**有文献依据的整理者比较，不跨条件排名。**

| 对照 | 关系与差异 |
| --- | --- |
| [CG-FedLLM](../2025-wu-cg-fedllm/notes.md) / [DR-Encoder](../2024-wu-dr-encoder/notes.md) | 两者重点是 LoRA 因子 / 梯度的传输表示、压缩器先验和 DP 流程（CGpp.4–6、DRpp.3–6）；本文 pp.6–9 优化客户端训练样本 / 加权目标并聚合完整 CNN 模型。Replaybuffer 不是 TGAP 真实梯度库或 DR 合成梯度，entropy 选样不提供隐私 accountant |
| [FFA-LoRA](../2024-sun-ffa-lora/notes.md) | FFA 通过共享冻结 A 因子解决双因子分别平均的聚合交叉项（其 pp.4–6）；本文 attention 只是给模型 / update 加权，不自动解决双因子乘积的代数问题。若迁移到 LoRA 须决定聚合对象，而非直接给 A/B 都套 attention |
| [FLASC](../2024-kuo-flasc/notes.md) | FLASC 使 localdenseLoRA 训练与上下行 Top-K 传输分离（其 pp.3–5）；本文 p.15 每轮仍传完整参数，replay 不增加消息与 sparsecommunication 是不同机制。本文 p.16 把 quantization / sparsification 列 futurework |
| [PowerSGD+](../2025-xie-powersgd-plus/notes.md) | PowerSGD+同步 worker 共同投影基底、EF 与周期 SVD 控制梯度压缩残差 / MSGD 收敛（其 pp.3–8）；本文浅 CNNpFL 无低秩通信收敛证明，auto-stop 也不是该 safeguard |
| [AdaLoRA](../2023-zhang-adalora/notes.md) / [SVD-LLM](../2025-wang-svd-llm/notes.md) / [ISER](../2026-park-iser/notes.md) | 分别优化适配容量、主干权重、每实例图像 codec 适配与码流。本篇 memorycapacity 是样本数，不是 rankbudget；其 attention 参数不是 AutoEncoderdecoder 或 SVD-LoRA |

**未验证研究设想：** 可研究在联邦 LoRA 本地训练中加入可微 replay，与 FFA 固定基底或 FLASC 稀疏传输组合。但需要新的 LLM 任务、显存 / 通信 / DP 成本分析，保护 buffer 访问和数据相关 stop / HPO，并解决非 IID 客户端与 LoRA 方向聚合；本文没有报告这些组合。不能引用其 CNN privateaccuracy 为组合有效的证据。

## 阅读总结

本篇提供轮内遗忘与本地样本回放的阅读视角，提示“压缩通信”与“改善客户端优化”是两个可分别评估的轴。可借鉴的是明确测量早期 batch 到轮末的 lossincrease；可复现结论的关键障碍是论文 / 代码不同步及评估协议不全。对增量收益应保持小差值、五次 std 和单机条件，而非无条件领先结论。

## 单光子 LiDAR 参数

探测器、阵列、距离、速度、SNR/SBR、每像素光子数、采集时间、LiDAR 重建帧率、空间分辨率和定位误差均**不适用**。分类图像尺寸、buffer 样本数、GPU 分钟数与预测熵不能替代这些物理量。

[来源 / 许可](source.md) · [BibTeX](citation.bib) · [跨论文比较](../../comparison.md) · [返回总览](../../README.md)
