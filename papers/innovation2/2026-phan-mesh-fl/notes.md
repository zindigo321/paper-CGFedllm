# Entropy-Guided Tensor Compression for Multimodal Federated Learning on Edge Devices

## 文献信息与阅读对象

| 项目 | 记录 |
| --- | --- |
| 方法名 | MESH-FL |
| 作者，上传版顺序 | Quoc Bao Phan、Tuy Tan Nguyen |
| 阅读版 | arXiv **2607.06651v1**，2026-07-07，12页；上传 PDF 的首页 stamp、内嵌 arXivID / DOI / Title 均对应此版本 |
| 官方版本 / 全文 | [版本页](https://arxiv.org/abs/2607.06651v1)；[官方 PDF](https://arxiv.org/pdf/2607.06651v1)；预印本 DOI [10.48550/arXiv.2607.06651](https://doi.org/10.48550/arXiv.2607.06651) |
| 正式出版 | 截至 2026-10-13 官方版本页未列期刊 / 会议出版；不编造正式 DOI |
| 许可 | 官方 v1 的 license 与上传 PDF 内嵌 `/License` 均为 **CC BY-NC-ND 4.0**；原字节非商业收录 [paper.pdf](paper.pdf)，见 [source.md](source.md) |
| 阅读范围 | 完整 12页，包括 pp. 6–9 的理论证明、p. 12 参考文献；无另列附录。未运行端侧实验 |

以下页码均为上传 PDF 的**物理页码**。区分**原文报告**、**整理者推导 / 计算 / 评估**与**待核实**；压缩包分类不披露或推断用户的创新点。

## 摘要

**整理者归纳，pp. 1–5。** 针对客户端模态缺失、算力 / 上传预算不同的 multimodal FL，把本地累计 model delta 按层 tensorize 为三阶张量，用 matrix product state（MPS / tensor-train）三个 cores 传输。客户端以 top-q singular-value energy 的 spectral entropy 估计各层压缩复杂度，用 entropy-guided bond rank 和设备预算决定 payload；服务器逐层只在拥有该模态的 eligible clients 间聚合。

在 15-node Raspberry Pi4/5、AV-MNIST、Dirichlet $\alpha=0.1$、50轮 / 全参与实验，light compression 最终97.73%（FedAvg95.72%），heavy 平均压缩56.82×、至95%阈值传输0.51GB。accuracy相对提升是**2.01个百分点**；压缩比56.82×与总阈值通信66×口径不同，也来自不同压缩等级。

## 背景、已有方法不足与贡献

**原文，pp. 1–3。** Uniform rank / bit-width 不区分不同模态 branch 的谱结构与设备预算，可能在某层压缩过度、在另一层浪费通信；把缺失模态客户端纳入平均会稀释该层有效更新。本文结合逐层谱熵、每客户端 scalar payload budget、MPS 与 eligible-client normalization。

**原文贡献，pp. 2、6–9：** majorization 条件下证明 spectral diffuseness 与最低误差目标秩的排序；给两步截断 MPS 的误差上界；把压缩误差加入 nonconvex FL bound；推导 continuous convex surrogate allocation 的 KKT 与单调性，再给整数 / 设备可行性修正。形式化结论与实际采用的 entropy proxy、三-core reshape、整数策略必须分别看待。

**边界，整理者归纳：** 任务是图像 / 音频 digit classification 的小模型累计 model updates，不是 LoRA / MLLM 专项实验。没有 DP、安全聚合或梯度泄漏攻击评估；把 raw data 留在设备不自动形成形式化隐私。

## 方法与核心公式

### Delta、active layers 与模型状态

**原文，pp. 2–3 式 (1)–(4)、p. 5 算法1。** 客户端从 $w_t$ 做 E 步本地SGD，发送对象定义为

$$
G_k^t=\Delta w_k^t=w_t-w_k^t.
$$

服务器用减法更新，因此这里 delta 的符号与写 $w_k-w_t$ 的论文相反；复现不能混用。Global parameters 为 modality-specific encoders 与 shared fusion，local classifier / fusion adapters 留设备（p. 4）。每客户端只更新 $\mathcal L_k$ 中其拥有模态相关的层。

### Tensorization 与精确 scalar payload

**原文，p. 3 式 (5)–(8)、pp. 4–5。** 对 $G_{k,\ell}\in\mathbb R^{m_\ell\times n_\ell}$，取 $m_1m_2\ge m_\ell$ 且两因子尽量接近，zero-pad 然后 reshape 为 $m_1\times m_2\times n_\ell$：

$$
\mathcal G(i_1,i_2,i_3)\approx A^{(1)}[i_1]A^{(2)}[i_2]A^{(3)}[i_3].
$$

三个 cores 为 $m_1\times1\times r$、$r\times m_2\times r$、$r\times n_\ell\times1$；两步截断 SVD 的 SV 吸收进下一 core，不单独发送。精确 scalar数

$$
\phi_\ell(r)=m_1r+m_2r^2+n_\ell r,
\qquad \rho_{k,\ell}=\frac{m_\ell n_\ell}{\phi_\ell(r)}.
$$

预算 $C_k$ 是**每轮可发 scalar 数**，不是直接 MB、FLOPs 或含包头的线速。二次项 $m_2r^2$ 不能忽略；MPS bond rank 不等于原矩阵简单截断SVD的 rank。服务器顺序 contract cores，删 padding，恢复原形状。

### 熵估计、预算与整数修正

**原文，p. 4 式 (9)–(17)。** 固定 q，取 leading SV：

$$
\hat p_i=\frac{\hat\sigma_i^2}{\sum_{j=1}^{q}\hat\sigma_j^2},
\qquad \hat H_{k,\ell}=-\sum_{i=1}^{q}\hat p_i\log\hat p_i,
\qquad \bar r_{k,\ell}=\alpha_k e^{\hat H_{k,\ell}/2}.
$$

这里 $\alpha_k$ 是客户端预算缩放，实验 Dirichlet $\alpha=0.1$ 是另外一个量。对 $\sum_\ell\phi_\ell(\bar r_{k,\ell})\le C_k$ 二分求缩放，然后投影至整数 / $[r_{\min},r_{\max}^{(k)}]$。超预算则从最低熵层逐个减秩，剩余预算向高熵层分配；1D bias / 小参数直接用 $r_{\min}$。理论 / 主文没有列最终每设备的 $r_{\min},r_{\max},C_k$ 全部数值，必须以给出的 compression target / mean ratio 与实际可行秩区分。

**整理者评估：** 若预算低于所有 active层的 minimum-rank payload，最低秩下仍不可行；正文未展开该边界 / fallback。zero-norm update 的能量分母为0时如何处理，也未说明。整数 bounds / correction / 设备异构会破坏无约束跨层的单纯熵排序，不能宣称任意两层“熵较大必取较大rank”。

### 缺失模态的服务器聚合

**原文，p. 5 式 (19)、算法1。**

$$
S_t^\ell=\{k\in S_t:\ell\in\mathcal L_k\},\quad
\hat G_\ell^t=\sum_{k\in S_t^\ell}\frac{n_k}{\sum_{j\in S_t^\ell}n_j}\hat G_{k,\ell}^t,
\quad w_{t+1,\ell}=w_{t,\ell}-\hat G_\ell^t.
$$

若 $S_t^\ell$ 为空，该层保持。此处每层分母不同，不能等价写成所有客户端统一加权后以缺失层zero填充。

## 理论分析：条件与实际机制的区别

### MPS误差与谱熵排序

**原文，pp. 6–7，Assumption V.1、Proposition V.1、Remark1、Theorem V.1。** 两个 MPS unfolding 的 tail-energy 指数衰减假设 $\sum_{j>r}p_j^{(s)}\le A_se^{-\alpha_s r}$，用于相对误差上界

$$
\frac{\|G-\hat G_r\|_F^2}{\|G\|_F^2}\le\frac{\Psi_{k,\ell}}{r},
\qquad \Psi_{k,\ell}=C_{1,\ell}e^{H^{(1)}_{k,\ell}}+C_{2,\ell}e^{H^{(2)}_{k,\ell}}.
$$

两个 unfolding 熵与原矩阵 entropy 不是同一量。作者明确承认 reshape 保存Frobenius范数但不保存奇异谱；实现以原矩阵 top-q 熵作为低成本 proxy，不声称与 $\Psi$ 精确相等。误差界中的谱常数 / tail assumption 未在所有层实测验证。

设 tail mass $\tau=\sum_{i>q}p_i$，Remark1：

$$
|H-\hat H|\le h_2(\tau)+\tau\log p.
$$

只有 tail mass 小且熵差超过双方扰动 margin 时，截断熵排序才有保证；q=10本身不保证 tail small。

最低误差目标 rank $r^*(\epsilon;p)=\min\{r:\sum_{i>r}p_i\le\epsilon^2\}$。**若能量分布 $p\succ p'$（majorizes）**，则 $H(p)\le H(p')$ 且 $r^*(\epsilon;p)\le r^*(\epsilon;p')$。这是 majorization 条件下的共同排序；仅看熵标量高低不能推出所有谱都满足 rank 排序，也不是任意tensorization的MPS最小bond-rank定理。

### 收敛界

**原文，pp. 6、8，式 (25)–(28)、Theorem V.2、式 (50)。** 假设 L-smooth、full participation、$\eta\le1/(4LE)$，本地累计delta conditional mean **恰等于** $\eta E\nabla F_k(w_t)$，以及 local-update variance / heterogeneity有界，令重建 $\hat G_k^t=G_k^t+e_k^t$：

$$
\frac1T\sum_{t=0}^{T-1}\mathbb E\|\nabla F(w_t)\|^2
\le\frac{4(F(w_0)-F^*)}{\eta ET}+4L\eta E\sigma^2+8L\eta E\delta^2
+\frac{5}{\eta^2E^2T}\sum_{t,k}\frac{n_k}{n}\mathbb E\|e_k^t\|^2.
$$

**整理者评估：** 多步local SGD一般有drift，精确conditional-mean条件比“SGD无偏”更强。若压缩误差不衰减，末项可留下误差floor，不能无条件宣布与未压缩FL同速收敛到stationary point。证明采用全模型统一 $n_k/n$ 加权；实际缺失模态采用式19的每层eligible denominator。正文未单独证明这种归一化和非参与模态如何满足全模型条件；不能把TheoremV.2推成任意partial participation / missing modality的通用保证。

### 凸 surrogate 与实际秩规则

**原文，pp. 8–9，Theorem V.3、式 (58)–(70)。**

$$
\min_{r_\ell>0}\sum_{\ell}\frac{\psi_\ell}{r_\ell}
\quad\mathrm{s.t.}\quad\sum_\ell(a_\ell r_\ell+b_\ell r_\ell^2)\le C_k.
$$

正复杂度、可行payload条件下连续问题严格凸；精确二次budget的KKT为

$$
\frac{\psi_\ell}{r_\ell^2}=\lambda_k(a_\ell+2b_\ell r_\ell).
$$

线性budget $b_\ell=0$ 下：

$$
r_\ell^*=\frac{C_k\sqrt{\psi_\ell/a_\ell}}{\sum_j\sqrt{a_j\psi_j}}.
$$

**整理者评估：** 实现的 $r\propto e^{\hat H/2}$ 是 surrogate-complexity proxy / linearized scaling 后再保证预算可行的策略；一般不等于精确二次budget的KKT解，且不同 $a_\ell$ 还改变线性最优比例。Theorem的单调性在固定payload系数 / multiplier条件下成立，不能跨不同形状 / hardware bounds直接推广。原文摘要“solves convex surrogate”需保留这一 continuous optimality vs practical heuristic 区别。

## 实验设置

**原文，p. 9。**

| 项目 | 配置 |
| --- | --- |
| 真实设备 | 5×Pi4B：Cortex-A72 1.8GHz、8GB RAM、64GB storage、B16；10×Pi5：Cortex-A76 2.4GHz、16GB RAM、128GB storage、B32 |
| 网络 | 局域Ethernet switch至central server；Pi4 assigned tighter compression target；不是无线WAN测量 |
| 数据 | AV-MNIST：60k train / 10k test配对，28×28灰度图与1,000维MFCC（20coeff、8kHz、hop160）、10classes |
| Non-IID / modalities | Dirichlet0.1；随机分image-only / audio-only / multimodal profile；multimodal 更新encoders+fusion |
| Model | CNN image encoder、MLP audio encoder、two-layer fusion、10class输出 |
| Training | 50rounds、full participation、E5 local SGD steps、lr0.01；q10 |
| Targets | Light Pi5 2–10× / Pi4 5–10×；moderate Pi5 30–50× / Pi4 40–60×；heavy Pi5 40–60× / Pi4 60–80× |
| Baselines | FedAvg uncompressed；TopK s1% + error feedback；QSGD4bit；PowerSGD rank4 |
| 统计 | 图1 loss带是across-client std；无明示重复runs / seed置信区间，不能当multi-seed uncertainty |

## 主要结果与适用范围

**原文，p. 10 表I / 图1–3、p. 11 表II；AV-MNIST0.1，15设备全参与。**

| 方法 | Final accuracy | Mean ratio | Rounds@95% | MB/rnd | Compression s | Transmission s | Total TX GB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FedAvg | 95.72% | 1.00× | 47 | 48.85 | 0.01 | 4.89 | 33.63 |
| TopK1% | 93.4% | 10.2× | 48 | 4.79 | 0.02 | 0.48 | 3.37 |
| QSGD4bit | 92.1% | 8.0× | >50 | 6.11 | 0.02 | 0.61 | 4.54 |
| PowerSGDr4 | 95.8% | 12.1× | 43 | 4.04 | 0.18 | 0.40 | 2.54 |
| MESH-FL light | **97.73%** | **9.36×** | 31 | 5.56 | 0.22 | 0.56 | 2.52 |
| MESH-FL moderate | **96.47%** | **40.52×** | 40 | 1.25 | 0.31 | 0.12 | 0.73 |
| MESH-FL heavy | **96.20%** | **56.82×** | 40 | 0.88 | 0.38 | 0.09 | 0.51 |

**整理者计算 / 解释：** light vsFedAvg=+2.01个百分点，heavy vsFedAvg=+0.48个百分点；56.82×和最大accuracy不是同一压缩等级。表II的TotalTX被正文解释为到95%accuracy累计传输，33.63/0.51≈**65.94×**。Comp+Trans：light0.78s、moderate0.43s、heavy0.47s、FedAvg4.90s，只是表中压缩+传输项，不包括每客户端E-step training、所有aggregation / synchronization，不能当完整wall-clock training time。

**数据口径待核实：**

- 表I TopK final93.4%却填Rnd@95%=48，可能早期达阈值后下降，也可能阈值记录不一致；正文没给TopK完整曲线来分辨。QSGD>50且表II仍列TotalTX，应视训练预算内累计值 / 原文记录，不能称它成功达到95%。
- Per-client mean MB ×15×rounds 与TotalTX并非所有行严格一致，mean ratio也不等于mean uncompressed MB / compressed MB（不同平均权重 / 时间区间可能造成）；正文没定义足够细的计数账。保留原数，不自行补充精确总字节、双向通信、headers/重传规则。
- TopK只保留1%却ratio10.2×，不等于100×；可能带坐标 / protocol成本，但原文未展开具体表示，不补造理由。
- 正文归因“过滤client-specific高频谱分量”的generalization机制是作者解释，p.12明确说accuracy提升无正式理论解释；不是已证明压缩必提升泛化。

## 消融与局限

**原文，pp. 11–12 图5。** 相同moderate budgets下uniform-rank MPS **94.88%** vsentropy-guided **96.47%**（+1.59个百分点）；uniform未在50轮内达95%，MESH-FL40轮；TotalTX至少0.92GB vs0.73GB；Comp+Trans0.41s vs0.43s。该消融说明本任务 / budget下rank allocation有收益，没有单独消融eligible aggregation、modality比例、q、tensorization与设备预算。

**原文局限（p.12） / 整理者评估：**

- 指数tail-decay假设没有跨所有层 / regime验证；原矩阵entropy不是两个MPS unfolding entropy的精确替代。
- continuous surrogate最优性不等价于实际指数缩放 / 整数corr在精确二次budget下全局最优；预算不足与zero-update需要实现规则。
- full-participation / local mean条件与实际missing-modality layer normalization存在证明适用边界；不覆盖任意asynchronous / partial-client FL。
- 一套AV-MNIST、15节点、50轮，未展示更大模型 / MLLM或任务广度；无multiple-seed置信度。
- 计算 / 网络表仅给压缩与传输部分，TotalTX与平均payload的详细口径需核查；不等于端到端实际wall-clock / energy全账。
- 未提供DP、secure aggregation或attack evaluation，通信压缩不是隐私保证。

## 复现信息与阅读结论

**已取得 / 未执行。** 上传12页、全部证明与参考文献、官方arXivv1、内嵌license / arXivID已核实；Poppler检查首页、rank公式、theorem与两主表。正文没有可核实的MESH-FL官方实现仓库链接；参考文献FSDD的GitHub为**数据集**，不误标为方法代码。

复现需要完整encoder/fusion结构、client模态分配seed / 类别划分、$C_k$ / rank bounds、integer projection规则、tensor reshape / padding、q10 retained-energy记录、scalar dtype、计算 / 传输计时与累计账以及多runs统计。本文陈述可用于复现的部分已记录，缺失信息明确标为限制，不填任意默认值。

**整理者结论：** 实质证据是“逐层谱熵proxy + 三-core MPS + per-device budget + eligible-client aggregation”在指定heterogeneous实机任务下的效率取舍。保持majorization条件、proxy与真实MPS谱的差异、continuous/整数allocation区别、95%阈值成本与compression ratio的不同口径。

[来源与原件](source.md) · [BibTeX](citation.bib) · [仓库总览](../../../README.md) · [跨论文比较](../../../comparison.md)
