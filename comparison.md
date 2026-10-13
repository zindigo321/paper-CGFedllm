# 14 篇论文的条件化比较

本表是**整理者归纳**，具体方法与数字以各篇笔记和其所标上传 PDF 页码为准。比较范围为现有 14 篇实际附件（文件名别名不重复计数，未提供的补充材料不算已读）；不是全领域综述。它们分别优化适配器容量、私有梯度压缩、学习传输压缩、传输稀疏性、聚合一致性、主干压缩、同步梯度压缩的收敛控制、每实例图像码流适配与客户端 replay 稳定性，不能按一个 Accuracy / 通信倍数做统一排名。

## 问题、方法、条件与局限

| 论文 / 已读版本 | 核心问题 | 方法与压缩对象 | 实验条件 | 主要结果与出处 | 局限 / 适用边界 |
| --- | --- | --- | --- | --- | --- |
| [AdaLoRA](papers/2023-zhang-adalora/notes.md)，2023 v2 | 同预算下各层 / 模块容量分配不合理 | 可学习 SVD 增量、重要性评分、动态总秩；压缩任务增量容量 | centralized DeBERTaV3-base / BART-large；GLUE / QA / 摘要；无 FL / DP | SQuAD v2.0，0.08% 参数，F1 88.7 vs LoRA 87.5；p. 8 表 2 | 额外评分 / 正则 / 调度开销；无联邦 / DP 验证；正文和附录部分配置冲突 |
| [DR-Encoder](papers/2024-wu-dr-encoder/notes.md)，2024 v1 | 压缩器训练与梯度交换泄漏、预训练收集开销 | 梯度统计量 → Gaussian 合成 → AutoEncoder；编码 / 裁剪 / 加噪 / 聚合 / 解码 | LLaMA / Qwen 7B，Dolly / MMLU 微调；C-Eval / MMLU；作者主张 client-level DP | Qwen / MMLU，GDP  $`\epsilon=4`$ ：56.20 vs 带噪 LoRA 25.50；p. 7 表 4 | 统计量发布隐私未完整说明；轮数 / 算子 / 字节数有疑点；未核实官方代码 |
| [FLASC](papers/2024-kuo-flasc/notes.md)，2024 v1 | LoRA 通信仍昂贵，冻结稀疏权重损害效用 | 稠密本地训练、上下行独立 Top-K 传输；服务端维持稠密状态 | cross-device 单机模拟，ViT-B-16 / GPT2-Small；4 任务；FedAdam / central client-level DP | 四任务约 3–10× 更少通信匹配 dense LoRA；pp. 6–7 图 2 | 实际网络端到端时间未测；仍需稠密适配器训练；DP 用模拟较大 cohort；不是 7B LLM 实验 |
| [FFA-LoRA](papers/2024-sun-ffa-lora/notes.md)，2024 v1 / ICLR | 分别聚合双因子产生误差，双噪声乘积与缩放不稳定 | 共享冻结随机  $`A_0`$ ，仅训练 / 聚合  $`B`$  | 3-client cross-silo，RoBERTa-Large，1000 rounds × 10 local steps；客户端 record-level DP-SGD | MNLI-m， $`\epsilon=6,\delta=10^{-5}`$ ：78.81±0.8 vs 39.46±14.3%；p. 7 表 1 | 冻结子空间限制容量；同预算不逐任务占优；参数减少不等于总计算量减半 |
| [SVD-LLM](papers/2025-wang-svd-llm/notes.md)，2025 v5 / ICLR | 权重 SVD 截断与校准输出误差不对应，截断后恢复不足 | Gram matrix 白化、 $`WS`$  的 SVD、两个低秩因子顺序 LoRA 恢复；压缩主干与可选 KV cache | 7 个模型、10 任务；256 校准样本、50K Alpaca 恢复；A100 / EPYC 7643 实测 | LLaMA-7B，40% 参数删减：WikiText-2 PPL 9.27 vs ASVD 1407；原模型 5.68；p. 6 表 1 | 高比例精度下降；恢复耗时；KV 展开延迟；PPL 不能完全代表生成质量；与早期版 / V2 不同 |
| [CG-FedLLM](papers/2025-wu-cg-fedllm/notes.md)，2025 v3 扩展版 | 联邦 LoRA 更新仍昂贵，动态联合训练压缩器困难 | 真实时间序列梯度 → TGAP AutoEncoder；FAF 编码 / 重建两个因子再聚合 | LLaMA / Alpaca / Qwen 7B，Dolly / C-Eval / MMLU，RTX 4090 单机模拟；作者分析 client-level DP | Qwen / MMLU，GDP  $`\epsilon=0.25`$ ：56.37 vs 带噪 LoRA 25.22；p. 7 表 2；二维 CR 1.56% 为元素保留比 | TGAP 真实梯度隐私、算子顺序、客户端数、泛化描述有疑点；分别聚合因子的交叉项；未测完整网络成本 |
| [PowerSGD+](papers/2025-xie-powersgd-plus/notes.md)，2025 v1；正式 ICASSP 2026 | 单步子空间跟踪即使配 EF 仍可能失去收敛控制 | 同步全参数梯度 / EF 校正更新；共同基底、单步 power iteration、周期 SVD safeguard | 4 × RTX 4090；RoBERTa-Base / GLUE；LLaMA-60M / 130M / C4；无 DP，非联邦 LoRA 实验 | GLUE 原表 Avg 86.28 vs PowerSGD 85.73，p. 6 表 1，前三个基线均值有核算差异；C4 130M / rank 8 PPL 26.11 vs 26.24，p. 9 表 3 | 理论针对 MSGD，实验 Adam / AdamW；刷新传完整矩阵；有限步依赖 tau / rank；证明记号、配置与官方代码待核实，未测 wall-clock |
| [ISER](papers/2026-park-iser/notes.md)，2026 Electronics 期刊版33页 | 图像 codec 在新任务 / 每图实例上的适配与 TTFT 开销 | SVD-LoRA，decoder SV 动态全局预算、ISES、patch→全图 MSTS；压缩图像码流 | TIC / Cheng2020，COCO / ImageNet / KITTI；每图已知目标 evaluator，无 DP；4090 | TIC open segmentation BD-Rate −52.86% vs LoRA-comp −49.51%，相对节省幅度约6.77%，p.17表2；最大44%编码减少为另一 closed detection 条件 | 秒级编码 / 毫秒解码分开；预算 / 信令与公开代码不完全一致；小 TTFT 预算不逐项领先，不是梯度压缩 |
| [FedALA-WR](papers/2026-singh-fedala-wr/notes.md)，2026 Cluster Computing 期刊版17页 | non-IID pFL 的轮内遗忘 / 聚合稳定性 | 本地 entropy replay、mixture loss、逐层 attention 聚合完整 CNN 参数；不压缩消息 | 4-layer CNN，20 / 50 / 100 clients，private test；五次重复，单机2×3080，无 DP | CIFAR-100 Dir0.10 / 20 clients，57.53±0.15% vs FedALA56.99±0.19%，p.12表3；Tiny时间175.56 vs182.43min，p.15表5 | 正文 / 表格及公开代码 replay detach、距离符号、stop规则有差异；无完整收敛证明 / 网络时间 / LLM验证 |

