# Test-Time Fine-Tuning of Image Compression Models for Multi-Task Adaptability

## 文献信息与阅读对象

| 项目 | 记录 |
| --- | --- |
| 方法名 | LoRA-comp（与已收录 ISER 的前作关系；本文题名未冠此短名） |
| 作者，上传版顺序 | Unki Park、Seongmoon Jeong、Youngchan Jang、Gyeong-Moon Park、Jong Hwan Ko |
| 阅读版 / 出版 | CVF 提供的 **CVPR 2025 Open Access accepted version**，11 页；印刷页 4430–4440 |
| 正式 DOI | [10.1109/CVPR52734.2025.00418](https://doi.org/10.1109/CVPR52734.2025.00418)；[作者所在 Korea University 记录](https://pure.korea.ac.kr/en/publications/test-time-fine-tuning-of-image-compression-models-for-multi-task-/) |
| 官方全文 | [CVF PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Park_Test-Time_Fine-Tuning_of_Image_Compression_Models_for_Multi-Task_Adaptability_CVPR_2025_paper.pdf)；首页称除 watermark 外与 accepted version 相同，最终会议版在 IEEE Xplore |
| PDF 处理 | 未确认此 CVF 阅读版本允许第三方公开再分发，保存官方全文入口；不复制 `paper.pdf`，详见 [source.md](source.md) |
| 阅读范围 / 核对 | 2026-10-13；上传 11 页全文，包括 pp. 9–11 参考文献；上传件不含 supplement。本次 supplement 官方请求 403，未取得 / 未完整阅读它；未运行训练 |

页码均为上传 PDF **物理页码**；公式按目视 PDF 恢复，区分**原文**、**整理者归纳 / 计算**和**待核实**。原仓库 ISER 笔记中的相关前作引用只属书目关联；这次为本篇实际全文建立独立阅读记录，不记作重复附件。

## 摘要

**整理者归纳，pp. 1–5。** 用 SVD-LoRA 在测试时针对**当前图像和当前已知目标任务**微调人眼导向 learned image compression（LIC）编码器 / 解码器。先离线初始化共享的低秩适配模块，再每图执行 TTFT；编码侧更新全部低秩因子，解码侧仅更新 singular values，并把这小组 SV 量化 / 算术编码后加入图像 bitstream，接收方恢复 SV 构造适配解码器。

它解决 LIC 的 closed-set / open-set 单任务码流适配，实验对象是图像 bpp 与检测 / 分割 / 分类效用。没有联邦参与方、梯度上传或 DP。标题 multi-task adaptability 表示能分别切换多个任务，不表示一条码流对任意未知任务同时达到最优。

## 背景、已有方法不足与贡献

**原文，pp. 1–3。** Multi-task bitstream 会增加处理复杂度、单任务额外码率及任务间取舍；single-task bitstream 按目标任务生成码流，但 TransTIC 等需要任务特定 prompt 预训练，难以适配没有离线初始化的新任务。逐实例 decoder fine-tuning 又会产生传输适配权重的负担。本文将 decoder 的可发送变化约束为低秩增量中的 SV。

**原文贡献，pp. 2–5：** 测试时同时适配 encoder / decoder；采用 SVD-LoRA 只微调 / 传输 decoder SV 控制码流；允许通过通用分类任务初始化处理 open-set detection / instance segmentation。主文 TIC 是 transformer 实验；CNN 结果只在未取得的 supplement 被提及，不能当成本次读过的定量证据。

**边界，整理者归纳：** open-set 只是没有目标任务的离线适配初始化；TTFT 仍需访问目标 evaluator 的 intermediate features，知道目标任务，并使用目标网络的预训练表征。它不是无任务信息学习，也不是不用数据 / 不用任何预训练。

## 方法与核心公式

### SVD-LoRA 与共享初始化

**原文，p. 3 式 (1)、p. 4 式 (2)、图 2–4。**

$$
W=W_0+\Delta W=W_0+BA,\qquad
W=W_0+U\Sigma V^{\mathsf T},
$$

$U\in\mathbb R^{d\times r}$、$\Sigma\in\mathbb R^{r\times r}$ 为对角矩阵、$V\in\mathbb R^{k\times r}$，$r\ll\min(d,k)$；本文 r=4。此处是**增量参数化**，不是每次对大模型所有 pretrained 权重进行完整 SVD 的算法。低秩增量可合并入 $W_0$；合并后的前向路径不必再显式增加 adapter 层，但 TTFT 时间仍需计入编码。

Stage 1：closed-set 用指定目标任务学习初始 SVD-LoRA；open-set 用分类的共同初始化。Stage 2：encoder 训练 $U,\Sigma,V$，decoder 仅训练 $\Sigma$，decoder $U,V,W_0$ 固定。双方必须共享 Stage 1 初始化、backbone、SV 顺序和量化规则。每图适配 / SV 是 instance-specific，不是保存每个客户端的永久任务 LoRA。

### 码流、训练范围与损失

**原文，pp. 4–6 图 3、5，式 (3)。** Decoder SV 量化并算术编码后与图像码流一同传输，rank4 的额外 SV 码流据文中说明小于图像码流的 1%；该比例只对应给出的配置，没有给所有图像 / rank 的保证。

$$
\mathcal L=-\log p(\hat z)-\log p(\hat y\mid\hat z)+\lambda d(x,\hat x).
$$

注：上传式 (3) 的条件文本写 $p(\hat y\mid z)$，本文以量化 hyperprior $\hat z$ 表示概率条件，属于记号规范；不改动原件。$x,y,z$ 分别为图像、latent、hyperprior；人眼任务 distortion 为像素 MSE，machine vision 采用原图 / 重建图经目标 evaluator 后 intermediate-feature 的 perceptual loss。不是直接用标签监督每张 TTFT 图像。式中 log 底 / 像素归一化未在主式展开，bpp 和原始 loss 不可直接等同。

TIC 的 SVD-LoRA 只放在**主 encoder / decoder 的 Swin Transformer Blocks**，hyper encoder / decoder 不在指定调参范围。选 encoder 的 PEFT 是为减少 TTFT 的训练参数与开销；编码侧参数不用跟图像发送。先合并低秩权重再解码的路径与在编码机上通过 codec / evaluator 反传的训练时间是不同成本。

## 实验设置

**原文，pp. 5–6。**

| 项目 | 配置 |
| --- | --- |
| Codec / initializer | Flickr2W 预训练 TIC；open-set 通用分类 initializer |
| 数据 / evaluator | MS-COCO 检测 Faster R-CNN / 实例分割 Mask R-CNN；ImageNet-1K 分类 ResNet50 |
| Task settings | Closed detection / segmentation / classification；open detection / segmentation；open classification 因 initializer 就是分类而被排除 |
| 预算 | rank4、40 TTFT iterations / image；数量可调整 |
| 质量点 | TIC 四 quality levels，$\lambda=2,1,0.5,0.2$；共同比较 RD 曲线 |
| 比较对象 | TIC、full fine-tuning、TransTIC、UIC、TIC+prefilter / SFT / channel selection |
| 指标 | 分类 top-1、检测 / 分割 mAP、相对 TIC 的 BD-Rate / BD-mAP / BD-accuracy |
| 详细消融 | Open-set COCO detection、5,000 validation images、A100 80GB |
| 不适用 / 未报告 | 无 DP、隐私会计或真实网络链路；主文未给训练 seed / 多 seed 标准差、完整初始化训练超参数 |

BD-Rate 负值表示在给定效用区间相对 TIC 的平均码率降低，不是梯度压缩比。分类 BD-accuracy 数值 0.14 使用表 1 的 accuracy 尺度，不能自行写成 top-1 增加 14 百分点。

## 主要结果与适用范围

### 任务效用 / 码率

**原文，p. 7 表 1、图 6；下表均以原始 TIC 为 anchor。**

| 场景 | w/o TTFT：BD-Rate / BD效用 | w/ TTFT：BD-Rate / BD效用 | TransTIC：BD-Rate / BD效用 |
| --- | --- | --- | --- |
| Closed 实例分割 | −43.44% / mAP 1.99 | **−56.49% / 2.68** | −47.45% / 2.34 |
| Closed 目标检测 | −38.62% / mAP 2.17 | **−54.96% / 2.98** | −46.64% / 2.71 |
| Closed 分类 | −50.67% / accuracy 0.08 | **−70.04% / 0.14** | −58.76% / 0.10 |
| Open 实例分割 | −32.48% / mAP 1.97 | **−49.51% / 2.43** | −43.55% / 2.28 |
| Open 目标检测 | −29.61% / mAP 1.87 | **−48.94% / 2.69** | −39.60% / 2.23 |

p. 2 “more than 50% across all evaluated machine tasks”不能覆盖 open-set 两行，实际为约49%。**整理者归纳：** TTFT 比自身固定适配版改善；closed full fine-tuning 的表1 BD-Rate 分割 **−75.55%**、检测 **−66.00%**、分类 **−100%**，优于本方法在该表的若干值。因而“outperforms all competing approaches”不能解读为每项数值都优于 full fine-tuning。分类 −100% 应保留为原表结果，需核查 BD 插值 / 重叠区间，不当作无传输即可完成任务的已证明结论。

**原文，p. 8 图 7。** 视觉例子显示 TTFT 改善检测 confidence；其单图 confidence 高于 raw image 也不等于总体 mAP 超过原图或所有任务质量全面领先。

### 训练预算与时间

**原文，p. 7 表 2；open-set COCO detection，A10080GB，5,000图。**

| TTFT budget | Bit-rate，bpp | mAP | TTFT time，s |
| --- | --- | --- | --- |
| w/o TTFT | 0.09591 | 34.021 | — |
| 5 iterations | 0.106 | 35.28 | 1.18 |
| 10 iterations | 0.106 | 35.84 | 4.28 |
| 15 iterations | 0.107 | 35.88 | 5.86 |
| 40 iterations | 0.106 | 36.25 | 14.13 |

没有在表2标注独立 quality 值，不能直接与全部 RD quality 平均耗时或 ISER 的最大预算均值混比。TTFT 增加 mAP，也使本表 w/o / w 之间 bpp 上升；不是“码率、效用、计算同时无代价改善”。“early iterations have most impact”是特定任务观测；时间不严格等比，本文称 linear 应理解为近似。w/o time 的“—”不是0秒 / 已测 realtime性能。

## 消融与局限

**原文消融，pp. 7–8 图 8–9、表 2：**

- Encoder only、decoder only、both 与 w/o TTFT 比较：both 最好，decoder 适配对最优效用必要；主图无可精确抄录的完整数字表，不从曲线补小数。
- Decoder 全部 SVD-LoRA 因子 vs 仅 SV：训练全部因子会使码流 overhead 增大 **15.3×**（p. 8）。其口径需按原图额外码流解释，不写成总图像码流必然15.3×或耗时15.3×。
- 固定40 iterations 面向每张图，缺少本文内的动态秩、自动 early-stopping 或预算适应；ISER 是后续单独扩展。

**整理者评估：**

- 适配显著增加编码计算，表2 40-iteration TTFT=14.13s；适合能容忍每图训练的场景，不能用 decoder 前向高效宣称实时编码。
- 目标网络仍已知，且需要原图 / 目标 evaluator 提供 features；open-set不是任意未知任务的零信息泛化。
- 固定rank4与共享方向限制 decoder 的适配容量；SV 码流、初始化分发与发送双方状态需一致。
- 主文没有完整多 seed 稳健性、峰值内存、端侧硬件、实际网络通信 / 能耗实验，也没有形式化收敛证明。
- 单任务 bitstream 支持多任务切换，不是一个统一 representation 对所有任务同时无损。
- 主文提及 supplement 的 CNN 与 LoRA / SVD-LoRA 细节，但本次没取得补充文件；不移用后作 ISER 的实验结果填补前作未读信息。

## 复现信息与版本关系

**已取得 / 未执行。** 完整阅读上传主文和参考文献；核对首页题名 / 五作者、公式和表1–2；记录官方 CVF 全文及作者大学出版 DOI。首页 code/project page 在此 PDF 的 link annotation 中无可解析链接，本次未把未经确认的仓库写成官方代码。完整复现需要补齐 initialization 数据 / epochs、codec checkpoint、TTFT optimizer / learning rate、SV quantization / entropy coding、evaluator feature层、padding / crop、BD metric区间与脚本。

原仓库 [ISER笔记](../../2026-park-iser/notes.md) 的 six-author 2026 期刊稿为本篇 revised and expanded version；本篇五位作者含 Youngchan Jang，ISER 名单变化，不能混写。ISER 的动态秩 / early stopping / 多尺度 / 深度结果不是 CVPR2025 主文已给结果；新增独立目录只跟本次压缩包归类。

**整理者结论：** 应把“每图 encoder全因子 / decoder仅SV的SVD-LoRA适配”“额外SV位流”“测试时目标features与秒级编码成本”一起记录。它给的是任务导向图像 codec 适配证据，不能直接当作联邦 LLM 梯度压缩定理或隐私机制。

[来源记录](source.md) · [BibTeX](citation.bib) · [仓库总览](../../../README.md) · [跨论文比较](../../../comparison.md)
