# SVD-LLM: Truncation-aware Singular Value Decomposition for Large Language Model Compression

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 完整题名 | SVD-LLM: Truncation-aware Singular Value Decomposition for Large Language Model Compression |
| 作者 | Xin Wang, Yu Zheng, Zhongwei Wan, Mi Zhang（PDF p. 1；ICLR proceedings 同序） |
| 正式发表 | The Thirteenth International Conference on Learning Representations，ICLR 2025 |
| 实际阅读版本 | arXiv:2403.07378v5，2025-03-16，21 页；首个预印本发布于 2024-03-12；上传件页眉标 Published as a conference paper at ICLR 2025；正文、参考文献、附录完整 |
| DOI | 会议 DOI：所核对官方记录未提供；arXiv DOI：[10.48550/arXiv.2403.07378](https://doi.org/10.48550/arXiv.2403.07378)，属于预印本记录 |
| 官方来源 | [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3104e1ab39875cf54fe1eb4473e7c5a1-Abstract-Conference.html)；[OpenReview](https://openreview.net/forum?id=LNYIUouhdt)；[arXiv v5](https://arxiv.org/abs/2403.07378v5) |
| PDF、代码、引用 | [官方 v5 PDF](https://arxiv.org/pdf/2403.07378v5)；[官方代码](https://github.com/AIoT-MLSys-Lab/SVD-LLM)；[citation.bib](citation.bib)；[source.md](source.md) |

本次分析依据**用户上传 v5**；页码均为该 PDF 的物理页码。公开仓库未收录本地 `paper.pdf`，因为该上传版本的 arXiv 非独占分发许可不足以确认第三方再分发权。元数据与代码来源核对日期：2026-10-11。

**版本辨别**：本文 v5 的参数恢复方法为 **Parameter Update with Sequential Low-rank Approximation**，即顺序 LoRA 微调（p. 5），不是早期版本中 layer-wise closed-form update。作者仓库还包含 SVD-LLM V2，不能用 V2 的论文、命令或结果替代本次 v5。

## 摘要

SVD-LLM 用数据感知低秩分解压缩 LLM 权重。它对校准激活的 Gram matrix 做 Cholesky 分解，在白化坐标中对  $`WS`$  求 SVD，使截断奇异值与该层校准输出的 Frobenius 误差直接对应；随后分别对两个低秩因子做顺序 LoRA 微调恢复精度。论文评估七个模型、三个模型家族、7B / 13B / 30B 三个规模和十个数据集。LLaMA-7B 参数压缩 40% 时 WikiText-2 perplexity 为 9.27，ASVD 为 1407；但原模型为 5.68，说明相对基线优势不代表无精度损失（pp. 1–7）。

## 背景、不足与贡献

- **问题（原文）**：LLM 权重规模限制部署；低秩因子可用普通矩阵计算，无须将完整权重重新展开，且有降低 KV cache 的可能（pp. 1–3、7–8）。
- **现有方法不足（原文）**：vanilla SVD 忽略激活分布；FWSVD 估计 Fisher 信息成本高；ASVD 的对角归一化未让奇异值大小直接对应输出误差；截断后没有充分更新剩余参数（pp. 1–4）。
- **贡献（原文）**：truncation-aware data whitening；对两个低秩因子的顺序微调；多模型 / 多任务与真实 CPU / GPU 推理评估，并研究与量化的组合（pp. 2、5–10）。

## 方法流程、关键模块与公式

1. 从 WikiText-2 随机选校准文本，收集每个待压缩线性层的激活统计  $`XX^\top`$ ；可以增量累计，无须长期存储全部  $`X`$ （pp. 3、5）。
2. 对  $`XX^\top`$  做 Cholesky，得到  $`S`$ ；在白化坐标中对  $`WS`$  求 SVD，按目标秩截断小奇异值。
3. 将权重替换为两个低秩矩阵；固定其中一个、用 LoRA 微调另一个，再交换；将适配器合并回各自因子（p. 5；p. 14 算法 1–3）。
4. 推理时先乘右因子，再乘左因子；可选只缓存低秩 K/V 中间表示，需要时再展开（pp. 7–8）。

为了统一维度，记  $`W\in\mathbb R^{d\times n}`$ 、 $`X\in\mathbb R^{n\times N}`$ ， $`N`$  为校准激活列数。原文优化每层输出误差（p. 3，式 (1)）：

$$
\min_{\operatorname{rank}(W')\le r}\lVert WX-W'X\rVert_F.
$$

白化与低秩分解（pp. 4–5）：

$$
XX^\top=SS^\top,\quad
\widetilde X=S^{-1}X,\quad
\widetilde X\widetilde X^\top=I,\quad
WS=U\Sigma V^\top,
$$

$$
W_u'=U_r\Sigma_r^{1/2},\qquad
W_v'=\Sigma_r^{1/2}V_r^\top S^{-1},\qquad
W'=W_u'W_v'.
$$

 $`S\in\mathbb R^{n\times n}`$  为白化矩阵， $`U_r,V_r`$  是保留的奇异向量， $`\Sigma_r`$  为保留奇异值对角矩阵， $`W_u'\in\mathbb R^{d\times r}`$ 、 $`W_v'\in\mathbb R^{r\times n}`$ 。若满足上述白化关系，截断后的误差为（p. 5，式 (6) / Corollary 3.3）：

$$
\lVert WX-W'X\rVert_F^2=\sum_{i>r}\sigma_i^2.
$$

因此截断最小奇异值最小化**给定层、给定校准激活、给定秩**下的误差，不是模型总体任务损失的全局最优保证。上述求逆要求  $`S`$  可逆；Gram matrix 不满秩时的数值处理应核对实现，不能凭笔记自行认定仍有完全相同的等式（后一说明为整理者推断）。

顺序恢复（p. 5，式 (7)）：

$$
W_u'\leftarrow W_u'+B_uA_u,
\qquad
W_v'\leftarrow W_v'+B_vA_v.
$$

算法 3 先固定所有  $`W_v'`$ 、更新  $`W_u'`$ ，再固定更新后的  $`W_u'`$ 、更新  $`W_v'`$ （p. 14）。它保持低秩结构；不能误写为直接在完整  $`W'`$  上增加一个未合并的 LoRA 分支。

参数压缩率定义（p. 1 脚注；p. 7）：

$$
R_w=1-\frac{r(d+n)}{dn}.
$$

 $`R_w`$  是**删减参数的比例**，不是保留比例，和 FLASC 的通信密度意义相反。推理采用  $`Y=W_u'(W_v'X)`$ ，而不是先重构完整  $`W'`$ 。KV cache 的低秩表示可减少占用，但展开带来额外延迟（pp. 7–8、21）。

## 实验设置与评价指标

| 设置 | 原文信息 |
| --- | --- |
| 七个模型 | LLaMA-7B / 13B / 30B，LLaMA2-7B，OPT-6.7B，Vicuna-7B，Mistral-7B（p. 6） |
| 十个数据集 | WikiText-2、C4；OpenbookQA、WinoGrande、HellaSwag、ARC-e、PIQA、MathQA；TruthfulQA、GSM8K（p. 6） |
| 指标 | WikiText-2 / C4：perplexity ↓；六分类任务 individual / average accuracy ↑；TruthfulQA：BLEU ↑；GSM8K：Exact Match accuracy ↑（p. 6，表 1） |
| 校准与恢复数据 | 256 条随机 WikiText-2 校准样本；Alpaca 50K 样本用于参数恢复；模型评估用 LM-Evaluation-Harness（p. 6）；校准长度分析以 2048 tokens 为单位（p. 10，图 5） |
| 对比方法 | vanilla SVD、FWSVD、ASVD、FLAP；LLM-Pruner、SliceGPT、BlockPruner；PB-LLM、BiLLM、OneBit；StableLM-3B（pp. 6、9–10、19） |
| 消融标记 | SVD-LLM (W)：仅白化与截断；完整 SVD-LLM：另含顺序微调；SVD-LLM (U)：按消融描述使用常规 SVD 截断加顺序恢复（pp. 6、8–9） |
| 硬件 | NVIDIA A100；推理另测 AMD EPYC 7643 CPU（p. 6） |

任务效果、压缩时间是离线评估；吞吐与峰值显存是上述硬件上的实际测量。完整方法额外使用 50K 微调数据和 GPU 时间，因此与没有恢复微调的 SVD 基线比较时，应同时看 W-only 结果，不能称所有方法耗费相同训练数据或计算预算。

## 主要定量结果

LLaMA-7B、表 1（p. 6），accuracy 以 0–1 表示，不能误当作百分制：

| 压缩率 / 原文权重内存 | ASVD WikiText-2 PPL | SVD-LLM WikiText-2 PPL | SVD-LLM C4 PPL | SVD-LLM 六任务平均 Accuracy | SVD-LLM GSM8K EM |
| --- | --- | --- | --- | --- | --- |
| 0% / 13.5 GB，原模型 | 不适用 | 5.68 | 7.34 | 0.57 | 0.09 |
| 20% / 10.2 GB | 11.14 | 7.73 | 12.23 | 0.55 | 0.08 |
| 40% / 7.76 GB | 1407 | 9.27 | 15.63 | 0.50 | 0.07 |
| 60% / 5.35 GB | 57057 | 15.00 | 26.26 | 0.30 | 0.04 |
| 80% / 2.58 GB | 80425 | 31.79 | 43.71 | 0.16 | 0.02 |

20% 压缩时的 WikiText-2 PPL：LLaMA-13B 原模型 / SVD-LLM 为 5.09 / 6.43；LLaMA-30B 为 4.10 / 5.14（p. 7，表 3）。更大模型的绝对得分不能与 7B 按同一基线直接排名。

其他实验需注明条件：

- 同 7 GB 内存预算，SVD-LLM PPL 9.63、LLM-Pruner 21.68、SliceGPT 27.41、BlockPruner 43.05（p. 10，表 7）。
- SVD-LLM + QuIP# 2-bit：1.3 GB、PPL 9.83；OneBit：1.3 GB、10.20，但训练 / 恢复流程不同（p. 10，表 8）。
- A100、batch size 32、sequence length 128：由 7B 压缩得到的约 3B LLaMA 吞吐 9254 tokens/sec、peak memory 7.43 GB；独立预训练的 StableLM-3B 为 8463 tokens/sec、9.41 GB；两者架构与预训练不同，六任务平均 Accuracy 为 0.46 / 0.44，**不是每个任务都更高**，例如 PIQA 为 0.68 / 0.69（p. 19，表 12）。
- 20% 压缩 LLaMA-7B、A100：完整 SVD-LLM 约 **3.5 h**，白化部分约 10 min；ASVD 约 5.5 h（p. 19，表 13）。不能引用早期版本的“完整方法 15 min”替换 v5 结果。

图 3 在不同 batch / sequence length 下测 GPU / CPU tokens/sec；图 4 为 batch 32、生成 128 tokens 的 peak memory（pp. 8–9）。原文未给这些图所有柱子的完整数值表，本笔记不补造精确读数。权重内存、运行时 KV cache、峰值显存是不同指标。

## 消融与敏感性

- **两模块（原文）**：p. 9 表 4，40% 压缩时 ASVD / W-only / U-only / 完整方法 PPL 为 1407 / 13.11 / 19.28 / 9.27；说明各模块都有贡献。
- **顺序 vs 同时更新（原文）**：p. 21 表 15，80% 压缩时 SVD-LLM (NFT) 80.23，ASVD (SFT) 271，SVD-LLM (SFT) 31.79；SFT 指顺序微调，NFT 指 normal fine-tuning，表标题的重复标签存在笔误，应按行标签与正文解释。
- **校准集（原文）**：p. 10 表 6，20% 压缩时 WikiText-2 / C4 校准后的 WikiText-2 PPL 为 7.73 / 7.79；图 5 探索样本数与种子，作者称变化影响有限，但不等于任意领域校准都可无差别替换。
- **顺序（原文）**：p. 10 表 5，先  $`W_u'`$  后  $`W_v'`$  在 60% 压缩时 PPL 13.20，反序为 15.00；效果受具体配置影响，算法顺序和最终报告采用顺序应保存。

**上传件的不一致需保留**：p. 6 表 1 W-only 的 40% / 60% PPL 为 13.73 / 66.62，与 p. 9 表 4 的 13.11 / 42.30 不同，原文未解释；不能把不同表格混为同一实验。p. 18 显存例子用 fp32 的 “32” 直接换算 GB，bit / byte 换算存在疑点；本笔记不将 419 GB / 3.6 GB 当成独立验证的实测显存。

## 适用条件、局限性与作者后续工作

**适用条件（整理者归纳）**：有代表性校准激活；需要普通矩阵运算可执行的低秩模型；可接受一定压缩损失和恢复微调成本。理论误差针对校准分布，数值稳定性、谱衰减和模型形状都会影响实际效果。

**作者明确列出的三项局限与未来工作**（p. 21，A.11）：

1. 高压缩率仍明显损害精度，希望进一步改善，使方法自身更接近量化方法的精度。
2. KV cache 的低秩表示要恢复 key / value，增加计算并影响延迟，需要优化。
3. 即使 perplexity 较低，仍可能生成重复、低质量文本，需改善生成质量。

**整理者补充推断**：完整方法使用数据和梯度恢复，不是无需微调的纯截断方法；吞吐增益依赖 batch、sequence length 与硬件，不能由参数压缩率直接推出同等端到端 latency 加速；原文没有 DP、FL 或真实 LiDAR 重建实验。

## 官方代码、数据与复现信息

官方代码：[AIoT-MLSys-Lab/SVD-LLM](https://github.com/AIoT-MLSys-Lab/SVD-LLM)，PDF p. 1 明确提供。当前作者 README 区分白化 / 压缩、`LoRA.py` 顺序更新、评估流程；其顺序 LoRA 示例为 rank 8、2 epochs、learning rate  $`10^{-4}`$ 、batch 64、`yahma/alpaca-cleaned`。这些是 2026-10-11 核对的**当前 README 示例**，不是上传 PDF 给出的所有实验最终配置。

复现应锁定对应 ICLR 2025 v5 的代码 commit，保存模型 / tokenizer revision、校准数据的精确采样、sequence length、压缩率与保留秩、两个恢复阶段的训练设置和合并结果。当前仓库包含 V2，且 README 提醒 C4 原下载地址失效、另给下载途径；尚未验证该外部数据下载与全部权重可取得。本文没有完整依赖锁文件 / 所有随机种子结果和 checkpoints 的统一清单；未运行压缩或微调实验。

## 阅读总结

**原文解决的问题**：让数据感知的奇异值截断真正对应校准层输出误差，并用保持低秩结构的顺序微调恢复任务性能。

**值得借鉴（整理者归纳）**：在与任务输出相关的坐标系中衡量压缩损失；将白化、截断和恢复效果分别验证；比较权重规模、运行时缓存、吞吐与生成质量，避免只报告一个 perplexity。与 AdaLoRA 的联系是利用方向的重要性控制资源，但前者压缩主干、后者学习增量，目标和资源预算不同。

## 单光子 LiDAR 参数

不适用。本文测量的是 LLM 硬件吞吐、权重 / KV cache memory 与文本任务效果；tokens/sec、压缩用时、模型内存不能替换光子采集时间、重建帧率、SNR/SBR 或定位误差。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [全文与版本说明](source.md)