## 2026-10-13 新增论文：条件与边界

以下仅归纳公开论文的方法和实验，不将分类名称解释为创新点，也不添加未验证的联合研究方案。

| 论文 / 阅读版本 | 方法与对象 | 实验条件 | 关键结果及页码 | 局限 |
| --- | --- | --- | --- | --- |
| [AE-PSL](papers/innovation1/2026-meuwissen-ae-psl/notes.md)，2607.17913v1 | GA公共对齐、CSA本地AE暖启及decoder平均；DFT冻结AE，压缩ViT切分层patch激活和latent梯度（pp.5–6） | ViT-B/32，s5；N5/25，四视觉分类任务；LoRA r16/alpha32，10epochs，3seeds；global测试移除AE、local保留（pp.6–8、16） | ViT-B/32、N=5、CIFAR-100 global evaluation、R≈10：82.7±0.2%，与无压缩82.7±0.2%相同；3 seeds（pp.8、17，表1/4） | 仅视觉分类、CLS不压缩；global评估移除AE而local评估保留；摘要与正文5.2/5.3及附录95/99%目标存在口径差异（pp.1、7、10、12、18–20） |
| [SNC](papers/innovation1/2026-almanifi-snc/notes.md)，Elsevier typeset journal article, Internet of Things 40 (2026) 102113 | Top-k残差、Conv1D/GDN量化latent及learned prior/arithmetic coding压缩非零更新，Fibonacci编码索引；服务器PCA+KDE增广训练codec（pp.7–11） | K15/Kp8，Dirichlet alpha0.3，MLP/CNN/VGG/ResNet四小视觉模型；codec100epochs；峰值测试accuracy/平均更新CR（pp.12–14） | FMNIST/CNN/FedAvg、K=15/Kp=8、alpha=0.3，lambda=10：峰值88.89%，平均更新CR450.79倍；无压缩88.24%（pp.13–14，表2/3） | 只小视觉模型；CR重点上行更新；CIFAR100 lambda10损失8.92个百分点；无独立privacy攻击或严格加密验证，收敛条件未保证（pp.12、14、16、20） |
| [ECLoRA](papers/innovation1/2025-ning-eclora/notes.md)，IEEE typeset October 2025 issue, current version dated 2025-10-09 | 重构BiAi按数据量平均，补偿服务器上一轮分解残差，RSVD并按客户端rank截断下发（pp.4–5） | N100/参与0.1，rank4/8/16/32/64；四语言基础模型、六任务，200rounds，3seeds，beta1、p2r（p.8） | RoBERTa-base/MRPC：88.7±1.4，FedIT83.8±1.1；聚合0.33s，FlexLoRA9.64s；各模型平均轮数收益1.54–3.01倍（pp.9–10，表II/III） | LoRA专属严格理论留待未来；完整维度服务器残差；label-flipping仅投毒实验；公开main源码RSVD输入未补偿，与论文式8不同（pp.4、8、13；作者代码静态核查） |
| [Learned Parameter Compression](papers/innovation1/2024-chen-learned-parameter-compression/notes.md)，IEEE Open Journal of the Communications Society Version of Record; current version 2024-06-25 | 逐层Conv1D autoencoder；本地每次迭代替换为有损重建参数；35轮预热后一次共享decoder，常规只上传低维码并解码平均（pp.5-7）。 | LeNet/MLP，Fashion-MNIST/CIFAR-10/100；100clients、500rounds、seed1234；B64/E10或B8/E1；DLG/IGA、128样本、7k攻击steps；无DP。 | Regular表示CR4.10×（p.9表6）；CIFAR10 LeNet IID B64/E10 60.43% vsFedAvg60.75%；non-IID B8/E1 41.65% vs46.18%（表4）；已训练MLP第5/40轮IGA，两个数据集测得SSIM0.00/ASR0（pp.11-12表11-12）。 | 攻击条件下经验结果非DP保证；4.1×未计全尺寸预热、decoder与下行总账；单seed、小模型；缺少本地替换/仅上传压缩的独立组件消融。 |
| [LoRA-comp](papers/innovation1/2025-park-lora-comp/notes.md)，CVF CVPR 2025 Open Access accepted version; printed pages 4430-4440; not the separately hosted supplementary material | SVD-LoRA W0+UΣVᵀ，两阶段初始化/每图TTFT；encoder更新全因子，decoder仅SV；量化/算术编码SV随图像位流发送（pp.4-5）。 | TIC、rank4、40iterations/图；COCO检测/分割、ImageNet分类；四quality λ2/1/0.5/0.2；open-set仍用已知目标evaluator特征；消融A10080GB、COCO5000图；无DP。 | 相对TIC：closed检测BD-Rate−54.96%/BD-mAP2.98；open检测−48.94%/2.69（p.7表1）；40iteration消融0.106bpp/mAP36.25/14.13s（表2）；decoder全因子额外位流overhead15.3×（p.8图9）。 | TTFT秒级编码；open-set需要目标网络而非未知任务零信息；SV共享初始化与码流成本；主文缺少seed统计/完整复现参数；未取得supplement，不能引用其CNN结果。 |

