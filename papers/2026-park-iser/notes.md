# ISER: Instance-Specific Early Stopping with Dynamic Low-Rank Adaptation for Learned Image Compression

## 文献信息与阅读对象

| 项目 | 记录 |
| --- | --- |
| 完整英文题名 | ISER: Instance-Specific Early Stopping with Dynamic Low-Rank Adaptation for Learned Image Compression |
| 作者，按上传版顺序 | Unki Park、Seongmoon Jeong、Sangmin Kim、Jeungsub Lee、Gyeong-Moon Park、Jong Hwan Ko |
| 正式出版 / 阅读版 | Electronics **2026, 15(17), 3807**；实际阅读上传的 33 页期刊 PDF，含正文与参考文献，无另列附录 |
| 日期 | Received 2026-07-14；Revised 2026-08-11；Accepted 2026-08-18；Published 2026-08-25；PDF 创建 / 修改日期均为 2026-08-25，时区与时间另见 source |
| DOI / 官方记录 | [10.3390/electronics15173807](https://doi.org/10.3390/electronics15173807)；[MDPI](https://www.mdpi.com/2079-9292/15/17/3807)；[出版社提交的 Crossref](https://api.crossref.org/works/10.3390/electronics15173807) |
| 版本关系 | 首页明确为 CVPR 2025 **Test-Time Fine-Tuning of Image Compression Models for Multi-Task Adaptability**（LoRA-comp）的 revised and expanded version；该前作作者包括 Youngchan Jang，与本篇六人名单不同，不能混写 |
| 许可 / 原件 | 上传期刊版为 **CC BY 4.0**，保留署名、来源和许可，原样收录 [paper.pdf](paper.pdf)；完整身份见 [source.md](source.md) |
| 引用 | [citation.bib](citation.bib) 的 `park2026iser_electronics` 引用本篇；`park2025loracomp_cvpr` 仅用于关联前作的正式书目，不计作新增已读论文 |
| 核对日期 / 范围 | 2026-10-12；阅读全文 33 页；页码均为上传 **PDF 物理页码**。未运行训练或复现实验 |

数字和公式以本上传期刊版为依据。以下区分**原文报告**、**整理者归纳**、**整理者计算**、**代码静态观察**和**待核实**。正式出版元数据已核对；后续直接读取官方全文入口取得 PDF，出版社文件、附件与仓库副本的 33 页、字节数和 SHA-256 均一致。

## 摘要

**整理者归纳，PDF pp. 1–4、6–16。** ISER 研究 learned image compression（LIC）对不同视觉任务的适配。它沿用 LoRA-comp 的两阶段 SVD-LoRA：先初始化适配参数，再为每一张待编码图像执行 test-time fine-tuning（TTFT）。编码器更新全部 SVD-LoRA 因子，解码器仅更新 singular values（SVs）；解码侧 SV 随图像码流发送，以控制额外码率。

新增机制为 instance-specific rank adaptation（ISRA）、instance-specific early stopping（ISES）和 multi-scale training strategy（MSTS）。先用 256×256 patch 训练，利用解码侧重要性评分的时间变化决定降秩时机；达到全局目标预算后进入全分辨率后训练。研究对象是**图像码流、任务适配和每张图像的编码计算**，没有联邦客户端、梯度压缩器或 DP 机制。

相对 LoRA-comp 的“最高 7%”指特定条件下 BD-Rate **节省幅度的相对增长**；相对 TransTIC 的“最高 98%”同样是 BD-Rate gain 的相对比较。它们不是准确率增长，也不是把码流再减少 7% / 98%。秒级 TTFT 编码与毫秒级解码需分别看待，见下文。

## 背景、已有方法不足与贡献

**原文，pp. 2–6。** Human-centric codec 优化人眼重建质量，不保证检测、分割或深度任务的效用。Multi-task bitstream 尝试一条码流支持多个任务；本文属于 single-task bitstream：每次面向一个已知目标任务生成码流，不能把它写成“一次编码同时兼顾任意任务”。TransTIC / Adapt-ICMH 需要预训练任务适配模块；LoRA-comp 用每实例 TTFT 扩展到未做数据集级任务预训练的任务，但使用固定秩、固定 epoch 和固定图像尺度。

**原文贡献，pp. 3–4、9–14：**

- ISRA 按每张图像的梯度动态分配解码器 SV 预算，改善统一层秩的适配限制。
- ISES 根据同一优化过程中产生的稳定性信号安排实例训练长度，MSTS 在 patch 与原分辨率间切换。
- 用 CKA 描述基准任务与下游网络的表征距离，并评估更远的深度估计任务；还比较 closed-set 与 open-set 重建的特征相似性。
- 验证 TIC（Transformer）和 Cheng2020（CNN）两种 codec 上的适配；低秩增量可合并进权重，减少推理路径额外运算。

**边界，p. 16：** open-set 的含义是没有针对最终任务保存离线数据集级适配参数；**测试时仍知道目标任务，并使用其冻结 evaluator 的中间特征**。并非无任务信息、无目标网络、无预训练或普适零成本适配。编码需要访问原图与目标 evaluator，解码只接收码流 / SV 和共享模型配置。

## 两阶段方法与核心公式

### 初始化、实例优化与解码

**原文，pp. 6–9、14–16，图 2–4、7。** Stage 1 初始化 SVD-LoRA：closed-set 使用目标任务；open-set 使用 ImageNet 预训练 ResNet50 作为共同基础。Stage 2 针对当前图像更新适配器；open-set 损失为原图和重建图经过目标任务冻结 evaluator 后的 feature-level MSE，不读取任务 ground-truth label / 输出作为 TTFT 监督。该说明不表示第一阶段也不使用训练数据。

主 encoder / decoder 插入 SVD-LoRA，hyper encoder / decoder 不属于本文指定的适配范围。TIC 只改主路径 Swin Transformer Blocks，Cheng2020 只改主路径 CNN layers（pp. 14–15）。原式 (2)，p. 8：

$$
W=W_0+\Delta W=W_0+U\Sigma V^{\mathsf T}.
$$

其中 $`U\in\mathbb R^{d\times r}`$ 、 $`\Sigma\in\mathbb R^{r\times r}`$ 为可学习对角矩阵、 $`V\in\mathbb R^{k\times r}`$ 。它是**可学习增量的分解参数化**，不能假定每次 TTFT 都对原始主干权重做完整 SVD，也不能把可学习 SV 直接当成当前主干的真实有序奇异值。

Stage 2 编码器训练 $`U,\Sigma,V`$ ，解码器只训练 $`\Sigma`$ ，共享的解码侧 $`U,V,W_0`$ 保持。将解码侧 SV 量化、熵编码并加入图像码流，接收方恢复 SV 后组成适配 decoder，重建图像再执行下游任务（pp. 7–9）。编码侧参数不必发送；双方必须事先具有相同 codec、初始化和 SV 解释规则。每张图像之后重新回到共同初始化，适配参数不作为下张图像的持续学习状态（p. 16；代码的 reset 机制见后文）。

### Rate–distortion 目标与指标口径

原式 (1)，pp. 7–8：

$$
\mathcal L=-\log p(\hat z)-\log p(\hat y\mid\hat z)+\lambda d(x,\hat x).
$$

$`x`$ 为原图、 $`y`$ 为 latent、 $`z`$ 为 hyperprior；帽符号对应量化 / 重建变量。前两项是概率模型的码率项，人眼任务以像素 MSE 度量失真，机器任务用冻结网络的特征失真。正文没有在式 (1) 标明对数底和像素归一化；写成数值 bpp 时必须落实这些细节，不能把未归一化 loss 本身当作已测传输字节。

| 指标 | 本文用途与方向 | 需要保留的区别 |
| --- | --- | --- |
| bpp / bitrate | 每像素码率，越小越好 | 图像部分、SV 部分、总码率；是否为概率估计或真正编码字节还需核对实现 |
| BD-Rate | 同任务质量区间内，RD 曲线的平均码率差，负数代表相对基准节省 | 曲线区间 / 插值、共同 human-centric backbone 基准；不是参数删减比例、梯度压缩比或分类准确率 |
| BD-mAP / BD-Acc. / BD-Error | 平均任务效用差；mAP / Acc. 越高、Error 越低越好 | 检测和分割 mAP、分类 top-1、深度 absolute relative error 的单位不同 |
| 编码时间 | 图像划分、TTFT / 降秩 / 后训练、SV 量化与辅助码流、下游推理，p. 16 | 每实例秒数；不能用单次前向 kMACs 代表所有训练反向计算 |
| 解码时间 | codec 推理 + 下游任务推理，p. 16 | 毫秒数；不等同编码时间，也未包含真实网络传输 |
| CKA | 冻结网络特征相似性，pp. 19–22 | 表征距离代理；不是 mAP、泛化证明或多 seed 置信度 |

所有实验无 DP；隐私预算 $`\epsilon,\delta`$ 均**不适用**。本文 $`\delta`$ 是学习率， $`\tau`$ 是收敛信号阈值；高斯输入噪声是鲁棒性测试，不是差分隐私噪声。

### ISRA 与 ISES：评分、稳定性、预算和停止

原文 p. 12 算法 1、式 (3)–(4)，p. 13 式 (5)–(6)。以下把层集合的基数显式写入预算，是整理者的记号规范；原文预算中的 K 表示层数。令 $`\mathcal K`$ 为 decoder SV 层集合， $`r_k^{(t)}`$ 为层 k 当前活跃分量数。原式仅以 AdaLoRA 的重要性函数 $`s`$ 指代评分，没有在本文展开完整灵敏度 / EMA 公式：

$$
S_{k,i}^{(t)}=s(\sigma_{k,i}^{(t)}).
$$

$$
\Delta^2S_{k,i}^{(t)}=\left|S_{k,i}^{(t)}-2S_{k,i}^{(t-1)}+S_{k,i}^{(t-2)}\right|.
$$

$$
C^{(t)}=\sum_{k\in\mathcal K}\sum_{i=1}^{r_k^{(t-1)}}\Delta^2S_{k,i}^{(t)}.
$$

若 $`C^{(t)}<\tau`$ 且当前总秩超出目标，触发全局降秩。原式 (6) 的取整符号已目视确认是 **floor**：

$$
m^{(t)}=\max\left(\left\lfloor\rho\sum_{k\in\mathcal K}r_k^{(t-1)}\right\rfloor,\lvert\mathcal K\rvert r_{\mathrm{target}}\right).
$$

**整理者归纳：** 将所有层分量按 $`\Delta^2S`$ 从小到大排序，删除总预算之外的分量；小二阶变化表示更稳定，不等价于较小权重、较小梯度或较低瞬时重要性。达到总目标预算后停止 rank-adaptation 阶段。 $`r_{\mathrm{target}}=4`$ 在这个算法中定义的是**每层平均预算 / 总预算换算值**；全局筛选本身不强制每层恰好保留 4 个分量。

正文另加 5-epoch warm-up 和 10-epoch post-training；算法 1 简写只显示至少三个 epoch 后评分和总预算停止，未完整列出 warm-up、尺度切换、post-training、预算耗尽时的处理（pp. 12–14、16）。不能将其第 21 行写成“所有计算立刻结束”；实际框架达到停止点后还要做全图后训练。

**MSTS，p. 14：** warm-up / rank adaptation 采用不重叠 256×256 patch，batch 数量按数据集分辨率确定；进入 post-training 后改原图、batch 1。这里的“低分辨率”主要是裁 patch，不能自行写成等比例缩小整图。全分辨率保证上下文，patch 便于优化但丢失跨 patch 全局上下文。

**待核实的算法 / 信令差异：** p. 28 和表 14 说明“所有 decoder SV 层最终都是 rank 4，所以无需 layer-wise rank / mask / index”，而 p. 12 算法、p. 13 的 global sorting、p. 24 图 13 的非均匀秩设计支持不同层保留不同数量。即使总秩固定为 $`4\lvert\mathcal K\rvert`$ ，也不直接推出每层方向及位置可由接收方确定。可能通过固定形状零值 SV 流保持位置，但需确认其零值编码 / 位置成本；本笔记保留两种陈述，不补造协议。

## 实验设置

**原文报告，pp. 14–17。**

| 项目 | 配置 |
| --- | --- |
| LIC backbone | TIC / Cheng2020，使用 CompressAI 的预训练模型；正文分别说明 Flickr2W / ImageNet 的 backbone 训练来源 |
| 任务与完整评估集 | COCO-2017 validation **5000** 张：Faster R-CNN 检测 / Mask R-CNN 实例分割；ImageNet-1K validation **50,000** 张：ResNet50 分类；KITTI Eigen test **697** 张：Depth Anything 深度 |
| open-set | Stage 1 共同 ResNet50 初始化；Stage 2 使用目标冻结 evaluator 的特征 MSE，无任务标签；检测、实例分割、深度 |
| closed-set | 目标任务初始化；与 LoRA-comp 比较检测 / 实例分割 / 分类 |
| 质量与训练预算 | 四质量点，正文 $`\lambda=2,1,0.5,0.2`$ ；TTFT 最大预算 40 epochs；实际长度按实例调整；学习率 $`5\times10^{-3}`$ |
| 秩与稳定性 | encoder 固定 4；decoder 初始 8、target 4； $`\rho=0.8`$ ；四质量阈值 $`4\times10^{-7},2\times10^{-7},9\times10^{-8},3\times10^{-8}`$ ；warm-up 5、post-training 10 epochs |
| 硬件 | 主机 4×RTX 4090（24 GB）、AMD EPYC 7313 16-Core、256 GB RAM；编码 / 解码各用单 GPU |
| 峰值显存 | TIC 实例分割：编码 17.79 GB、解码 5.94 GB；特定任务 / 实现，不表示边缘设备实测 |
| 对照 | Human-centric TIC / Cheng2020、TransTIC、Adapt-ICMH、LoRA-comp；质量点 / 图像集按本文条件对齐 |
| 隐私 / 不确定性 | 无 DP；大多数 RD 主表未提供跨 seed 标准差；表 4 为跨图像 CKA 分布，表 5 单独提供五次独立运行统计 |

四质量点的 BD 指标需在共同曲线区间解释；原文未给完整拟合实现。CKA 两类实验也要分开：p. 19–20 图 10 用 **CIFAR-10** 作为网络间共同 probing dataset，层对应 ResNet50 layers 1–4 / detection backbones / Depth Anything reassembly；p. 21 表 4 用 **COCO-2017、检测、quality 1**，按每张图像的空间位置计算 closed/open reconstructions 的末层特征 CKA。前者跨网络平均，不是后者跨图像平均。

## 主要结果与适用范围

### 与 LoRA-comp：TIC、四质量点、无 DP

下表前两列为**原文报告**（p. 17 表 2、p. 18 图 8，基准为 human-centric TIC）。最后两列为**整理者计算**：BD-Rate 百分点差 / 节省幅度相对增长，不是两种 adapted codec 在相同 mAP 下重新拟合的独立 BD-Rate。

| 任务 / 条件 | LoRA-comp：BD-Rate / BD 效用 | ISER：BD-Rate / BD 效用 | BD-Rate 差，百分点 | 节省幅度相对增加 |
| --- | --- | --- | --- | --- |
| COCO 检测，closed | −54.96% / BD-mAP 2.98 | −57.86% / 3.26 | −2.90 | 5.28% |
| COCO 实例分割，closed | −56.49% / BD-mAP 2.68 | −58.39% / 2.77 | −1.90 | 3.36% |
| ImageNet 分类，closed | −70.04% / BD-Acc. 0.14 | −70.85% / 0.14 | −0.81 | 1.16% |
| COCO 检测，open | −48.94% / BD-mAP 2.69 | −50.49% / 2.93 | −1.55 | 3.17% |
| COCO 实例分割，open | −49.51% / BD-mAP 2.43 | −52.86% / 2.67 | −3.35 | **6.77%** |

最后一行解释原文四舍五入后的“最高约 7%”： $`(52.86-49.51)/49.51\times100\%=6.77\%`$ 。不表示分割 mAP 增加 7 分。图 8 的单实例平均编码时间按任务分别为 16.97→9.40、16.12→9.19、16.78→9.87、16.85→10.68、15.93→10.27 s。最大降幅来自 closed-set detection：**整理者计算** $`(16.97-9.40)/16.97=44.61\%`$ ，原图写 44%；保留原文近似，不擅改图标注。

Cheng2020 的 p. 18 图 9 对 closed/open detection 报告约 2% / 5% BD-Rate gain 的相对提高，以及约 43% / 38% 编码时间下降；并没有给与表 2 相同完整数值表。本笔记不从曲线读出更多小数，也不推成所有 CNN / 所有任务结论。

### Open-set 对 TransTIC / Adapt-ICMH：TIC、四质量点、无 DP

**原文报告，p. 21 表 3；COCO / KITTI 与冻结 evaluator 见实验配置。** 所有 BD-Rate 都以 human-centric TIC 为参照。

| 任务 | ISER：BD-Rate / BD 效用 | TransTIC：BD-Rate / BD 效用 | Adapt-ICMH：BD-Rate / BD 效用 |
| --- | --- | --- | --- |
| COCO 检测 / Faster R-CNN | −50.49% / BD-mAP 2.93 | −39.60% / 2.23 | −40.09% / 2.58 |
| COCO 实例分割 / Mask R-CNN | −52.86% / BD-mAP 2.67 | −43.55% / 2.28 | −43.35% / 2.35 |
| KITTI 深度 / Depth Anything | −66.87% / BD-Error −0.020 | −33.81% / −0.011 | −45.73% / −0.012 |

深度行“98%”的**整理者计算**为 $`(66.87-33.81)/33.81\times100\%=97.78\%`$ ，它是节省幅度相对增大，BD-Rate 差为 **33.06 百分点**，不是 98% 绝对节省或深度误差下降 98%。

**原文报告，p. 20 图 11：** ISER / TransTIC 的检测解码 70.9 / 80.1 ms，分割 71.8 / 79.3 ms，深度 23.5 / 29.1 ms；深度降幅 **整理者计算** $`(29.1-23.5)/29.1=19.24\%`$ ，对应原文 19.2%。它们含下游推理，并非测量网络链路。TransTIC / Adapt-ICMH 不做每图 TTFT，编码开销小；ISER 的适配优势以一次秒级编码换取多次解码的效率，不适合直接宣传为实时编码。

### 表征与训练长度的不确定性

| 量 / 条件 | 原文报告 | 出处 / 解释 |
| --- | --- | --- |
| 图 10 ResNet50 与检测 / 分割 / 深度的相对 mCKA | 86.6% / 86.3% / 53.5%；自身跨层均值 0.0381 | p. 20；CIFAR-10 probe，归一化参照是自身平均，不应把 53.5% 当绝对 CKA |
| ISER / LoRA-comp 的 closed–open CKA | mean 0.4400 / 0.4230；std 0.3395 / 0.3574 | p. 21 表 4；COCO 检测 quality 1，**跨图像**波动，不是 seed 标准误 |
| 单次运行停止 epoch / 编码秒数 | mean 25.70 / 9.92；std 6.35 / 2.29；范围 [14,40] / [6.61,16.00] | pp. 21–22 表 5，COCO 5000 实例，TIC open detection quality 1 |
| 五次独立运行的实例均值 | epoch 24.78±0.66；时间 9.66±0.15 s | p. 22 表 5；此处 ± 是 run-to-run std；与单次图像差异分开 |

更接近 closed-set 表征是本文的代理证据；不等于找到全局最优，也不能用表 4 的均值差证明显著优越。表 5 有五次运行，不能把它的误差条移到全部 RD 结果。

## 消融、泛化与资源分析

### 组件存在效果 / 速度取舍

**原文报告，p. 22 表 6；TIC、open-set、无 DP；时间为任务平均。**

| 配置 | 平均编码 s/图 | 检测 BD-Rate / BD-mAP | 分割 BD-Rate / BD-mAP | 深度 BD-Rate / BD-Error |
| --- | --- | --- | --- | --- |
| ISRA only | 12.6 | −52.46% / 3.09 | −54.66% / 2.87 | −70.25% / −0.022 |
| ISRA + ISES | 11.5 | −51.33% / 3.02 | −53.49% / 2.73 | −67.62% / −0.021 |
| ISRA + ISES + MSTS | 8.16 | −50.49% / 2.93 | −52.86% / 2.67 | −66.87% / −0.020 |

完整框架更快，但此表中 BD 效用低于 ISRA only；三组件不构成“同时提高所有指标”。pp. 23–24 解释 additive ablation 的依赖关系，没有做完整 factorial ablation。表 8 / 10 / 11 的 10.68 s 是检测任务时间，表 5 / 9 的 9.92 s 是 quality 1，不能与表 6 的 8.16 s 直接判定矛盾或混成一个默认耗时。

| 消融 | 原文观察与选取数值 | 配置 / 出处 |
| --- | --- | --- |
| 动态 vs 固定层 | detection BD-Rate ISRA −52.46%，Fixed-Front −49.64%、Mid −50.71%、Back −51.82%；Back 的 depth −70.15% 接近 ISRA −70.25% | p. 24 表 7 / 图 13；TIC 28 层，固定前 / 中 / 后 14 层；该表是 ISRA only 条件，不是完整 ISER 主结果 |
| warm-up / post-training | 5/10：−50.49%、10.68 s；10/10：−51.17%、13.52 s；10/5：−46.25%、13.09 s | p. 25 表 8；open detection，速度与效用取舍 |
| 初始 decoder 秩 | 6：−49.03%、8.31 s；8：−50.49%、10.68 s；12：−50.37%、13.65 s | p. 26 表 10；target 4，并非起始秩越高越好 |
| 降秩比例 | 0.6：−48.79%、9.24 s；0.8：−50.49%、10.68 s；0.9：−50.25%、12.12 s | p. 27 表 11；open detection |
| 阈值 / loss 相关性 | 全质量自适应阈值优于给出的两个统一阈值配置； $`C^{(t)}`$ 与 loss 的 per-instance Pearson 为 0.71±0.09 | pp. 25–27 表 11 / 图 14；相关性是代理，未证明任意模型下的收敛判据 |

### 较小 TTFT 预算不保证每项领先

**原文报告，p. 26 表 9；TIC、COCO open detection、quality 1、无 DP。**

| TTFT 预算 | LoRA-comp：bpp / mAP / 秒 | ISER：bpp / mAP / 秒 |
| --- | --- | --- |
| 5 epochs | 0.1063 / 35.278 / 1.18 | 0.1050 / 35.083 / 1.47 |
| 10 epochs | 0.1059 / 35.838 / 4.28 | 0.1050 / 35.613 / 2.93 |
| 40 epochs | 0.1058 / 36.245 / 14.13 | 0.1050 / 36.343 / 9.92 |

5 epochs 的 ISER 更慢且 mAP 更低；10 epochs 的 ISER mAP 也稍低，虽码率 / 时间较小。因此不能写“所有预算下全面领先”。w/o TTFT 两者都是初始化阶段的 mAP 34.021；raw TIC 为 31.603。原表零 TTFT 的时间是“—”，并未给实时 FPS 或嵌入式实测，不能把正文 real-time-capable 的部署讨论当已测性能。

### 输入退化测试不是 DP 或通用 OOD 证明

**原文报告，pp. 27–28 表 12；COCO 随机 100 张、TIC open detection、quality 1，不是全部 5000 张；无 DP。**

| 条件 | TIC：bpp / mAP | ISER：bpp / mAP | 报告的 mAP 差 |
| --- | --- | --- | --- |
| 原图 | 0.0924 / 39.93 | 0.119 / 44.58 | +4.65 |
| Blur，kernel 9、std 2.5 | 0.0552 / 30.06 | 0.077 / 38.31 | +8.25 |
| Noise，std 0.02 | 0.0931 / 41.58 | 0.114 / 44.73 | +3.15 |
| Noise，std 0.05 | 0.0946 / 39.58 | 0.100 / 41.04 | +1.46 |

ISER 保持给定配置下的正增益，但比较两者的 bpp 不相同；这不是固定码率的独立鲁棒性证明。较强噪声下增益收窄，说明单图梯度信号质量影响方法。没有检测对抗攻击、所有退化类型或隐私泄漏。

### 单次推理计算、参数与额外码流

**原文报告，p. 28 表 13；TIC，encoder / decoder 分列。**

| 方法 / 阶段 | kMACs/pixel：enc / dec | 参数 M：enc / dec |
| --- | --- | --- |
| TIC | 142.31 / 142.53 | 3.64 / 3.86 |
| TransTIC | 332.03 / 202.60 | 5.24 / 3.89 |
| LoRA-comp | 142.31 / 142.53 | 3.72 / 3.94 |
| ISER 编码侧 TTFT 模型 | 142.31 / 142.53 | 3.72 / 3.99 |
| ISER 解码侧 inference | — / 142.53 | — / 3.94 |

正文称参数约增加 2% / 3%；按 ISER 编码阶段表内小数重算约 **2.20% / 3.37%**，解码 inference 相对 TIC 约 **2.07%**（整理者计算）。四舍五入 / 阶段不同，不把文字近似数字直接混用。MACs 是推理复杂度口径，未涵盖所有 TTFT 前后向、梯度评分、patch 和 evaluator 的累计开销。

**原文报告，p. 29 表 14；四质量点，SV overhead 按原表保留。**

| open-set 任务 | SV bitrate，bpp | Q1 / Q2 / Q3 / Q4 报告的 SV overhead |
| --- | --- | --- |
| COCO 检测 | 0.0021 | 2.05% / 1.46% / 1.04% / 0.67% |
| COCO 分割 | 0.0020 | 1.73% / 1.24% / 0.86% / 0.58% |
| KITTI 深度 | 0.0014 | 0.80% / 0.62% / 0.43% / 0.29% |

十二个**报告比例**的算术平均为 **0.98083%**，对应正文 0.98%（整理者计算）；不是按图像数 / 总字节加权均值，也不是每例均低于 1%。分母还有表述差异：p. 9 写相对 image bitstream，p. 28 写 total bitstream；表 14 的 OD Q1 显示 total 0.105、image 0.103、SV 0.0021。按显示值算 SV/image≈**2.04%**，SV/total=**2.00%**，原表写 2.05%。舍入不能完全重建精确比例，但原表更接近 image denominator。需原始未舍入码率和真实流验证；不改原文数值，不把 0.98% 当全流程协议开销。

## 隐私、局限与待核实问题

**整理者归纳：** 无裁剪 / DP 噪声 / accountant、secure aggregation 或加密证明。编码会使用私有图像，图像码流与实例 SV 是数据相关发布；低秩、TTFT、熵编码本身不构成隐私保证。公开任务模型 / 数据集的许可也与本文 PDF 的 CC BY、代码 Apache-2.0 分开。

| 问题 | 已有证据与保留事项 |
| --- | --- |
| 每层秩与信令 | pp. 12–13 全局预算 / 跨层排序、p. 24 非均匀架构，和 pp. 28–29 “每层 rank 4、无需 index”须解释；总秩不决定方向位置 |
| 停止与后训练 | 算法 1 未展开 warm-up / post-training；达到预算和全部停止的关系需以可执行版本确认，尤其最大 40 epochs 未触发时如何处理 |
| AdaLoRA 对比 | p. 11 将 AdaLoRA 等概括为在 fine-tuning 开始前 / 开始时一次分秩，与 [AdaLoRA](../2023-zhang-adalora/notes.md) pp. 4–6 的训练中动态预算 / 重要性更新不符；可成立的是 task-level vs instance-level 和适配范围区别，不能改写 AdaLoRA 为静态法 |
| “最佳 / 一致领先”范围 | 表 6 速度收益伴随 BD 效用损失；表 9 5/10 epochs 不全面领先；高斯退化样本仅 100，主表未普遍给 seed 标准差 |
| 码率 / 编码部署 | SV/image 与 SV/total 描述不同；真实码流位置成本、entropy estimate 与实际字节、模型初始化 / evaluator / 传输成本需计入部署评估 |
| 适配信息 | open-set 仍使用任务身份和冻结 evaluator；可能有模型特定偏好，不能等同未知任务无监督泛化 |
| 可扩展性 | 只验证 TIC / Cheng2020、有限视觉任务、4090；无端侧实时 TTFT、异构网络或联邦 / DP 结果 |

## 官方代码、数据与复现信息

**已核实的作者来源，2026-10-12：** PDF p. 30 给出 [unkipark/ISER](https://github.com/unkipark/ISER)，README 明确官方实现。核对代码快照 [1c66c38](https://github.com/unkipark/ISER/commit/1c66c38d3a4c92b5aae767f15d94473955c50928)，日期 2026-08-03，根 LICENSE 为 Apache-2.0。只读 README、相关配置、detection / depth 脚本、LoRA utils / layers 与权重熵模块；没有安装作者环境、下载权重或运行评估。

README 记录 Python 3.8、PyTorch 2.2.2 / CUDA 12.1，列 TIC / cls / OD / IS checkpoint 与冻结任务模型下载链接，并要求 ImageNet / COCO / KITTI。checkpoint 链接存在不等于已下载校验、数据准备正确或结果可复现。README 的 `python example/...` 与实际目录 **examples/** 不同，执行前应按文件树核对。

| 静态观察 | 与论文的关系 / 尚需核实 |
| --- | --- |
| detection.py 的 `update_ipt` | 使用绝对值 parameter×gradient 和 EMA / uncertainty；这补充了式 (3) 未展开的评分实现，不能写成原式已经完整定义 |
| sensitivity 分支 | 对二阶差乘 `ies_scale=5` 后用 **mean** 与阈值比，每 3 epoch 更新预算，使用 `round`，同时有 AdaLoRA 式 cubic schedule；原文式 (5) 为 **sum**，式 (6) 为 **floor**。同一数值 tau 在不同归一化下不能直接等价 |
| 默认 detection.yaml | `train_image_form: 0` 为 full image，`pre_weight: od` 为 closed-set；论文完整 ISER 的 MSTS 是 hybrid，open-set 应用 cls 初始化。直接使用默认配置不等于本文 open-set 主实验 |
| 质量 / rank 配置 | encoder 4、decoder 8、target 4、warm-up 5 / post 10 与正文相符；分类 YAML 的 task-loss lambda 列表不同于正文统一四值，须区分 human rate 参数与 task-loss 系数及实际覆盖值 |
| post-training 循环 | 已读的 `test_epoch_w_instance_train` 路径在到达 post count 后打印耗时，外层仍是固定 `range(cfg.epochs)`，该处未见退出语句；不能仅根据日志中的“early stop”认定实际少做所有后续计算 |
| SV bitrate 估计 | `test_epoch_w_instance_train` 量化 SV 后将零位置 likelihood 设为 1，再累加 −log2 likelihood / pixels；权重模块虽提供 compress / decompress，已读路径未调用完整字节流 round trip。被剪位置如何无成本定位需核实 |
| 每图重置 | 当前提交直接遍历 module tree 恢复参考 tensors，防止跨图适配状态残留；是否与论文全套数值对应仍需 checkpoint / 日志 |

以上只针对该公开快照的静态阅读，不能据此断言论文实验使用了同一代码路径，也没有代替作者修代码。完整 reproduction 应先锁定 commit、权重 hash、task / quality / MSTS overrides、seed 和所有 evaluator，明确 epoch 与停止定义，再测真实编码流、解码一致性、字节数、计时与 RD 曲线；本仓库未执行这些实验。

## 与仓库其他论文的关系

**有文献依据的整理者比较；不做跨实验排名。**

| 对照 | 共同点 / 差别与依据 |
| --- | --- |
| [AdaLoRA](../2023-zhang-adalora/notes.md) | 都用可学习 SVD 增量 / 重要性 / 全局方向预算；AdaLoRA 训练中动态分配 task-level PEFT 容量（其 pp. 4–6），ISER 每图用 decoder SV 的时间变化安排秩 / 停止（本篇 pp. 11–14）。ISER 并未实测“把 AdaLoRA 直接用于同 TTFT 条件”的完整比较 |
| [SVD-LLM](../2025-wang-svd-llm/notes.md) | SVD-LLM 用校准输出目标对白化后的**主干权重**做截断和顺序恢复（其 pp. 3–5）；ISER SVD-LoRA 是**图像 codec 的适配增量**，encoder / decoder scope 不同，SV 还加入图像流。不能把主干删减 40%与 SV overhead0.98%放在同一分母 |
| [CG-FedLLM](../2025-wu-cg-fedllm/notes.md) / [DR-Encoder](../2024-wu-dr-encoder/notes.md) | 本篇 codec 的 encoder / decoder 编解码图像，CG / DR 的 AutoEncoder 重建梯度 / 低秩因子；训练先验、传输对象与效用不同。本篇 pp. 7–9、14–16 不涉及真实梯度收集隐私或 Gaussian accountant；不以同名 encoder 推断方法可直接互换 |
| [FFA-LoRA](../2024-sun-ffa-lora/notes.md) | 解码阶段固定方向、只更新 SV，与 FFA 固定共享因子以线性聚合有“限制可训练子空间”的概念联系；ISER 不执行联邦双因子聚合，不能用它证明 CG 的聚合一致性（FFA pp. 4–6） |
| [FLASC](../2024-kuo-flasc/notes.md) / [PowerSGD+](../2025-xie-powersgd-plus/notes.md) | 它们压缩训练消息 / 梯度而非图像比特流（FLASC pp. 3–5，PowerSGD+ pp. 3–4）；ISER 的 image bpp、BD-Rate 和 TTFT 秒数不提供相同通信或收敛结果 |

**未验证研究设想：** 将 ISER 的实例稳定性信号用于联邦 LoRA 本地停止、结合 AdaLoRA 的预算调度或在 CG / DR latent 上学习动态秩，都需要重新验证信号、方向对齐、客户端聚合、总通信与隐私核算。本文没有报告这些组合。

## 阅读总结

ISER 的价值是把“对每图使用统一适配器 / 固定训练时长”推进为实例预算和速度取舍。最值得借鉴的是用同一优化过程中的梯度动态进行预算调度，而不是其摘要中的最大百分比。阅读时必须同时保留 open-set 的任务网络前提、真实码流 / 熵估计口径、编码侧秒级计算和公开实现差异。

## 单光子 LiDAR 参数

本篇为图像压缩 / 视觉任务论文。探测器、阵列规模、探测距离、目标速度、SNR/SBR、每像素光子数、采集时间、LiDAR 重建帧率、空间分辨率和定位误差均**不适用**。256×256 patch、KITTI 深度误差、bpp、解码毫秒和高斯图像噪声不能替代这些物理量。

[原件 / 许可](source.md) · [BibTeX](citation.bib) · [跨论文比较](../../comparison.md) · [返回总览](../../README.md)
