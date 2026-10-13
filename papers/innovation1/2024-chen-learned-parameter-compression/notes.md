# Learned Parameter Compression for Efficient and Privacy-Preserving Federated Learning

## 文献信息与阅读对象

| 项目 | 记录 |
| --- | --- |
| 作者，按上传版顺序 | Yiming Chen、Lusine Abrahamyan、Hichem Sahli、Nikos Deligiannis |
| 阅读版本 / 出版 | IEEE Open Journal of the Communications Society, **5:3503–3516 (2024)**；上传期刊版 14 页 |
| 日期 | Received 2024-05-11；Accepted 2024-05-28；Published 2024-06-03；Current version 2024-06-25（PDF p. 1） |
| 正式 DOI | [10.1109/OJCOMS.2024.3409191](https://doi.org/10.1109/OJCOMS.2024.3409191) |
| 官方核实 | [VUB 作者所在大学记录](https://researchportal.vub.be/en/publications/learned-parameter-compression-for-efficient-and-privacy-preservin/)；[IEEE ComSoc 出版目录](https://www.comsoc.org/system/files/2024-07/Publications_Contents_Digest_2024_Jun.pdf) |
| 许可 / 原件 | 首页 **CC BY-NC-ND 4.0**；本非商业整理原字节收录 [paper.pdf](paper.pdf)，署名、来源和许可详见 [source.md](source.md) |
| 阅读范围 / 核对 | 2026-10-13；阅读全文 14 页，包含 pp. 12–13 参考文献、p. 14 作者简介，无另列附录；未运行训练或攻击实验 |

页码均指上传 PDF 的**物理页码**。**原文报告**指论文内容，**整理者归纳 / 计算**和**待核实**不作为作者已证明的结论。方法没有明确独立简称；目录短名仅便于检索，不将此前分布式训练的 LGC 名称挪为本方法名。

## 摘要

**整理者归纳，pp. 1–2、5–7。** 本文把每层局部**模型参数**展平成一维向量，用客户端独立训练的一维卷积 autoencoder 编码。每个本地 SGD iteration 后将参数替换为有损重建值，使压缩误差同时充当输入相关扰动。预热期间训练 / 微调 autoencoder 并传输重建参数；进入 regular rounds 后，将一次共享给服务器的 decoder 与每轮发送的低维码结合，服务器先分别解码，再做模型平均。

原文在 LeNet / MLP、Fashion-MNIST / CIFAR-10 / CIFAR-100 上报告 regular-stage 参数表示压缩约 **4.1×**；DLG / IGA 重建攻击在若干设置下失败。这里的 privacy-preserving 是**所测试攻击下的经验结果**，不是差分隐私或密码学保证；本文没有给出 $\epsilon,\delta$、隐私会计或自适应攻击下的安全证明。

## 背景、已有方法不足与贡献

**原文，pp. 2–4。** 原始数据留在客户端不阻止服务器从梯度 / 模型变化逆向恢复训练样本。加高强度高斯噪声或大比例稀疏化可能影响最终精度；PRECODE 修改模型并增加通信量，且引用的 Bayesian gradient-leakage 工作可绕过其部分 MLP 防御。作者此前 LGC 用学习型自编码器提高**分布式训练**通信效率，本篇重点改为**联邦局部参数的有损压缩与隐私防御**，二者问题设定不同。

**原文贡献，pp. 2、5–7：**

- 压缩本地参数而非直接公开原始参数 / 梯度，降低 uplink 表示尺寸。
- 把重建误差放入每次本地迭代，形成与该层参数相关的扰动。
- 每客户端 decoder 在预热结束时只传一次；常规阶段服务器用对应 decoder 逐客户端重建。
- 用分类精度、压缩比与重建 MSE / PSNR / SSIM / ASR 分别衡量效用、通信和攻击效果。

**边界，整理者归纳：** 本篇不是 LLM / LoRA 专项方法，也不是多模态实验；数据集均为图像分类。对攻击成功率的改善只涵盖文中威胁模型与选定攻击，不代表完全消除所有信息泄漏。

## 方法与核心公式

### 逐层编码、重建与本地替换

**原文，p. 5，式 (5)–(8)、图 2；pp. 6–7，式 (11) 与算法 1–3。** 为避免抽取文本中希腊字母丢失，以下将 flattened 参数记为 $v$，属于整理者记号规范：

$$
v_{k,\ell,i}=\operatorname{flatten}(\theta_{k,\ell,i}),\qquad
z_{k,\ell,i}=\phi_{E,k}(v_{k,\ell,i}),
$$
$$
\hat v_{k,\ell,i}=\phi_{D,k}(z_{k,\ell,i})=v_{k,\ell,i}+e_{k,\ell,i},\qquad
\hat\theta_{k,\ell,i}=\operatorname{reshape}(\hat v_{k,\ell,i}).
$$

下一本地更新使用**重建参数**：

$$
\theta_{k,\ell,i+1}=\hat\theta_{k,\ell,i}-\eta\nabla_{\hat\theta_{k,\ell,i}}
\mathcal L(f(\{\hat\theta_{k,\ell,i}\}_{\ell=1}^{L});D_k^i).
$$

这里 $e$ 是确定性学习 codec 的重建误差，不能自动视作独立同分布噪声、DP 噪声、随机投影或无偏压缩器。服务器持有 decoder，因此能够恢复有损参数；防御不是隐藏解码器或加密通信。

### Autoencoder 结构与训练

**原文，p. 6 表 1–2、式 (9)–(10)，图表已目视核对。** Encoder 五个 Conv1D 层的输出 filters 为 **64,128,256,64,4**，kernel size 全 3，stride 为 **2,2,2,2,1**；Decoder 五个 deconvolution 层 filters 为 **4,32,64,128,32**、kernel 3、stride 为 **1,2,2,2,2**，最后 Conv1D 为 **1 filter、kernel 1、stride 1**。每阶段用 leaky-ReLU。按层处理不同长度向量，不是为每个目标网络重新设计固定大小的全连接瓶颈。

Reconstruction objective：

$$
\mathcal L_{\mathrm{rec}}=\|\hat v-v\|_2^2,
$$

原文称 MSE，显示公式未除向量长度；实现的 reduction 与不同层长度的权重需要复现时核对。更新 encoder / decoder 的学习步长记为 $\lambda$；它与主任务模型步长 $\eta$ 不同。

### 三阶段与通信内容

| 阶段 | Autoencoder / 本地更新 | 发给服务器 | 出处 |
| --- | --- | --- | --- |
| Initialization | 服务器初始化 global model；每客户端初始化并保留自己的 codec | 主任务模型下发 | p. 6 |
| Warming-up rounds，$t=1,\ldots,T_w-1$ | 每轮头 $m_w-1$ 次本地迭代训练 / 微调 codec；这部分不做参数替换；随后用重建参数迭代 | **完整重建参数**，非低维码；结束时一次发送客户端 decoder | pp. 6–7，算法 1–2 |
| Regular rounds，$t=T_w,\ldots,T$ | codec 已学习，逐 iteration 重建替换，之后本地 SGD | 每层低维表示 $z$；服务器用该客户端 decoder 重建 | p. 7，算法 2–3 |

原文实验 $T_w=35$、$m_w=30$；“using updates twice over 30 iterations”见 p. 8。文字 / 算法有 $m_w-1$ 和 30 的边界差异，应核对实现，不改成任意具体 29 次训练的实测结论。每客户端参与轮计数与全局 round 计数也需在抽样参与时明确。

服务器算法 3 和式 (12) 为**参与客户端简单平均**：

$$
\theta_{\ell}^{\mathrm{new}}=\frac{1}{|C|}\sum_{k\in C}
\operatorname{reshape}\bigl(\phi_{D,k}(z_{k,\ell,m})\bigr).
$$

p. 3 联邦 objective 写数据量权重，但实际显示聚合式未包含 $|D_k|$；不能把加权平均实现写成原文已明确。没有 error-feedback 机制、形式化收敛定理或端到端编解码协议字节统计。

## 实验设置

**原文，pp. 8–10。**

| 项目 | 配置 |
| --- | --- |
| 模型 | LeNet：三层 12-filter Conv、Sigmoid、末层全连接；MLP：三层、hidden 256 |
| 数据 | Fashion-MNIST 60k/10k；CIFAR-10 50k/10k；CIFAR-100 100 classes；按文中 FedAvg 设置分 IID / non-IID |
| FL / 精度 | 100 clients、500 rounds；batch 64 配本地 10 epochs，batch 8 配 1 epoch；seed 1234 |
| Codec | 35 warming-up rounds、30 warming-up iterations；每客户端 decoder 72,352 参数，289,408 bytes，只上传一次 |
| 硬件 | 单机 2×GeForce RTX 3090 Ti、128 GB RAM；非真实端设备网络实验 |
| Baselines | FedAvg；NG Gaussian std $10^{-1}$ / $10^{-2}$；GS 丢弃 90% / 70%；PRECODE |
| 攻击 | 128 随机样本；DLG 的梯度 MSE、IGA 的 negative cosine + TV；Adam、7,000 iterations、初始 lr 0.1 |
| Attack phase | 随机初始化模型；已训练模型第 5 轮 / 第 40 轮；后两者 batch 8 更新（p. 11） |
| 隐私指标 | MSE↑、PSNR↓、SSIM↓、ASR↓；ASR 定义 SSIM≥0.6 的成功恢复比例，不是任务准确率 |

未训练模型的防御测试先做单次样本更新，再以该模型参数训练 autoencoder **100 SGD iterations**，然后攻击解码后的参数（p. 10）。这与完整 FL 的 35-round 预热不同，不应把两套实验训练预算混成一种。攻击优化里 “reduced by 10% at milestones of 18,38,78 of total iterations”表达不清，未补造绝对 iteration / 百分位实现。

## 主要结果与适用范围

### 分类效用与通信

**原文，p. 9 表 3–6；下表“差”是整理者计算的百分**点**，无跨 seed 置信区间。**

| 条件 | FedAvg top-1 | 本方法 top-1 | 差，百分点 |
| --- | --- | --- | --- |
| Fashion-MNIST、MLP、non-IID、B64 / E10 | 85.06% | 83.92% | −1.14 |
| Fashion-MNIST、MLP、non-IID、B8 / E1 | 85.13% | 84.62% | −0.51 |
| CIFAR-10、LeNet、IID、B64 / E10 | 60.75% | 60.43% | −0.32 |
| CIFAR-10、LeNet、non-IID、B64 / E10 | 46.73% | 45.23% | −1.50 |
| CIFAR-10、LeNet、non-IID、B8 / E1 | 46.18% | 41.65% | −4.53 |
| CIFAR-100、LeNet、IID、B64 / E10 | 27.63% | 27.02% | −0.61 |

精度接近并非每种配置都几乎无损；上表 −4.53 百分点展示小 batch / 非 IID 的限制。原文表 3–5 用括号表示**与 FedAvg 的差**，不是标准差。NG $10^{-2}$ / GS70% 部分精度更高，却更易发生泄漏；不能只按精度判定最优防御。

**原文，p. 9 式 (13)、表 6–7、p. 10 图 3。** 本方法 CR=**4.10×**，FedAvg / NG=1.00×，GS90%=3.33×、GS70%=1.11×；PRECODE 的 CR 随模型而变，LeNet–Fashion-MNIST=0.0288×，表示通信**变大**，不是减少 34.8×。CR 是原参数大小 / 表示大小，不包含下行、35-round 全尺寸预热、一次 decoder 上传、包头或重传的完整总账。289,408 bytes 的 decoder 传输应该在完整训练成本中另计。

### 梯度反演：保留攻击 / 模型 / 阶段

**原文，pp. 10–12 表 8–12、图 4–7；DLG/IGA 用斜线分开。**

| 条件 | FedAvg SSIM / ASR | 本方法 SSIM / ASR | 出处 |
| --- | --- | --- | --- |
| Untrained LeNet、Fashion-MNIST，DLG / IGA | 0.99/0.95；100/100% | 0.027/0.072；0/0% | p. 10 表 8 |
| Untrained MLP、Fashion-MNIST，DLG / IGA | 1.00/1.00；100/100% | 0.06/0.03；0/0% | p. 10 表 8 |
| Untrained LeNet、CIFAR-10，DLG / IGA | 0.62/0.60；58/56% | 0.02/0.03；0/0% | p. 10 表 9 |
| Trained MLP、第 5 轮、Fashion-MNIST，IGA | 0.97；100% | 0.00；0% | p. 11 表 11 |
| Trained MLP、第 5 轮、CIFAR-10，IGA | 0.37；28.75% | 0.00；0% | p. 11 表 11 |
| Trained MLP、第 40 轮、Fashion-MNIST，IGA | 0.95；100% | 0.00；0% | p. 12 表 12 |
| Trained MLP、第 40 轮、CIFAR-10，IGA | 0.34；28.75% | 0.00；0% | p. 12 表 12 |

表 10 的 untrained LeNet / CIFAR-100：本方法 DLG / IGA SSIM **0.0153/0.0442**、ASR **0/0%**（p. 11）。这些零值代表样本和阈值下的测得结果，不能推成任意攻击成功概率为零。p. 11 图 5 是绕过 PRECODE 的 Bayesian framework 下若干 MLP / CIFAR-10 视觉例子，无完整与表 8–12 同规格的多 seed 定量安全结论。

## 消融与局限

**原文实验边界 / 整理者评估：**

- pp. 8–12 比较 defense 强度、模型、数据分布、batch/epoch 和训练阶段；没有系统拆分“本地迭代替换”“仅 uplink 压缩”“预热长度 / codec 容量”的组件消融，无法独立估计每一项贡献。
- 没有针对编码器 / 解码器已知的自适应攻击重新优化全过程的全面测试；论文讨论恶意服务器，但经验攻击的输入为解压参数。攻击能力边界需要明确，不能把本文的成功防御当安全定理。
- 没有 DP 参数 / 会计，学习型有损扰动不自动满足 DP。NG 基线使用固定标准差，也未在本文做与目标 $\epsilon$ 相匹配的比较。
- 精度表是单 seed 1234；攻击成功率取决于 128 样本、SSIM0.6、optimizer / 重启与训练阶段。没有多 seed confidence interval。
- 4.1× 对应参数表示比例；初始预热成本、decoder 上传、全局模型下发、实际 wall-clock、能耗 / 显存未给完整端到端测量。
- 主任务只有较小 LeNet / MLP 和图像数据；不能直接推广到 transformer / LLM / LoRA 更新或大规模端侧部署。
- 原文 table references 存在笔误：p. 8 写“Tables 2,4,5”但 Fashion-MNIST 精度实际表 3；本笔记按图表标签记录，不沿用笔误。

## 复现信息与阅读结论

**已取得 / 未执行。** 本次确认完整期刊版、作者、DOI、页数、正文许可、上传件 SHA-256；Poppler 检查首页与方法 / 结果页。正文未给出可核实的本方法官方代码仓库，本次不编造代码链接，也未复现实验。

复现还需确定模型与 codec 优化器 / 学习率、Leaky-ReLU slope、padding / 长度恢复、active-client selection、non-IID 划分参数、客户端预热计数、codec 更新次数及攻击 lr schedule。上述未展开项是复现边界，不是待填写模板。

**整理者结论：** 有价值的证据是“逐客户端学习 codec + 本地迭代重建替换”在指定小模型任务下获得通信 / 效用 / 攻击重建的经验取舍。4.1×、ASR0 与安全保证三者必须分开；与仓库其他论文比较时分别记录压缩对象、codec 共享成本、攻防条件和是否具备形式化隐私。

[来源与原件](source.md) · [BibTeX](citation.bib) · [仓库总览](../../../README.md) · [跨论文比较](../../../comparison.md)