不同论文压缩的激活、参数、图像码流、张量因子和同步次数不同；压缩率 / 同步量 / BD-Rate / 准确率不可跨条件直接排名。

## 哪些资源数字可以比较

| 概念 | 在论文中表示什么 | 不能混淆的量 |
| --- | --- | --- |
| AdaLoRA 的  $`b(t)`$  / 参数比例 | 全局保留方向数 / 相对 full fine-tuning 的可训练参数量 | 实际训练 GPU 显存、传输字节、主干删减比例 |
| DR-Encoder 的  $`6.10\times10^{-5}`$  | AutoEncoder **预训练前收集阶段**传输数值个数之比；167,772,160 vs 10,240 | 全程总网络通信压缩比；原文 160 MB / 0.078 MB 的精度口径有疑点（p. 9 表 5） |
| FLASC 的  $`d_{\mathrm{up/down}}`$  | 上 / 下行**保留比例**；达到目标效用的累计通信 | 本地稠密训练 FLOPs；实际网络 wall-clock；不一定含协议 / 索引全部成本 |
| FFA-LoRA 的参数“减半” | 仅训练  $`B`$ ；方阵时  $`rd/[r(d+k)]=1/2`$  | 所有非方阵的精确减半；完整模型训练时间减半 |
| SVD-LLM 的  $`R_w`$  | 主干权重**删减比例**： $`1-r(d+n)/(dn)`$  | 保留比例、量化位宽、运行时 peak memory 或 KV cache 占用 |
| CG-FedLLM 的 CR / 元素压缩比 | 表 1 的编码输出 / 输入元素数；二维 131,072 / 8,388,608 = 1.5625%，其倒数为 64（整理者计算） | 不含 TGAP 梯度收集、压缩器分发、下行和协议成本；1D 形状计算为 3.125%，原表写 3.21%（pp. 4–5） |
| PowerSGD+ 的每步通信量级 | 原表为  $`mr+nr+mn/\tau`$ ，刷新步对完整 EF 校正矩阵做 All-Reduce；表内元素保留比为  $`r/m+r/n+1/\tau`$ （整理者计算，pp. 4、7–8） | 不是协议 / 拓扑后的累计字节或网络速度；伪代码替换刷新步的精细摊销为  $`mr+nr+(mn-mr)/\tau`$ ；未消除完整 EF / 优化器状态 |
| ISER 的 BD-Rate / SV overhead | 相对 human-centric codec 的 RD 曲线码率差；p.29表14的 SV 比例报告平均0.98%、范围0.29%–2.05%，涉及 image / total 分母差异 | 不是全程联邦通信节省、主干删减或每图均低于1%；表中 MACs 不含累计 TTFT 训练；码流位置成本待核实 |
| FedALA-WR 的 TΣ / buffer size | 上下行完整模型参数个数累计到 T 轮；buffer容量按本地样本数，不增加 sample 消息 | 不是字节 / 稀疏密度 / rank；须计客户端数、实际停止轮数、位宽 / 协议；wall-clock 为单机计算 + 调度，不是公网传输 |

