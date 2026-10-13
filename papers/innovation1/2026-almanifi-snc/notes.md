# Enhancing communication-efficiency of cross-device federated learning through end-to-end neural compression with sparsification

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 作者 | Omair Rashed Abdulwareth Almanifi, Chee-Onn Chow, Mau-Luen Tham, Joon Huang Chuah, Jeevan Kanesan, David Chieng（PDF p. 1；姓名中 `fi` 为排版连字） |
| 发表渠道 | Internet of Things，Volume 40，2026，Article 102113；官方网页标示卷期为 November 2026 |
| 实际阅读版本 | Elsevier 排版正式期刊版本；23 物理页，正文及声明 pp. 1–20、数据声明和 84 条参考文献 pp. 21–23；无独立附录 |
| 日期 | PDF p. 1：2026-05-06 received、2026-08-30 revised、2026-09-27 accepted、2026-09-29 available online；已在线发表，不把未来卷期月份当未发表 |
| DOI与官方入口 | [10.1016/j.iot.2026.102113](https://doi.org/10.1016/j.iot.2026.102113)；[ScienceDirect article](https://www.sciencedirect.com/science/article/pii/S254266052600243X) |
| PDF与引用 | 上传件为 Elsevier All rights reserved，不在公开目录复制；[source.md](source.md)；[citation.bib](citation.bib) |

本笔记阅读全文、数据声明和参考文献；页码均为上传 PDF 物理页码。核对日期 2026-10-13。以下区分原文主张与整理者判断，未运行代码或复现实验；分类只遵循用户压缩包。

## 摘要

Sparse Neural Compression（SNC）在 FedAvg 本地训练后压缩**权重更新**：先 top-κ 稀疏并保留本地残差，再用共享的 Conv1D 编码器、量化 latent、可训练 prior 和 arithmetic coding 压缩非零值；稀疏索引用 Fibonacci run-length 无损编码。前若干轮只稀疏发送更新，服务器收集样本，经 PCA+KDE 合成增广训练 codec 后，下发 encoder/prior 一次。15 客户端、8 客户端参与、Dirichlet α=0.3 的 FMNIST/CNN、FedAvg 中，λ=10 得到 88.89% 峰值测试准确率及平均 450.79× 更新压缩；无压缩基线 88.24%（p. 14，表 3）。这不是大语言模型或 LoRA 的实验。

## 背景、不足与贡献

- **原文问题**：cross-device 客户端带宽和计算受限，延迟通信的 FedAvg 仍有大更新；现有量化/稀疏规则通常不能直接优化 rate-distortion 折衷（pp. 3–7）。
- **原文方法定位**：FedAvg、部分参与、非 IID；重点是压缩更新，避免把 momentum、clipping 等作为主要方法，另评估 FedAdam/FedProx/FedCOM 兼容性（pp. 6、13、16–17）。
- **原文贡献**：可训练量化压缩器；服务器学习跨客户端统计；低算力客户端只运行 encoder；Fibonacci 索引编码（pp. 6、8–11）。
- **相关方法边界**：LGC 原设计依赖 FedSGD 的大量迭代收集压缩器训练数据，本文改造为 FedAvg 后在本实验未收敛；不能据此否定 LGC 原 FedSGD 场景（pp. 6、17，图 8）。

## 方法流程与核心公式

以 $`\Delta w_{k,t}`$ 表示客户端本地训练后的完整权重更新、$`n_k`$ 表示样本数、$`m_t`$ 为本轮参与样本总数。服务器解码后按样本数平均（p. 7，式 3）：

$$
\Delta w_{g,t}=\sum_{k\in\mathcal C_{p,t}}\frac{n_k}{m_t}
D_e(E_n(\Delta w_{k,t})).
$$

学习目标将 rate、log-cosh 重构误差、cosine similarity 组合（pp. 7–8，式 5–7）：

$$
\mathcal J=\mathcal J_R+\lambda(\mathcal J_D-\sigma\mathcal J_S),
\qquad \sigma=0.4,
$$

$$
\mathcal J_R=\frac{\#_b(E_n(\Delta w))}{32\,\#(\Delta w)},
\qquad
\mathcal J_S=\frac{\Delta w\cdot\widehat{\Delta w}}
{\|\Delta w\|_2\|\widehat{\Delta w}\|_2}.
$$

$`\mathcal J_D`$ 为原文 log-cosh 的逐元素重构距离；正文未在式 5 明写求和/平均归约，本式不自行补充。$`\#_b`$ 是位数、$`\#`$ 是元素数；该 rate 是压缩后与原 32-bit 张量位数比，而结果表报告的是反比 CR。λ 增大倾向减少 distortion、牺牲 CR。

Universal quantization（p. 8，式 8）：

$$
z=A_n(u),\quad \widetilde z=\operatorname{round}(z-v)+v,
\quad v\sim\mathcal U[-0.5,0.5).
$$

$`u`$ 是 top-κ 更新 densify 后的非零值向量。训练结合 soft rounding（式 9），以共享 factorized learned prior 提供 arithmetic coding 所需概率，rate 由 latent cross-entropy $`\mathbb E[-\log_2p_{\widetilde z}]`$ 估计（p. 8，式 10–11）。编码器 Conv1D+GDN、解码器 Conv1DTranspose+IGDN，使用 strides、无 bias，encoder 第二层 20% dropout（p. 9，图 3、式 12–13）。GDN 分母为 $`\sqrt{\beta_i+\sum_j\zeta_{ij}I_j^2}`$，降低统计相关性。

稀疏及残差（p. 9，式 14；p. 11，算法 3）：

$$
v_k=\operatorname{Top}_{\kappa}(\Delta w_k),\qquad
r_k=\Delta w_k-v_k.
$$

**按原算法**，残差在下次本地训练前加到收到的模型上；不是把神经 codec 的全部解码误差都放入误差反馈。最后分类层因敏感不按统一 κ 稀疏。非零索引相邻距离用 Zeckendorf/Fibonacci 编码，decode 后累加复原索引（p. 10，算法 1–2）；数组起点/零距离约定需要在实现中明确。

完整过程（pp. 10–11，算法 3）：

1. 前 $`T_c`$ 轮，top-κ + Fibonacci 仍工作，但非零数值没有使用神经 codec；服务器积累更新样本。
2. 服务器降到 15 个 PCA 主成分，grid search KDE bandwidth，以 Gaussian KDE 采样后 inverse PCA 扩充数据。
3. 训练量化 AE 100 epochs；下发 encoder + prior，之后客户端保持该压缩器，服务器 decode/scatter 后聚合。
4. 全局模型仍按原 FL 流程广播；论文重点减少上行更新，不是用同等比例压缩上下行全部通信。

**收敛论述边界**（p. 12，式 16–17）：引用既有 FedAvg noisy-channel 分析，假设 L-smooth、μ-strongly convex、SGD 方差及梯度有界，并且平均 codec MSE $`e_t\leq\eta_{l,t}^2\sim O(t^{-2})`$。作者明确不能为学习到的 codec 给出该条件的硬保证，只建议把观察到的误差作为训练终止条件。它是条件性收敛直觉，不能标成深度非凸模型上无条件保持 FedAvg 收敛的证明。

## 实验设置

| 项目 | 原文条件 |
| --- | --- |
| 模型任务 | MNIST/两层 MLP（128 hidden）；FMNIST/小型 CNN；CIFAR10/修改 VGG；CIFAR100/8-layer ResNet，LayerNorm 替代 BatchNorm（pp. 12–13） |
| 联邦主配置 | K=15，Kp=8，local batch=16，Dirichlet α=0.3，SGD；每客户端分区 10% 用于每轮测试（p. 13，表 2） |
| 任务对应 Tc/E/lr | MNIST：14/100/0.001；FMNIST：14/100/0.01；CIFAR10：40/200/0.04；CIFAR100：20/100/0.01（p. 13，表 2 合并单元格已视觉核对） |
| κ | MNIST/FM/CIFAR10=0.01；CIFAR100：FedAvg 0.015、FedAdam 0.0125；分类层例外（pp. 9、14） |
| codec | AdamW，100 epochs，lr=0.01，batch=32；σ=0.4，λ=10/15/25/50（pp. 8、13） |
| 对比 | Natural、TernGrad、1-SignFedAvg、Drive+、QSGD、RQSGD、RDQ、FedFQ、Top-κ、STC；FedAvg/FedAdam 两组（pp. 13–14） |
| 环境/软件 | Python3、NumPy、TensorFlow、TensorFlow Compression、Scikit-learn；单机器，文中写 NVIDIA 4080 RTX、6GB graphics RAM、32GB RAM（p. 12）；硬件名称与显存组合需要复现时另确认 |

表 2 未列出主实验本地 epochs $`E_l`$，p. 13 仅称未提及设置使用 TensorFlow 默认；也未完整列出 seed、重复次数、误差条、KDE bandwidth grid、合成数据数、完整层通道/核配置与依赖版本。因此不能把表中 Top Acc 当多次均值或最终轮准确率。

## 主要定量结果

下表取 p. 14 表 3，**峰值测试 Accuracy / 平均更新 CR**；K=15、Kp=8、α=0.3。

| 任务/协议 | 无压缩 | SNC λ=10 | SNC λ=50 |
| --- | --- | --- | --- |
| MNIST/FedAvg | 88.91% / 1× | 89.21% / 428.27× | 91.43% / 379.93× |
| FMNIST/FedAvg | 88.24% / 1× | 88.89% / 450.79× | 89.09% / 402.62× |
| CIFAR10/FedAvg | 71.08% / 1× | 70.56% / 352.79× | 72.75% / 293.10× |
| CIFAR100/FedAvg | 31.21% / 1× | 22.29% / 257.52× | 31.87% / 210.05× |
| FMNIST/FedAdam | 90.27% / 1× | 92.62% / 395.83× | 93.54% / 363.73× |

CIFAR100 λ=10 相对无压缩损失 **8.92 个百分点**（整理者由表 3 相减），表明高 CR 并非总能保持效用；FedAdam/CIFAR100 λ=25/50 的 Top Acc 为 32.09/31.59，也非随 λ 严格单调。FMNIST/FedAvg 的 STC 达 89.38%/335.72×，准确率高于所列 SNC 主配置；“超越所有方法”不应解释成 accuracy 和 CR 每格同时占优。

扩展 FMNIST、100 客户端、相同参与比例：FedAvg 80.50%；SNC λ=10/50 为 81.66%/471.58×、84.26%/404.85×（p. 16，表 4）。文中未明确非整数参与人数如何取整，本笔记不补造。

通信图 7a（pp. 16–17）只统计 **compression round 之后的上行**，FMNIST λ=10/15/50 为约 734/759/821KB，无压缩约 330MB；没有据此将前 $`T_c`$ 轮、下发全局模型、下发 encoder 一次的成本当作已计入。

**计算与附加通信**（p. 20，表 9）：encoder+prior 469KB，一次下发；FMNIST 平均压缩 0.0127s、本地模型 epoch 0.2582s；codec **每 epoch** 0.0787s，共训练100 epochs；PCA/KDE 合成 0.0506s。这是同一桌面机器上的 CT，不能当作真实低算力手机的端到端网络提速或能耗结果。

## 消融、适用条件与局限性

- **索引编码（原文）**：FMNIST/CNN、Top-κ=0.01、50 epochs 下 Fibonacci 约 6.1 bit/index，Golomb 8.36、Elias Gamma 8.89（p. 18，图 7b）。表 8 去掉 Fibonacci 后，λ=10 的 FMNIST CR 从 450.79× 降到 97.72×，准确率同为 88.89%（p. 19）。
- **PCA/KDE 消融**：FMNIST λ=10，不合成数据后准确率 89.77%、CR 440.91×，完整方法 88.89%/450.79×；所以合成增广主要偏向更高 CR，并非每例提高准确率（p. 19，表 8）。CIFAR10 λ=15 去增广为 73.47%/326.74×，完整70.60%/329.12×。
- **延迟 Tc**：FMNIST λ=10，Tc=5/10/20/40 时 Top Acc 87.69/89.23/89.38/90.15，CR 465.49/436.80/396.78/295.57×；更晚训练有更大样本池，却降低 CR，并延后神经压缩上线（p. 18，表 6）。
- **异质性**：FMNIST α=0.1，FedAvg 84.44%，SNC λ=50 91.43%/413.99×，STC 91.15%/333.67×；这些是本文小模型设置，不推广为所有非 IID 数据都无退化（p. 19，表 7）。
- **其他协议**：FMNIST/FedProx λ=15 SNC 91.49%/431.56×；FedCOM λ=50 89.40%/356.65×；表 5 FedCOM baseline 填破折号，不造基线增益（p. 17）。
- **作者明确限制**：需要服务器前期收集更新；factorized prior 未建模各维依赖，拟进一步改进（p. 20）。
- **隐私主张的证据边界（整理者判断）**：pp. 4、12、16、20 使用“encrypted”措辞，论据主要援引别篇 AE/稀疏攻击实验；本篇没有密钥管理、正式威胁模型、DP参数或自有 inversion-attack 实验。共享 prior 和 arithmetic coding 本身不是密码学加密，不能写成保证防止数据反演。
- **整理者局限归纳**：只有小视觉模型和离线模拟；缺少大模型/LoRA、压缩器长期分布漂移、真实设备/网络、重复实验及置信区间、能耗测量。绿色通信是动机，非实测减碳结论。

**上传版内部差异**：CIFAR10/FedAvg λ=25，p. 14 表 3 为 72.47%，p. 19 表 8 完整方法为 72.60%；不合并为同一确定数值。算法 3 的 `otherwise` 收集数据分支按字面还可能在 Tc 后执行，正文则说明只在前期采集训练一次；复现需核对实现。图 3 架构还需结合图读通道/stride，不能仅用文字把 decoder 声称严格数学逆。

## 官方代码、数据与复现信息

PDF 未给出本文专属代码地址；本次未核实作者公布的 SNC 实现，不能以 TensorFlow Compression 库地址替代 SNC 官方代码。p. 21 数据声明仅说明使用数据公开可用。复现先确定全局/本地迭代、划分和峰值统计，保持原 32-bit 分母、索引与最终分类层例外、codec 训练开销和一次下发成本；独立记录 warm-up、神经阶段和上下行总通信。未运行复现。

## 阅读总结

**原文解决的问题**：在 FedAvg 较少通信轮、部分参与及异质数据下，把神经压缩器学习纳入可编码的稀疏更新通信流程。

**整理者归纳**：值压缩和索引编码共同决定实际 CR；学习率、训练样本池与 λ 需要配套报告。检验方法时应区分峰值效用、上行压缩比、端到端通信、严格收敛条件及隐私证据。

## 单光子 LiDAR 参数

不适用。MNIST/FM/CIFAR 分类无单光子器件、采集/重建参数或测距定位误差。

[返回总览](../../../README.md) · [跨论文比较](../../../comparison.md) · [来源与许可](source.md)
