# You Only Communicate Once: One-shot Federated Low-Rank Adaptation of MLLM

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 完整题名 | You Only Communicate Once: One-shot Federated Low-Rank Adaptation of MLLM |
| 完整作者 | Binqian Xu, Haiyang Mei, Zechen Bai, Jinjin Gong, Rui Yan, Guo-Sen Xie, Yazhou Yao, Basura Fernando, Xiangbo Shu（上传PDF p.1；proceedings将同一作者拼为Guosen Xie） |
| 实际阅读版本 | 用户上传32页NeurIPS 2025会议排版 /camera-ready版本；首页标39th Conference on Neural Information Processing Systems。正文pp.1–10、参考文献pp.10–14、checklist pp.15–21、附录pp.22–32；PDF创建日期2025-10-06。不把创建日期当作正式发表日 |
| 正式出版 | Advances in Neural Information Processing Systems 38 Main Conference（NeurIPS 2025），Main Conference Track，2025；官方proceedings核对题名、九作者和DOI |
| 正式DOI | [10.52202/085713-2060](https://doi.org/10.52202/085713-2060) |
| 官方来源 | [NeurIPS论文页](https://papers.nips.cc/paper_files/paper/2025/hash/58e6c003c9fb3992265005ff6aef1913-Abstract-Conference.html)；[官方会议PDF](https://papers.neurips.cc/paper_files/paper/2025/file/58e6c003c9fb3992265005ff6aef1913-Paper-Conference.pdf) |
| 引用与许可 | [citation.bib](citation.bib)；[source.md](source.md)；尚未核实明确覆盖上传32页版本的第三方CC再分发许可，公开目录只保存全文链接 |

已读全部32页，包括参考文献、完整checklist和A–I附录，并视觉核对首页、关键公式 /结果 /附录表。以下均为上传件物理页码。元数据核对日期2026-10-13；不把官方会议PDF可下载当作第三方再分发授权，不声称与上传件做过字节匹配。

## 摘要

YOCO 研究无需服务器额外数据或生成模型、只在本地训练后一次上传适配器的MLLM联邦LoRA。方法从冻结预训练权重的SVD获得共同A/B初始化，将B的符号约束到初始方向，让A经L1正则保留客户端特征；服务器对A做PCA坐标加权重建、对B用普通聚合。默认只训练最后一层q_proj、rank8，每个客户端10epochs。论文按“轮数×层数×LoRA模块数”的归一化通信规模称成本约为多轮FL的0.03%，且在部分CrisisMMD /医学场景有效（pp.5–9）。完整PCA版本并非每个表格单元格都优于one-shot基线；必须同时读各变体、聚合器和数据条件。

## 背景、不足与贡献

- **问题（pp.1–2）**：多轮联邦微调仍有通信负担；无聚合后的显式全局监督时，本地非IID训练容易偏向私有数据。
- **原文对照（pp.2–3、9–10、22–23）**：作者把需要分块 /轻量聚合器反复沟通的FuseFL /FENS称为pseudo one-shot；YOCO使用预训练初始权重提供implicit global supervision。这是作者采用的严格通信定义，不等于所有领域已有one-shot定义均无效。
- **经验发现（pp.3–5图3–4）**：方向约束比幅度约束干扰小；同时约束A/B过强，约束B并配合共同SVD初始化使B冲突下降、A保留更多自由度。
- **贡献（原文，pp.2、5–6）**：无需额外服务器数据的真正一次聚合；B一致性与A适应性折中；通信预算明确的多轮 /单轮对照。

## 方法流程与核心公式

### 1. 先验初始化

预训练矩阵W的rank-r截断SVD（p.5式(3)）：

$$
W=U\Sigma V^\top,\qquad
A_0=\Sigma_r^{1/2}V_r^\top,\quad B_0=U_r\Sigma_r^{1/2},\quad
B^s=\operatorname{sign}(B_0).
$$

共同初始化给所有客户端相同因子坐标和B的初始符号；B的符号是**低秩因子坐标**的符号，不能直接等同于原矩阵W每个元素的符号。因子正负 /旋转自由度意味着共享坐标很重要。

**复现边界（整理者核查）**：式(3)使B_0A_0等于W的非零截断项。正文说最终LoRA与预训练权重合并，却没有明确写出如何在初始化时从冻结主干减去B_0A_0以保持初始函数不变。不能擅自补入某种PiSSA残差规则；需代码或作者解释核对是否使用、以及alpha/r的缩放补偿。

### 2. 客户端联合训练

任务损失为L_s，原式(4)使用**L2范数比，并非平方L2范数比**（p.6、p.31算法1）：

$$
R_{\rm sign}=\frac{\|\tanh(\gamma B)-B^s\|_2}{\|B^s\|_2+\epsilon},
\qquad R_{\rm sparse}=\lambda\|A\|_1,
\qquad \mathcal L=L_s+R_{\rm sign}+R_{\rm sparse}.
$$

ε=10^-6，γ控制soft-sign平滑 /趋于硬符号的程度，λ控制A稀疏。图2与正文描述逐步增强方向约束；附录表6给γ的二元设置，如Hateful α=0.5为(1,200)、λ=10^-4，Crisis α=0.5为(1,200)、λ=10^-2；医学γ=(1,25)、λ=10^-4（p.30）。表中元组的具体调度函数 /步数并未完整写明，不能自行假定线性增长或当作两个独立实验值。

“noise-free”指用L1强化特征、过滤作者所称无关噪声，不是差分隐私噪声消除证明。本地仍训练A和B，不冻结B。

### 3. 一次服务器聚合

将各客户端A展平叠成A'，得到PCA坐标Z与主成分P；按样本数量权重p_i聚合坐标（p.6式(5)）：

$$
A'=[\operatorname{vec}(A_1);\cdots;\operatorname{vec}(A_N)]\in\mathbb R^{N\times d},
\quad Z=\operatorname{PCA}(A')\in\mathbb R^{N\times k},
\quad Z_g=\sum_i p_iZ_i,\quad p_i=\frac{|D_i|}{\sum_j|D_j|},
\quad \operatorname{vec}(A_g)=Z_gP^\top.
$$

B用作者所称vanilla aggregation，然后与A_g组合并评估。不能把“vanilla”固定写成所有实验均样本加权FedAvg：附录表7 /8列明B在不同场景选Mean、FedAvg、FedAvgM、FedAdagrad或FedYogi；非PCA变体有时还用Ensemble。医学I3:T7的B用FedAvgM，I7:T3及Hybrid用FedYogi（pp.30–31）。一轮下采用有状态聚合器如何初始化其状态，复现也需核对。

**PCA复现边界（整理者核查）**：标准中心化PCA重建需加回均值 $`\mu_A+Z_gP^\top`$，原式省略均值；也未给出全部场景k、是否白化或展平粒度。若加回均值且保留全部主成分，线性加权重建等价于原空间加权平均；差异须来自截断 /中心化 /另行处理。PCA聚合不等于“所有局部知识都无损保留”。分别聚合A/B也不自动满足 $`B_gA_g=\sum_i p_iB_iA_i`$。

### 冲突分析与理论条件

令参数i在N客户端中有k_i个正号，M为参数总数，q_i=min(k_i,N−k_i)，C为平均少数符号比例（pp.4、23）：

$$
C=\frac1{MN}\sum_i q_i,\qquad
\bar\rho=\frac{2}{MN(N-1)}\sum_i k_i(N-k_i)
=\frac{2N}{N-1}\left(C-\frac1{MN^2}\sum_i q_i^2\right).
$$

这条计数恒等式成立，但跨不同冲突分布时不能只由C推断唯一ρ。作者在符号 /幅度模型下给IID近似 $`\mathbb E[\Delta W_g]=(1-2C)\mu`$、$`\operatorname{Var}(\Delta W_g)\approx[\sigma^2+4C(1-C)\mu^2]/N`$（pp.23–24）。它依赖独立性、幅度统计 /符号方向设定、近似均匀C_i；不是任意LoRA非凸任务上的风险界。

Non-IID附录引入客户端幅度差异d²，并假设C_i与幅度均值独立、客户端间协方差为零（pp.24–26）。原式(34)中的d_i²受4C_i(1−C_i)乘权，式(36)转成直接加d²时额外使用“幅度差异独立”的近似，不能把它称为前式必然的精确代数化简。

附录C的单轮收敛界还假设L-smooth、**强凸**、有界梯度方差、符号冲突方差与gradient-sign alignment（pp.26–28）。例如non-IID界为（p.27定理C.2）：

$$
\mathbb E[L(W^1)-L(W^*)]\le
\left(1-\eta\lambda_c\gamma_c(1-2C)^2\right)
\left[L(W^0)-L(W^*)\right]+\frac{\sigma_{\rm niid}^2}{2\lambda_cN}.
$$

这里把强凸系数与alignment系数重命名为λ_c、γ_c，避免与L1系数 /tanh温度混淆。LoRA双因子及MLLM目标通常非凸，原文未验证强凸或所有假设；它是受条件约束的理论模型。p.28式(1.4)的渐近表述没有保留上述初始误差收缩项，不能据此推出一次更新在N趋大时必然最优。p.29在符号概率近1/2时仍给C趋1/2，故不能同时无条件声称C=O(1/N)。千 /万客户端效用仅凭这些近似不能视为实验证明。

## 实验设置

| 项目 | 原文配置 |
| --- | --- |
| 模型 | 默认MiniCPM-V-2_6-int4；另测MiniCPM-Llama3-V-2_5-int4（pp.7、9） |
| 可训练位置 | 只最后一层q_proj的LoRA，rank8、alpha8、dropout0.05；主干冻结（p.7） |
| 客户端 / 本地训练 | 默认10客户端，各10epochs，表中报告第5 /10epoch的最佳结果；另测20、30、50客户端（pp.7、9、28） |
| 学习率 | Hateful2×10^-5；其他2×10^-4；cosine、1%warmup、batch1、accumulation4；NVIDIA A40（p.7） |
| 数据 / 场景 | Hateful-Memes、CrisisMMD、VQA-RAD、SLAKE、MedAlpaca；α=5 /1 /0.5、β=30 /40 /50%、I:T=3:7 /5:5 /7:3、p=80 /70 /60%（pp.6–7） |
| 指标 | Hateful AUC、Crisis F1；医学GPT-4评判open /closed /overall accuracy；MedAlpaca仅训练、SLAKE未见测试，沿用FedMLLM基准（pp.7–8） |
| 对照与变体 | Local、FedAvg、Mean、Ensemble、Combine与四种YOCO变体；多轮FL使用全部28层×4模块，分别25 /40 /50轮（pp.7–8表1–3） |
| 统计限制 | checklist第7项作者明确“No”：未报告error bars；表1–9不提供重复次数 /std /显著性，不能自行写成3seeds均值（p.17） |

上传件没有独立可执行代码压缩包，checklist的“代码在supplement”是作者声明，不表示本次已经取得或执行了那份代码。

## 主要定量结果

| 明确条件 | YOCO结果 | 同表对照与含义 | 证据 |
| --- | --- | --- | --- |
| CrisisMMD Aligned α=5.0，F1 | 完整PCA版本63.69 | one-shot Mean62.47、多轮FedAdam61.80 | p.7表1；分别+1.22 /+1.89个百分点 |
| Hateful Aligned α=0.5，AUC | 完整PCA70.65 | one-shot FedAvg68.19；多轮FedYogi74.32 | p.7表1；胜部分单轮，但低于多轮3.67个百分点 |
| Crisis Cross I3:T7，F1 | 完整PCA43.33；不带PCA稀疏版52.40 | Ensemble51.48、多轮FedAdam53.17 | p.8表2；PCA明显退化，不能称完整方案逐格最佳 |
| Crisis Cross I7:T3，F1 | YOCOInit&B56.12、完整PCA50.33 | Ensemble55.69 | p.8表2；不同YOCO变体的最佳值不同 |
| 医学I5:T5，VQA-RAD /SLAKE overall acc | 完整PCA61.64 /63.04 | 多轮FedYogi60.53 /56.74 | p.8表3；GPT-4评估，+1.11 /+6.30个百分点 |
| 医学Hybrid p=60%，VQA-RAD overall acc | 完整PCA62.75 | 多轮FedYogi63.08 | p.8表3；也有医学单元格低于多轮 |
| 50客户端、两个MLLM | 完整YOCO68.15 /69.83 | 多轮FedAdam66.67 /68.64 | p.28表5；新增扩展实验证据仅到N=50 |
| 单模态文本、Crisis α=0.5，F1 | 完整YOCO38.65 | 单轮Combine37.08、多轮FedAdam37.95 | p.31表9 |

“始终超越one-shot”属于摘要概括；上表明确显示完整PCA版的反例，且把不同变体挑选最佳值不能代替固定算法每格优胜。Hateful Hybrid p=80%的完整PCA版67.95也低于YOCO非PCA稀疏版69.13；不同变体与聚合器配置有实质影响。未报告不确定性，小差距不代表统计显著。

## 消融、成本与局限性

- **初始化 /正则 /PCA（pp.7–9表1–2、图6 /8）**：Crisis aligned α=5.0 的四变体63.23→63.58→63.51→63.69，并非每加一组件都上升；Crisis跨模态的PCA会明显降分，说明保留本地适应性与聚合一致性需要按条件判断。
- **rank /模块（p.9图7）**：Hateful示例r=2 /4 /8 /16对应69.44 /70.59 /70.65 /70.85；q /k /v /o为70.65 /69.22 /70.75 /69.73。作者取q、r8折中；不是q所有任务绝对最佳。
- **客户端数（p.9表4）**：MiniCPM-V-2_6，N10 /20 /30，完整YOCO69.96 /69.10 /68.49；多轮FedAdam75.58 /69.70 /66.91。改善并不覆盖全部客户端数。
- **通信口径（整理者计算）**：1×1×1除以25×28×4为0.0357%，除以40×28×4为0.0223%，医学50×28×4为0.0179%。论文约0.03% /0.02%使用的是轮数、层数、模块数归一化代理，**不是实测传输字节、网络时延或能耗**。客户端数量、参数尺寸、上下行 /模型初始分发、精度和PCA开销均需另计；不能说仅减少轮数就带来同一比例。
- **计算成本（原文 /边界）**：仅最后一层q适配器明显缩小训练参数范围；仍需主干计算，SVD初始化和服务器PCA也有成本。上传件未给每任务运行时、峰值内存 /总GPU-hours或PCA规模曲线，不伪造实测值。
- **作者局限（p.10）**：更适于LoRA初始化 /正则，其他PEFT方法未解决；仅最后一层并非最优，自动参数选择待探索；implicit supervision对多轮explicit supervision的额外收益未验证。
- **理论 /扩展限制（pp.23–29，整理者核查）**：独立性、符号与幅度关系、强凸、alignment等条件未在真实MLLM验证；N50以外是统计外推。PCA中心化、k和初始残差补偿不明确，影响可复现性。
- **隐私（整理者判断）**：原始数据不集中、上传次数减少；没有DPε/δ、secure aggregation或攻击评估。一次上传仍可泄露信息，不能从通信节省推出形式化隐私保证。L1“noise-free”不意味着更新不泄露私有内容。

## 官方代码、数据与复现信息

PDF p.1链接[作者仓库1xbq1/FedMLLM](https://github.com/1xbq1/FedMLLM)。截至2026-10-13核对，README确认YOCO获NeurIPS2025接收，但仍列“Release YOCO code”TODO；现有FedMLLM实现不等于完整YOCO实现。本次**未运行代码、未训练、未复现表中结果**。

复现需要取得对应YOCO实现 /supplement代码，核对SVD残差初始化与LoRA缩放、γ元组的调度、A的PCA中心化 /k /reshape、各条件聚合器状态、最佳第5 /10epoch选择规则、医学GPT评估版本。必须保留按场景变化的表7 /8聚合策略，才能诚实评估组件本身贡献；固定划分 /重复种子之后另行报告不确定性。

## 与其他论文的阅读联系

- [FedMLLM](../2025-xu-fedmllm/notes.md) 是明确基准来源（本篇p.13参考文献54，pp.7–8表1–3）；四模态构造及多轮数据共享，但轮数 /层数 /模块预算不同。本篇引用列表仍含FedMLLM早期版的Mike Zheng Shou，而本次上传FedMLLM v2首页 /官方v2六作者不含此人，不因此改写v2作者。
- [FFA-LoRA](../../2024-sun-ffa-lora/notes.md) 被直接引用（p.12参考文献41、p.22 related works）。其固定共同A保持聚合线性并验证DP；YOCO训练A/B，用符号和稀疏约束减少冲突，不具同样的严格线性聚合或DP条件。
- [AdaLoRA](../../2023-zhang-adalora/notes.md) 被引用（p.14参考文献65）。AdaLoRA分配层间rank预算；本文默认固定最后一层q、rank8，仅做rank /模块消融，不是已经采用AdaLoRA自适应选层。
- [PFAdapter](../2026-liu-pfadapter/notes.md) 保留V/O本地、共享Q/K并多轮聚合（其pp.4–6）；本篇区分同一q模块内部A/B的约束 /聚合，最终聚成统一模型。二者“个性化”的参数保留方式不同，无直接联合实验证据。

## 阅读总结

YOCO把预训练先验用于单轮联邦适配，并提供符号约束 /稀疏正则的机制与实证。评估时应分开“某YOCO变体最佳”“完整PCA方案”“相对多轮参数预算的通信代理”；其跨模态退化、理论前提、初始化 /PCA实现细节和代码发布状态都影响结论能否复用。

[返回总览](../../../README.md) · [跨论文比较](../../../comparison.md) · [官方会议全文](https://papers.neurips.cc/paper_files/paper/2025/file/58e6c003c9fb3992265005ff6aef1913-Paper-Conference.pdf)