这些比例的对象、阶段和分母不同，不能将 10×、64 倍元素比、一半、40%、 $`6.10\times10^{-5}`$  与一个矩阵的秩 / 刷新元素比例排为“哪个方法最省资源”。

## 隐私保护条件不是同一种实验

| 方法 | 保护对象与噪声位置 | 对服务器的信任 / 采样前提 | 尚需核实 |
| --- | --- | --- | --- |
| AdaLoRA | 未提供 DP 机制 | centralized PEFT | 无法据此主张隐私保护 |
| DR-Encoder | 作者称 client-level DP；客户端编码后裁剪加噪，再聚合 / 解码 | 按客户端采样，使用 GDP / RDP；预训练统计量也被分享 | 统计量是否私有化、完整  $`\delta`$ 、Qwen 轮数、Gaussian mechanism 的精确对象（PDF pp. 3–6、13–15） |
| FLASC | central / global client-level DP-FedAdam；服务端裁剪聚合后加噪 | 实际 Reddit 10 / FLAIR 200 clients，但预算用 1000 / 5000 simulated cohort | 报告预算与实际小 cohort 直接部署不等价；完整 accountant /  $`\delta`$ （pp. 10–11、20） |
| FFA-LoRA | record-level DP；客户端逐样本裁剪和加噪，发布更新前已 DP | 无须可信服务器；3 个机构持较多本地记录 | 全轮次客户端采样率 / DP step 核算、HPO 的完整隐私成本（pp. 3、7、16） |
| SVD-LLM | 未提供 DP；使用校准和微调数据 | 离线压缩 / 恢复 | 不能视为私有压缩算法 |
| CG-FedLLM | 作者分析 add/remove-client DP / GDP；第 4.5 节为编码后裁剪加噪聚合解码，附录 D.2 为因子先加噪再编码 | 第 3.4 节假设 honest server / semi-honest client；TGAP 用真实梯度，基本 FAF 先逐客户端解码再聚合 | TGAP 与压缩器权重发布的覆盖范围、完整  $`\delta`$ 、A/B 联合预算、采样与噪声单位、机制次序（pp. 5–6、8–9、20–21） |
| PowerSGD+ | 未定义 DP / 加密 / secure aggregation；普通步骤发布投影与坐标，刷新交换完整校正更新 | 同步 workers 的共同基底 / All-Reduce；理论为优化收敛 | delta 为收缩系数、sigma 为随机梯度方差、epsilon 为优化精度；加入 DP 后须重做发布范围与核算，原定理不提供隐私保证（pp. 3–8、16–18） |
| ISER | 未提供 DP / 加密；图像与实例 SV 是数据相关输出 | 单图 TTFT、已知任务 evaluator 和共同初始化；无联邦服务器 | 输入 Gaussian noise 是鲁棒性测试；delta 是学习率，不能视为隐私预算；原始码流 / SV 发布隐私另需研究（pp.7–9、16、27–28） |
| FedALA-WR | 未提供 DP / secure aggregation；buffer存本地原样输入，服务器收完整模型 | 经典单机 FL 模拟；不发 raw buffer 不等于输出具有形式化隐私保证 | replay重复使用数据、HPO / test-based stop 的隐私成本若引入DP须另算；sigma是梯度方差上界（pp.7–9、15–16） |

