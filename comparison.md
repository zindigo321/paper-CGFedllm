# 五篇论文的条件化比较

本表是**整理者归纳**，具体方法与数字以各篇笔记和其所标上传 PDF 页码为准。比较范围仅限五个实际上传全文；不是全领域综述。它们分别优化适配器容量、私有梯度压缩、传输稀疏性、聚合一致性与主干压缩，不能按一个 Accuracy / 通信倍数做统一排名。

## 问题、方法、条件与局限

| 论文 / 已读版本 | 核心问题 | 方法与压缩对象 | 实验条件 | 主要结果与出处 | 局限 / 适用边界 |
| --- | --- | --- | --- | --- | --- |
| [AdaLoRA](papers/2023-zhang-adalora/notes.md)，2023 v2 | 同预算下各层 / 模块容量分配不合理 | 可学习 SVD 增量、重要性评分、动态总秩；压缩任务增量容量 | centralized DeBERTaV3-base / BART-large；GLUE / QA / 摘要；无 FL / DP | SQuAD v2.0，0.08% 参数，F1 88.7 vs LoRA 87.5；p. 8 表 2 | 额外评分 / 正则 / 调度开销；无联邦 / DP 验证；正文和附录部分配置冲突 |
| [DR-Encoder](papers/2024-wu-dr-encoder/notes.md)，2024 v1 | 压缩器训练与梯度交换泄漏、预训练收集开销 | 梯度统计量 → Gaussian 合成 → AutoEncoder；编码 / 裁剪 / 加噪 / 聚合 / 解码 | LLaMA / Qwen 7B，Dolly / MMLU 微调；C-Eval / MMLU；作者主张 client-level DP | Qwen / MMLU，GDP $\epsilon=4$：56.20 vs 带噪 LoRA 25.50；p. 7 表 4 | 统计量发布隐私未完整说明；轮数 / 算子 / 字节数有疑点；未核实官方代码 |
| [FLASC](papers/2024-kuo-flasc/notes.md)，2024 v1 | LoRA 通信仍昂贵，冻结稀疏权重损害效用 | 稠密本地训练、上下行独立 Top-K 传输；服务端维持稠密状态 | cross-device 单机模拟，ViT-B-16 / GPT2-Small；4 任务；FedAdam / central client-level DP | 四任务约 3–10× 更少通信匹配 dense LoRA；pp. 6–7 图 2 | 实际网络端到端时间未测；仍需稠密适配器训练；DP 用模拟较大 cohort；不是 7B LLM 实验 |
| [FFA-LoRA](papers/2024-sun-ffa-lora/notes.md)，2024 v1 / ICLR | 分别聚合双因子产生误差，双噪声乘积与缩放不稳定 | 共享冻结随机 $A_0$，仅训练 / 聚合 $B$ | 3-client cross-silo，RoBERTa-Large，1000 rounds × 10 local steps；客户端 record-level DP-SGD | MNLI-m，$\epsilon=6,\delta=10^{-5}$：78.81±0.8 vs 39.46±14.3%；p. 7 表 1 | 冻结子空间限制容量；同预算不逐任务占优；参数减少不等于总计算量减半 |
| [SVD-LLM](papers/2025-wang-svd-llm/notes.md)，2025 v5 / ICLR | 权重 SVD 截断与校准输出误差不对应，截断后恢复不足 | Gram matrix 白化、$WS$ 的 SVD、两个低秩因子顺序 LoRA 恢复；压缩主干与可选 KV cache | 7 个模型、10 任务；256 校准样本、50K Alpaca 恢复；A100 / EPYC 7643 实测 | LLaMA-7B，40% 参数删减：WikiText-2 PPL 9.27 vs ASVD 1407；原模型 5.68；p. 6 表 1 | 高比例精度下降；恢复耗时；KV 展开延迟；PPL 不能完全代表生成质量；与早期版 / V2 不同 |

## 哪些资源数字可以比较

| 概念 | 在论文中表示什么 | 不能混淆的量 |
| --- | --- | --- |
| AdaLoRA 的 $b(t)$ / 参数比例 | 全局保留方向数 / 相对 full fine-tuning 的可训练参数量 | 实际训练 GPU 显存、传输字节、主干删减比例 |
| DR-Encoder 的 $6.10\times10^{-5}$ | AutoEncoder **预训练前收集阶段**传输数值个数之比；167,772,160 vs 10,240 | 全程总网络通信压缩比；原文 160 MB / 0.078 MB 的精度口径有疑点（p. 9 表 5） |
| FLASC 的 $d_{\mathrm{up/down}}$ | 上 / 下行**保留比例**；达到目标效用的累计通信 | 本地稠密训练 FLOPs；实际网络 wall-clock；不一定含协议 / 索引全部成本 |
| FFA-LoRA 的参数“减半” | 仅训练 $B$；方阵时 $rd/[r(d+k)]=1/2$ | 所有非方阵的精确减半；完整模型训练时间减半 |
| SVD-LLM 的 $R_w$ | 主干权重**删减比例**：$1-r(d+n)/(dn)$ | 保留比例、量化位宽、运行时 peak memory 或 KV cache 占用 |

