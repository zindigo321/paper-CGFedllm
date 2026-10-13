# FedMLLM: Federated Fine-tuning MLLM on Multimodal Heterogeneity Data

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 完整题名 | FedMLLM: Federated Fine-tuning MLLM on Multimodal Heterogeneity Data |
| 完整作者 | Binqian Xu, Xiangbo Shu, Haiyang Mei, Guosen Xie, Basura Fernando, Jinhui Tang（上传 PDF p.1；官方 v2 页面同序） |
| 实际阅读版本 | arXiv:2411.14717v2，2025-03-08；15 个物理页，正文 pp.1–8、参考文献 pp.9–10、补充材料 pp.11–15。目录年份采用阅读版的 2025，不采用首次预印本的 2024 |
| 正式发表信息 | 官方版本页未列出期刊 / 会议正式出版记录；按预印本整理，不把其他论文的 NeurIPS 接收信息移到本篇 |
| DOI | [10.48550/arXiv.2411.14717](https://doi.org/10.48550/arXiv.2411.14717)，arXiv DOI，非独立会议 DOI |
| 来源与引用 | [官方 v2 页面](https://arxiv.org/abs/2411.14717v2)；[官方 v2 全文](https://arxiv.org/pdf/2411.14717v2)；[citation.bib](citation.bib)；[source.md](source.md) |
| PDF 许可 | 官方 v2 为 arXiv non-exclusive distribution；仅保存全文链接，公开目录不复制上传 PDF |

以下页码均为上传 PDF 的物理页码；已读完全部正文、参考文献与补充材料，并检查首页、关键方法 / 实验表。核对日期：2026-10-13。`innovation2` 只沿用用户压缩包的分类，不解释其私有研究方向。

## 摘要

FedMLLM 研究图像与文本模态不完整、客户端间模态组成不同的 MLLM 联邦微调。贡献包含基准和框架：构造 aligned / missing / cross / hybrid 四种场景，覆盖五个数据集、两个轻量 MLLM、分类与医学 VQA 两类任务；在 LoRA 联邦微调上比较四个服务器优化方法、Zero-shot 与 Local，并加入模态无关提示以及中间层自适应近端正则。主实验强调跨机构 cross-silo 场景。在 FedAdagrad、Hybrid、p=60% 的 CrisisMMD 条件下，两项策略将 F1 从 53.45 提到 58.46，提升 5.01 个百分点（p.8 表10）。这不能推广为所有数据集或任意联邦优化器均有相同收益。

## 背景、不足与贡献

- **问题（原文）**：MLLM 使用图文输入，客户端可能丢失单个样本的模态，也可能整家机构只持有一种模态；仅用传统标签非 IID 描述不够（pp.1–3，图1 / 图3–5）。
- **既有不足（原文）**：多模态 FL 往往先用预训练编码器抽取特征；MLLM 完整微调规模大，普通 FedAvg / FedProx 在本基准出现不稳定（pp.4–5、11、14–15，图13–14）。这是作者的具体训练配置下观察，不能据此宣布 FedAvg 普遍不收敛。
- **贡献（原文）**：可控制的图文异质性基准；量化轻量 MLLM + LoRA 的统一联邦微调流程；无需生成缺失模态的提示和正则策略；多数据集及客户端数的评估（pp.2–8）。

## 方法流程与核心公式

设 K 个客户端共享冻结主干，客户端 k 的分布为 D_k、任务损失为 F_k。论文式(1)使用**等客户端权重**的目标，不应写成式中已有按样本数加权：

$$
\min_w f(w)=\frac{1}{K}\sum_{k=1}^K F_k(w),\qquad
w=w_0+\Delta w=w_0+BA.
$$

服务器初始化 / 下发 LoRA，选中客户端本地训练后上传 LoRA，服务器用 FedYogi / FedAdam / FedAvgM / FedAdagrad 聚合，循环多轮。生成式任务采用响应 token 的负对数似然（p.4 式(2)）。主干不上传原始数据，但这本身不是 DP 保证。

| 场景 | 构造与含义（pp.3–4、14） |
| --- | --- |
| Aligned | 所有样本模态完整；Dirichlet α=5.0 / 1.0 / 0.5 控制客户端非 IID |
| Missing | 在 aligned 划分上按**样本**移除模态，β=30% / 40% / 50%；与整客户端缺失不同 |
| Cross | 客户端仅图像 / 仅文本；I-3:T-7、I-5:T-5、I-7:T-3。医学场景分别分配 VQA-RAD 与 MedAlpaca |
| Hybrid | 以**客户端**为单位，每种模态以 p=80% / 70% / 60% 保留；若两者都缺失，随机保留一种 |

**提示策略**：将问题中“根据文本和图像”改为“without considering the modality”，避免缺失模态时仍要求完整图文依据；完整数据格式为 id / image / conversations（pp.4、14–15，表13–14）。这是作者的任务提示设计，不是给整理者的指令。

**正则策略（p.5 式(3)）**：

$$
\mathcal L=\mathcal L_{\rm mllm}
+\gamma\,\mathbf m\cdot\|\Delta\widetilde w-\Delta w_k\|_2,
\qquad
\mathbf m=[\underbrace{0,\ldots,0}_{S},1,\ldots,1,
\underbrace{0,\ldots,0}_{S}]^\top.
$$

为避免与 LoRA 因子 A 混淆，这里把论文的层掩码 A 重命名为 $`\mathbf m`$。原式写 L2 范数，未标平方；其层选择意图是只对中间 LoRA 层与全局 LoRA 的距离正则。前后 S 层保留低层模态与高层任务适应自由度。附录明确：cross 时 γ=γ_max；missing 时 γ=γ_max β；hybrid 按实际本地缺失情况处理，aligned 不正则。最终 γ_max=0.1、S=4（pp.7–8、14）。

这依赖客户端知道自身缺失模态比例，不是服务器自动推断隐私数据的机制。分别平均 A/B 仍可能出现 $`\overline B\,\overline A\ne\overline{BA}`$；本文未像 FFA-LoRA 那样通过固定因子消除该代数问题。

## 实验设置

| 项目 | 上传全文中的配置 |
| --- | --- |
| 模型 | 默认 MiniCPM-V-2_6-int4；另测 MiniCPM-Llama3-V-2_5-int4（pp.6–7 表7） |
| LoRA | rank=8、alpha=8、dropout=0.05；max sequence length=1200（p.6） |
| 联邦 | 默认10客户端、每轮随机选2；每轮本地1 epoch；另测4/10、5/20、10/30（pp.6–7、14） |
| 学习率 / 调度 | 初始2×10^-5；cosine，warmup ratio=0.01（p.6） |
| 训练预算 | Hateful-Memes 25轮；CrisisMMD 40轮；医学50轮。附录概括50轮时，仍应以主文的数据集停止点解释表中结果（pp.6、14） |
| Local / 统计 | Local选5 epochs；联邦结果3次随机划分的均值 ± 标准差（pp.6、14 表11） |
| 数据 / 指标 | Hateful-Memes：8,500训练 / 1,000测试，ROC AUC；CrisisMMD：13,608 / 2,238，F1；MedAlpaca：33,951训练；VQA-RAD：1,797 / 451；SLAKE仅未见测试（p.5 表1） |
| 医学评估 | MedAlpaca + VQA-RAD用于训练，VQA-RAD / SLAKE测试；GPT-4判 open / closed / overall accuracy（pp.5–6 表6） |

补充材料 SLAKE 一处称2,070测试，但表1和图12为2,094（836 open +1,258 closed；pp.5、13）；复现应核对实际测试清单。没有通过修改原文数字来消除差异。

## 主要定量结果

| 条件 | 对照 | FedMLLM基准 / 策略结果 | 证据 |
| --- | --- | --- | --- |
| Aligned α=0.5，CrisisMMD F1 | Local 39.12±1.45 | FedYogi 61.46±0.95 | p.5 表2；3次运行 |
| Missing β=50%，Hateful-Memes AUC | Local 66.80±0.11 | FedAdam 75.58±1.72 | p.5 表3 |
| Cross I-3:T-7，Hateful-Memes / CrisisMMD | FedAdagrad 69.33 / 49.22 | 加两策略71.17 / 49.56 | p.8 表9；AUC / F1，提升1.84 / 0.34个百分点 |
| Hybrid p=60%，CrisisMMD F1 | FedAdagrad 53.45 | 两策略58.46 | pp.7–8 表8 / 表10；+5.01个百分点 |
| 医学 Hybrid p=60%，VQA-RAD overall acc | Local 61.42±0.10 | FedYogi63.08±0.11 | p.6 表6；GPT-4评估 |
| 同一医学条件，SLAKE overall acc | Zero-shot64.95、Local59.22±0.28 | FedYogi57.05±0.59 | p.6 表6；未见域并不必然受益 |

医学测试也显示“协同训练扩大数据范围”不保证域外开放问题提升。例如 SLAKE 的 I-7:T-3 下 FL overall 为55.83，低于Zero-shot64.95和Local60.46（p.6）。不要用某个分类收益替代医学有效性证据。

## 消融、成本与局限

- **组件消融（p.8 表10）**：FedAdagrad / Hybrid / p=60% 的 CrisisMMD，基线53.45，仅prompt53.86，仅reg53.82，prompt +传统FedProx55.68，prompt +自适应中间层reg58.46。对应Hateful-Memes基线**69.93**，两策略73.69；p.7 表8把Hybrid基线写69.69，二者不一致，+3.76使用表10的69.93计算。
- **超参数（p.7 图7）**：γ_max与排除层数S影响结果，作者取0.1 /4；不能将其当作任意主干 / 模态的最优值。
- **客户端 / 模型（p.7 表7）**：在文中 missing β=50% 对应默认结果下，MiniCPM-V-2_6 的 FedAdam AUC 从2/10客户端75.58±1.72变为5/20的69.70±0.45、10/30的66.91±0.62；规模增加与每客户端样本变少同时变化，不是纯网络规模消融。
- **通信（pp.7、14，表7 / 表12）**：论文报告约617M /621M的通信规模；表12“Trainable / Total”是617M /8716M，正文未把该M清楚定义成参数或字节并完整列链路统计。不能无条件当作617 MB/每轮或617M可训练参数，更不能直接与另一论文按MB/R统计相除。
- **时间（p.14 表12）**：Hateful-Memes 11h05m、CrisisMMD 21h04m；该表无完整GPU型号、精度、每方向通信计费或真实网络条件。可训练适配器的减少不自动减去主干前向 / 反向成本。
- **作者局限（p.8）**：仅图文，尚未验证视频 / 音频；真实缺失机制更复杂；重点为10–30客户端的cross-silo，未验证成千上万移动设备。
- **隐私（整理者判断）**：训练数据留在本地；没有DP预算、裁剪 / 噪声机制、更新反演或成员推断评估，不把“隐私敏感任务”写成形式化隐私保护。

## 官方代码、数据与复现信息

[作者仓库1xbq1/FedMLLM](https://github.com/1xbq1/FedMLLM) 的README明确链接本篇，包含数据划分、missing / cross / hybrid生成、本地微调与分类 / GPT医学评估文件。当前README的Python / CUDA安装说明是仓库现状，不必然等于2025 v2的原始环境；代码许可不替代PDF许可。本次**未安装、未训练、未运行复现**。

复现需固定具体主干版本、真实LoRA target modules、聚合器超参数、3组seed及数据清单；医学评估应保留GPT模型版本 / 提示 /响应和测试数量；确认617M统计口径。上传件的补充材料不含独立代码压缩包。

## 与其他论文的阅读联系

- [YOCO](../2025-xu-yoco/notes.md) 直接引用本篇（YOCO p.13参考文献54，pp.7–8表1–3），采用四模态场景和相同主干，转为只训练最后一层q_proj并一次通信。YOCO的0.03%比较同时改变轮数、层数和模块数，不能当作同一训练参数预算下的纯通信算法收益。
- [PFAdapter](../2026-liu-pfadapter/notes.md) 将本篇作为MLLM联邦基线（其p.11参考文献36），通过Q/K全局、V/O本地的投影划分减少同步；其客户端本地测试平均 / accuracy / AUC口径不能直接与本篇的未见SLAKE零样本测试数值横比。
- [FFA-LoRA](../../2024-sun-ffa-lora/notes.md) 固定共同A使聚合线性（其pp.4–6）；本篇训练双因子并改变server optimizer / local regularization，问题有交集，但无相同DP / 图文任务的受控实验。这里是机制对照，不声称已验证组合方案。

## 阅读总结

本篇主要价值是区分图文缺失的粒度和构造可重复场景，再评估轻量MLLM联邦微调。读结果时需同时检查模态场景、服务器优化器、提示 / 正则是否启用、测试域及通信单位，不能只摘取“FL优于Local”或“保持隐私”的概括。

[返回总览](../../../README.md) · [跨论文比较](../../../comparison.md) · [官方阅读版全文](https://arxiv.org/pdf/2411.14717v2)