相同  $`\epsilon`$  在不同邻接关系、 $`\delta`$ 、轮数、采样率和信任模型下不能直接比较。FFA-LoRA 在自己的 cross-silo DP-SGD 条件下受益，而 FLASC 在 central client-level DP-FedAdam 下发现冻结  $`A`$  可能降低效用（分别 p. 7 表 1 与 pp. 10–11 图 7–8）；两个结果不是同条件复现，也不构成简单互相否定。

## 选取定量结果时保留条件

| 论文 | 数字及指标 | 对照与关键条件 | 性质 |
| --- | --- | --- | --- |
| AdaLoRA | RTE Accuracy 87.36 vs 85.56 | 0.32M vs 0.33M 可训练参数；DeBERTaV3-base；GLUE 开发集；5 seeds；p. 7 表 1 | 离线微调评估 |
| DR-Encoder | Qwen / MMLU 56.20 vs 25.50 |  $`\epsilon=4`$  的 DR vs 带噪 LoRA；不能与非私有 LoRA 56.77 等同；p. 7 表 4 | 单机联邦模拟 / 离线 benchmark |
| FLASC | 约 16× 更快通信，达到 70% Accuracy | 20NewsGroups，下行 1/4、上行 1/64 密度，理想固定带宽，上传 / 下载速度比有变化；p. 7 图 3 | 传输时间模型，不是实测端到端训练 |
| FFA-LoRA | MNLI-m 78.81±0.8 vs 39.46±14.3% |  $`r=8`$ ，强异质性 3 clients， $`\epsilon=6,\delta=10^{-5}`$ ，20 runs；p. 7 表 1 | 离线联邦微调，均值 ± 标准差 |
| SVD-LLM | 完整压缩约 3.5 h vs ASVD 5.5 h | 20% 压缩 LLaMA-7B、A100；含顺序 LoRA 恢复，白化约 10 min；p. 19 表 13 | GPU 压缩流程时间 |
| SVD-LLM | 9254 tokens/sec，peak 7.43 GB | 从 7B 压到约 3B，A100，batch 32、sequence length 128；p. 19 表 12 | 具体硬件与 workload 的实际测量 |
| CG-FedLLM | MMLU Average 56.37 vs 25.22 | Qwen-7B，GDP  $`\epsilon=0.25`$  的 Compress vs 带噪 LoRA；完整 delta / sigma 未列明；p. 7 表 2 | 联邦模拟 / 离线 benchmark，非独立验证的隐私实现 |
| CG-FedLLM | C-Eval Average 26.6 vs 25.8 / 24.9 | LLaMA，表 2 第 1 组 Compress / LoRA / Cent；同表第 7 组基本 Compress 为 26.2，分别保留；p. 7 | 配置 / 行标签不同；不能推广为所有任务都比 CL / FL 高约 3 分 |
| PowerSGD+ | GLUE 原表 Avg 86.28 vs 85.73 / 85.70 | RoBERTa-Base，rank 4，4 GPUs，AdamW，10 epochs，无 DP；p. 6 表 1。按表内八项重算为 86.27625 vs 85.76250 / 85.76875；Full precision 也有均值差异 | 原文报告与整理者计算分列；无多 seed 不确定性，不能用差值证明显著性 |
| PowerSGD+ | C4 validation PPL 32.63 vs 32.57 | LLaMA-60M，rank 8，10k steps，restart 200，无 DP；p. 9 表 3 | 此配置 PowerSGD+ 比 PowerSGD 稍差；四个模型 / rank 配置并非全部领先 |
| ISER | Depth BD-Rate −66.87% vs TransTIC−33.81%；节省幅度相对增大97.78%（整理者计算） | TIC / KITTI / Depth Anything，四质量点，无DP；p.21表3，相同 TIC 基准；不是误差下降98% | 每图任务适配 / RD评估，与训练梯度通信无共同分母 |
| ISER | 5 epochs：mAP35.083、1.47s vs LoRA-comp35.278、1.18s | TIC open detection quality1，无DP；p.26表9；前者码率0.1050 vs0.1063 | 小预算存在速度 / 质量取舍，不能推广“始终全面领先” |
| FedALA-WR | practical CIFAR-10：91.40±0.25% vs FedALA91.25±0.14% | 4-layer CNN、20 clients、Dir0.10、private local test、五次重复、无DP；p.12表3 | +0.15百分点（整理者计算），未报告配对显著性；不是 LLM或统一全局test |
| FedALA-WR | 175.56±5.340min vs FedALA182.43±5.340min | Tiny-ImageNet、4-layer CNN、单节点2GPU、auto-break、无DP；p.15表5；同表FedAMP147.20min更快 | 约3.77%计时下降（整理者计算），排除公网延迟；不是所有基线最快 |

