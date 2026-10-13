# PFAdapter: Hierarchical LoRA Decomposition for Personalized Federated MLLMs

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 完整题名 | PFAdapter: Hierarchical LoRA Decomposition for Personalized Federated MLLMs |
| 完整作者 | Jing Liu, Kun Yang, Yan Wang, Dingkang Yang, Xiaoshuai Hao, Wei Zhang, Yang Liu, Wei Zhou（上传PDF p.1、官方v2页面同序） |
| 实际阅读版本 | arXiv:2607.12111v2，2026-10-03，11个物理页；正文pp.1–10、参考文献pp.10–11；首页IEEE TCCN排版，但阅读对象仍是上传的arXiv托管版 |
| 正式发表信息 | 官方v2注释“Accepted by IEEE TCCN”，并列[期刊DOI 10.1109/TCCN.2026.3740672](https://doi.org/10.1109/TCCN.2026.3740672)；本次未取得独立IEEE VOR全文或核定卷期页码，不声称上传件与正式VOR逐字节一致 |
| arXiv DOI | [10.48550/arXiv.2607.12111](https://doi.org/10.48550/arXiv.2607.12111)，与期刊DOI分开 |
| 来源与引用 | [官方v2](https://arxiv.org/abs/2607.12111v2)；[官方v2全文](https://arxiv.org/pdf/2607.12111v2)；[citation.bib](citation.bib)；[source.md](source.md) |
| PDF许可 | 指定v2为arXiv非独占分发许可；公开目录仅链接全文，不复制上传PDF |

已读完上传件全部正文与参考文献，检查首页和关键公式 / 表格；全文多次引用独立supplement，但**上传11页不含该补充材料**，不能将其证明、客户端本地测试细则或显著性表写成已经读到。物理页码和元数据核对日期：2026-10-13。分类沿用上传压缩包，不描述用户创新点。

## 摘要

PFAdapter 将MLLM注意力中的LoRA按投影模块拆成两组：Q/K参与全局同步，V/O保留为客户端个性化参数。客户端用任务损失和Frobenius正交惩罚训练所有适配器，服务器仅按样本量聚合Q/K。它减小上传的适配器范围，保留本地知识，针对非IID下全参数同步的“weight washing”。Aligned / Dirichlet α=0.5、10客户端每轮选2、50轮条件下，VQA-RAD accuracy为62.83±0.62%，pFedLoRA为61.74±0.74%；同步流量315 MB/round，对照617 MB/round（p.8表I）。这是客户端本地测试平均的个性化评估；与全局未见域评估不是同一口径。

## 背景、不足与贡献

- **问题（pp.1–3）**：机构的数据分布不同，统一平均全部LoRA可能冲淡本地任务知识，并传输无需共享的适配器。
- **方法动机（pp.4–5）**：Q/K改变token之间的注意力关系，V/O更直接承载内容变换。作者据此固定投影级共享边界；这是一种结构设计及实验归纳，不是所有模型都严格成立的语义分解定理。
- **原文贡献（pp.2、4–6）**：投影级global/local划分；正交损失；选择性聚合；医学与社交图文任务上的效用及成本评估。

## 方法流程与核心公式

冻结主干 $`W_0`$，每个模块更新为 $`\Delta W_{l,m}=B_{l,m}A_{l,m}`$。L层的共享 / 本地参数集合（p.4式(6)–(7)）为：

$$
\Theta^G=\bigcup_{l=1}^L\{A_{l,m},B_{l,m}:m\in\{q,k\}\},
\qquad
\Theta_k^L=\{\hbox{client }k\hbox{ 的 }v,o\hbox{ LoRA因子}\}.
$$

Q/K全局并不表示冻结：选中客户端仍训练其本地Q/K副本。V/O本地也不等于只训练一半参数：每个客户端训练的LoRA总量与同配置完整LoRA相同（p.5）。服务器下发Q/K，本地V/O持续保留，参与客户端一起优化任务损失与正交损失；训练后只上传Q/K，按选中客户端样本数量加权（p.6式(16)）：

$$
\Theta^{G,t+1}=\sum_{k\in S_t}
\frac{n_k}{\sum_{j\in S_t}n_j}\Theta_k^{G,t+1}.
$$

**正交损失（p.5式(11)）**，令 $`U_{l,m}=B_{l,m}A_{l,m}`$（将原文W重命名，避免与冻结主干混淆）：

$$
\mathcal L_o=\sum_{l=1}^L\sum_{g\in\{q,k\}}\sum_{h\in\{v,o\}}
\|U_{l,g}^{\top}U_{l,h}\|_F^2,
\qquad
\mathcal L_{\rm total}=\mathcal L_t(D_k;\Theta^G,\Theta_k^L)+\lambda_o\mathcal L_o.
$$

该乘积要求各模块对应的行维度相容；换成不同输出维度 / grouped-query架构时必须重新核对实现，不能只照抄模块名。原式以有效更新矩阵为对象，减少线性子空间的重合；有限惩罚不意味着完全独立或隐私信息不可泄露。

对一个相容矩阵对，$`\partial\|U_g^\top U_h\|_F^2/\partial U_g=2U_hU_h^\top U_g`$（与p.5式(13)的矩阵顺序一致）。这先是**有效更新矩阵**的导数；实际训练A/B需链式法则，不能把同形表达式无条件当作每个低秩因子的梯度。

**通信计算（p.6式(17)）**：

$$
P_{\rm all}=\sum_l\sum_{m\in\{q,k,v,o\}}r(d^{\rm in}_{l,m}+d^{\rm out}_{l,m}),
\quad
P_{\rm PF}=\sum_l\sum_{m\in\{q,k\}}r(d^{\rm in}_{l,m}+d^{\rm out}_{l,m}),
\quad C_{\rm PF}^{\rm round}=2bP_{\rm PF}.
$$

其中b为传输字节/参数，2表示上传+下载的理论计数。只有等秩、匹配投影尺寸等条件下P_PF/P_all=1/2；论文报告617→315 MB/R，实际为48.95%减少（整理者按1−315/617计算），而不是总训练内存或算力减半。

### 理论结果与可解释边界

作者p.6假设局部目标smooth、随机梯度方差与梯度有界、非IID漂移δ²有界、选择性聚合偏差β和正交梯度H_o有界。定理1（式(18)）上界包含：

$$
\frac1T\sum_{t<T}\mathbb E\|\nabla F_t\|^2
\le\frac{C_1+C_2\delta^2+C_3\sigma^2/|S_t|}{\sqrt T}
+C_4\lambda_o^2H_o^2+C_5\beta^2.
$$

**整理者核查**：固定非零λ_oH_o与β时，最后两项不会随T消失，因此显示的上界只给衰减项加残差，不能仅由“各量有限”推出全文接着声称的趋零O(T^-1/2)。需要额外的残差消失 / 衰减条件，或不同stationarity定义。上传件也未附其证明，所以不代作者补证明，不把该句当作无条件收敛保证。

## 实验设置

| 项目 | 原文配置与边界 |
| --- | --- |
| 主干 | MiniCPM-V-2_6-int4、Qwen2 backbone；p.7同时提8-bit量化 / gradient checkpointing，int4模型名与实际8-bit加载关系未完整说明 |
| LoRA | Q/K/V/O投影，rank8、LoRA alpha16；λ_o=0.1（p.7） |
| 客户端 / 预算 | 10客户端、每轮采样2、50轮；本地1epoch；batch1、gradient accumulation16（p.7） |
| 优化器 | 本地AdamW、lr2×10^-5、cosine；PFAdapter服务端为样本量加权平均，不是FedYogi（pp.6–7） |
| 场景 / 统计 | 主表Aligned、Dirichlet α=0.5，3seeds mean±std；表I明确macro-averaged client-local test scores（pp.7–8） |
| 数据 / 指标 | VQA-RAD、SLAKE、CrisisMMD：accuracy / weighted F1；Hateful Memes：accuracy / AUC（p.7） |
| 硬件 | 单NVIDIA L20，48GB VRAM（p.7） |

上传正文把完整数据量写为VQA-RAD3,515对、SLAKE14,028样本、Hateful10,000、CrisisMMD16,080（p.7），未给出全部实际训练 / 本地测试切分；不能把数据集总量当作每轮训练数。补充材料VI-B的具体分区复用 / 本地评估细则未随上传提供。主表固定50轮，正文引用的达到目标准确率所需更长轮数属于另一诊断，不能混合成本预算。

## 主要定量结果

同为Aligned α=0.5、50轮、3seeds，p.8表I摘取：

| 数据 / 指标（%） | pFedLoRA | PFAdapter | 差值（整理者计算，百分点） |
| --- | --- | --- | --- |
| VQA-RAD accuracy | 61.74±0.74 | 62.83±0.62 | +1.09 |
| SLAKE accuracy | 59.12±0.43 | 60.08±0.38 | +0.96 |
| Hateful Memes accuracy | 74.38±0.68 | 75.23±0.51 | +0.85 |
| Hateful Memes AUC | 74.92±0.72 | 75.63±0.63 | +0.71 |
| CrisisMMD accuracy | 61.48±0.58 | 62.49±0.46 | +1.01 |

图1 / 图2及官方摘要仍出现“+2.4–4.8%”概括，但表I对最强个性化基线差距为上表，不把该范围写成相对pFedLoRA的严格提升。SLAKE Zero-shot=64.95%、Local=61.63%，都高于PFAdapter60.08%，说明“在四数据集全面最佳”应限于匹配的联邦学习基线，而非表内所有参考项。3seeds标准差不等于统计显著性，独立supplement的paired-test表未实际取得。

额外正文诊断：α=0.1的VQA-RAD accuracy61.2 vs FedYogi57.8；Missing β=50%时Hateful AUC76.8 vs75.12、CrisisMMD F1 56.5 vs53.78；20%高斯噪声时VQA-RAD accuracy54.6 vs48.5（pp.8–10图3 /图5、p.9文字）。这里的高斯扰动是鲁棒性压力测试，没有DP会计，不写成DP效用实验。Missing文字称“50%客户端”，而图标为β并沿用FedMLLM的样本缺失指标，缺失粒度需实现 / 细则核对。

## 消融、成本与局限性

- **消融（p.8表II）**：完整62.83 /60.08 /75.63（VQA acc /SLAKE acc /Hateful AUC）；去正交61.33 /58.58 /74.30；取消选择性聚合60.93 /58.18 /73.80、通信617 MB/R；去层次拆分60.53 /58.67 /72.48。正文明确去拆分仍用同样服务器加权平均，不能说它自动变成FedYogi，即使表中结果相同。
- **拆分（p.8表III）**：VQA，Q-only全局60.2 /155 MB/R；QKV全局59.7 /469；QV全局61.5 /315；QK全局62.8 /315。该表仅列VQA，SLAKE拆分结论来自正文 / 未提供supplement。
- **敏感性（pp.8–9图3）**：VQA和Hateful在λ_o=0.1较好，SLAKE在0.05较好；过强惩罚退化。50:50是文中条件的选择，不是统一最优。
- **成本（p.9表IV）**：PFAdapter10.8 min/round、0.180 GPU-h/R、15.8 GB峰值；FedYogi10.3 min/round、0.172 GPU-h/R、15.7 GB。共50轮传输15.75 vs30.85 GB，时间略增而通信减。表IV列Inference Time14.8 vs14.7，但未清楚标该列计时单位 / 测试批量，因此不补写毫秒。
- **作者局限（p.10）**：极端域漂移可能要自适应拆分；各层用统一拆分；没有含straggler、upload-cap、dropout调度的分布式实网试验；Frobenius不能完整刻画非线性依赖。
- **隐私范围（p.1及整理者归纳）**：作者明确只保持原始数据本地，不保证抵抗更新反演 /梯度泄露 /成员推断。Q/K更新仍发送，不含DP预算；“local-private”是参数驻留位置，不是形式化隐私定义。
- **适用限制（整理者判断）**：个性化模型需保留各客户端V/O状态，只有服务器Q/K不能完整代表所有客户端；新客户端如何初始化V/O、cold-start0-shot的评估来源，应结合独立supplement核对。

## 官方代码、数据与复现信息

上传11页未给独立实现仓库或执行脚本；官方arXiv v2页亦未列专属代码。本次检索未核实作者发布的PFAdapter实现，不虚构同名社区项目为官方。论文所引用FedMLLM仓库只能确认基准来源，不能说明PFAdapter模块拆分和正交实现已经公开。本次**未安装、未运行、未训练复现**。

复现至少要补足独立supplement、训练 /本地测试清单、seed、模块维度映射、量化加载精度、适配器持久化 /下发规则、目标层、正交损失实现与实际梯度、字节统计方向及序列化口径。未提供的证明及公平性 /显著性诊断不能用正文引用替代。

## 与其他论文的阅读联系

- [FedMLLM](../2025-xu-fedmllm/notes.md) 被本篇直接引用（p.11参考文献36）；本篇把全适配器同步改为Q/K同步、V/O本地，而FedMLLM主要改server optimizer及本地prompt /proximal。两篇SLAKE评估域和本地 /全局指标定义不同，不能按表面数字排序。
- [YOCO](../2025-xu-yoco/notes.md) 一次上传最后一层q_proj的A/B，靠SVD先验方向和A稀疏正则减少冲突（其pp.5–7）；本篇是50轮投影级个性化。二者模块选择与轮数都不同，48.9%与0.03%是不同分母。
- [FFA-LoRA](../../2024-sun-ffa-lora/notes.md) 固定共享A解决双因子聚合误差并研究DP（其pp.4–6）；本篇仍优化双因子Q/K，因此选择性同步本身未证明消除LoRA乘积交叉项，也未验证DP。

## 阅读总结

该文提供了注意力投影内的共享 /个性化边界，并在本地测试的联邦LoRA比较中实现效用与通信折中。重要阅读边界是：本地仍训练全部LoRA，通信减半不等于计算减半；严格结果以表I为准；带固定残差的理论界不等于无条件趋零；独立补充材料仍需取得。

[返回总览](../../../README.md) · [跨论文比较](../../../comparison.md) · [官方阅读版全文](https://arxiv.org/pdf/2607.12111v2)