这些比例的对象、阶段和分母不同，不能将 10×、一半、40% 和 $6.10\times10^{-5}$ 排为“哪个方法最省资源”。

## 隐私保护条件不是同一种实验

| 方法 | 保护对象与噪声位置 | 对服务器的信任 / 采样前提 | 尚需核实 |
| --- | --- | --- | --- |
| AdaLoRA | 未提供 DP 机制 | centralized PEFT | 无法据此主张隐私保护 |
| DR-Encoder | 作者称 client-level DP；客户端编码后裁剪加噪，再聚合 / 解码 | 按客户端采样，使用 GDP / RDP；预训练统计量也被分享 | 统计量是否私有化、完整 $\delta$、Qwen 轮数、Gaussian mechanism 的精确对象（PDF pp. 3–6、13–15） |
| FLASC | central / global client-level DP-FedAdam；服务端裁剪聚合后加噪 | 实际 Reddit 10 / FLAIR 200 clients，但预算用 1000 / 5000 simulated cohort | 报告预算与实际小 cohort 直接部署不等价；完整 accountant / $\delta$（pp. 10–11、20） |
| FFA-LoRA | record-level DP；客户端逐样本裁剪和加噪，发布更新前已 DP | 无须可信服务器；3 个机构持较多本地记录 | 全轮次客户端采样率 / DP step 核算、HPO 的完整隐私成本（pp. 3、7、16） |
| SVD-LLM | 未提供 DP；使用校准和微调数据 | 离线压缩 / 恢复 | 不能视为私有压缩算法 |

相同 $\epsilon$ 在不同邻接关系、$\delta$、轮数、采样率和信任模型下不能直接比较。FFA-LoRA 在自己的 cross-silo DP-SGD 条件下受益，而 FLASC 在 central client-level DP-FedAdam 下发现冻结 $A$ 可能降低效用（分别 p. 7 表 1 与 pp. 10–11 图 7–8）；两个结果不是同条件复现，也不构成简单互相否定。

## 选取定量结果时保留条件

| 论文 | 数字及指标 | 对照与关键条件 | 性质 |
| --- | --- | --- | --- |
| AdaLoRA | RTE Accuracy 87.36 vs 85.56 | 0.32M vs 0.33M 可训练参数；DeBERTaV3-base；GLUE 开发集；5 seeds；p. 7 表 1 | 离线微调评估 |
| DR-Encoder | Qwen / MMLU 56.20 vs 25.50 | $\epsilon=4$ 的 DR vs 带噪 LoRA；不能与非私有 LoRA 56.77 等同；p. 7 表 4 | 单机联邦模拟 / 离线 benchmark |
| FLASC | 约 16× 更快通信，达到 70% Accuracy | 20NewsGroups，下行 1/4、上行 1/64 密度，理想固定带宽，上传 / 下载速度比有变化；p. 7 图 3 | 传输时间模型，不是实测端到端训练 |
| FFA-LoRA | MNLI-m 78.81±0.8 vs 39.46±14.3% | $r=8$，强异质性 3 clients，$\epsilon=6,\delta=10^{-5}$，20 runs；p. 7 表 1 | 离线联邦微调，均值 ± 标准差 |
| SVD-LLM | 完整压缩约 3.5 h vs ASVD 5.5 h | 20% 压缩 LLaMA-7B、A100；含顺序 LoRA 恢复，白化约 10 min；p. 19 表 13 | GPU 压缩流程时间 |
| SVD-LLM | 9254 tokens/sec，peak 7.43 GB | 从 7B 压到约 3B，A100，batch 32、sequence length 128；p. 19 表 12 | 具体硬件与 workload 的实际测量 |

## 可借鉴思路与未验证组合

以下为**整理者推断**，不是作者报告的联合方法或已复现结果。

- 若重点是 task adapter 容量，AdaLoRA 的全局方向预算可作为研究起点；迁移到 FL 时要解决客户端方向对齐、重要性估计和聚合。
- 若重点是 cross-device 非对称通信，FLASC 将训练与传输表示解耦，值得比较 rank 与 sparsity 的联合配置。
- 若重点是 client-side DP-SGD 与 FedAvg 一致性，FFA-LoRA 的共享固定基底有清楚的代数依据，但要验证容量是否足够。
- 若重点是压缩器预训练开销，DR-Encoder 的统计量 / 合成梯度思路值得研究；需要先补齐这些统计量发布本身的隐私机制。
- 若重点是模型部署内存，SVD-LLM 直接压缩主干；与量化组合已有原文实验，但与本知识库其他联邦 / DP 方法的组合仍未验证。

## 单光子 LiDAR 参数核查

五篇均不涉及单光子 LiDAR。探测器类型、阵列规模、探测距离、目标速度、SNR/SBR、平均每像素光子数、采集时间、重建帧率、空间分辨率、定位误差均为**不适用**；没有仿真 / 实测 / 离线重建的 LiDAR 数值可比较。ViT 输入图像尺寸、LLM tokens/sec 和模型训练时长不能替代这些物理参数。

[返回总览](README.md) · [版本 / 版权](NOTICE.md) · [验证与待补充项](verification.md)