## 可借鉴思路与未验证组合

以下为**整理者推断**，不是作者报告的联合方法或已复现结果。

- 若重点是 task adapter 容量，AdaLoRA 的全局方向预算可作为研究起点；迁移到 FL 时要解决客户端方向对齐、重要性估计和聚合。
- 若重点是 cross-device 非对称通信，FLASC 将训练与传输表示解耦，值得比较 rank 与 sparsity 的联合配置。
- 若重点是 client-side DP-SGD 与 FedAvg 一致性，FFA-LoRA 的共享固定基底有清楚的代数依据，但要验证容量是否足够。
- 若重点是压缩器预训练开销，DR-Encoder 的统计量 / 合成梯度思路值得研究；需要先补齐这些统计量发布本身的隐私机制。
- 若重点是模型部署内存，SVD-LLM 直接压缩主干；与量化组合已有原文实验，但与本知识库其他联邦 / DP 方法的组合仍未验证。

- 若重点是学习传输表示，CG-FedLLM 的 TGAP / FAF 分阶段值得比较；须将真实梯度收集、压缩器权重和 FAF 消息纳入同一成本 / 隐私账本。
- 若重点是同步低秩梯度的子空间漂移，PowerSGD+ 的 EF / 周期性 safeguard 可作为研究起点；MSGD 理论不自动覆盖 learned encoder、Adam、客户端部分参与或 DP 噪声，且必须计入完整矩阵刷新。

### CG-FedLLM 与 DR-Encoder / FFA-LoRA 的直接阅读联系

CG-FedLLM 用真实时间序列因子训练压缩器（pp. 4–5、19）；DR-Encoder 用统计量和合成梯度（其 pp. 3–4、9）。后者减少的是预训练收集阶段传输，不能将该阶段数字与前者每轮 latent 元素比直接比较；统计量发布的隐私也需核实。不凭论文年份断言两者具体继承关系，也不把 DR 的 FedCG 对照当作已确认与本 v3 同配置。

CG 算法 1 分别求和两个因子再相乘（p. 5）；FFA-LoRA 说明双因子分别平均一般不等于权重增量平均，并以共享冻结基底消除这类额外项（FFA pp. 4–6）。AutoEncoder 改善因子重建不自动修复聚合代数差异。冻结基底、动态秩、稀疏传输或主干压缩与 CG 的联合方法均未验证。

### PowerSGD+ 的共同基底与收敛控制

PowerSGD+ 在同一步对 workers 使用共同投影基底，平均的是该基底下的坐标，因此平均后的压缩更新等于各压缩更新的平均（p. 4 算法 1、p. 13）；这与 FFA 的共享冻结因子有代数联系，但共同基底会更新，且训练对象为完整梯度。它不对应 CG 中各自可训练的双因子分别聚合。SVD-LLM 则对主干权重 / 白化校准目标做 SVD，并非本篇的全局 EF 校正更新（SVD-LLM pp. 3–5）。

本篇的最优 SVD 压缩满足收缩条件，其普通投影加周期刷新控制平均残差（pp. 3、13–18）。CG / DR 的 AutoEncoder 不因重建误差小就自动满足同一统一收缩条件；预训练成本、隐私发布范围与自适应基底的组合都需要另证。以上为有文献依据的整理者比较，方法组合仍为未验证研究设想。

### ISER 的秩预算与 FedALA-WR 的本地优化

ISER 借用 AdaLoRA 重要性与全局预算思想（ISER pp.11–13；AdaLoRA pp.4–6），区别是每图 TTFT / decoder SV 范围。原 ISER p.11 对 AdaLoRA“开始时一次定秩”的宽泛表述不符合 AdaLoRA 训练中动态调度，不能据此改写原方法。ISER 的 SVD-LoRA 分解适配增量，SVD-LLM 分解校准后的主干权重，任务、对象和预算不同。

FedALA-WR 的 replay 与 CG TGAP 的真实梯度库 / DR 的统计量合成先验不同；一个控制本地样本访问和目标，一个训练传输压缩器。FedALA-WR attention 加权也不消除 FFA 所证明的双可训练因子聚合交叉项。公开作者代码的 replay detach / norm 符号 / test-based stop 与期刊正文有差异（见该篇notes的固定commit），不能据可访问代码称已复现。

把 replay 与 FLASC / FFA / CG 组合、把 ISER 稳定性信号迁移到联邦停止均为**未验证研究设想**。应先统一模型 / 数据 / 参与 / 预算，验证 direction alignment、真实全流程字节、DP采样与发布范围，不作跨条件数值排名。

## 单光子 LiDAR 参数核查

九篇均不涉及单光子 LiDAR。探测器类型、阵列规模、探测距离、目标速度、SNR/SBR、平均每像素光子数、采集时间、重建帧率、空间分辨率、定位误差均为**不适用**；没有仿真 / 实测 / 离线重建的 LiDAR 数值可比较。ViT 输入图像尺寸、LLM tokens/sec 和模型训练时长不能替代这些物理参数。CG-FedLLM 的 SNR 是梯度重建信号 / 误差比，不是光子信号 / 背景统计。

[返回总览](README.md) · [版本 / 版权](NOTICE.md) · [验证与待补充项](verification.md)
