# From PowerSGD to PowerSGD+: Low-Rank Gradient Compression for Distributed Optimization with Convergence Guarantees

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 上传版完整题名 | From PowerSGD to PowerSGD+: Low-Rank Gradient Compression for Distributed Optimization with Convergence Guarantees |
| 作者，按上传版顺序 | Shengping Xie、Chuyan Chen、Kun Yuan；北京大学，Kun Yuan 为通讯作者（PDF p. 1） |
| 实际阅读版本 | arXiv:2509.11254v1，2025-09-14 提交；附件共 19 页，含正文、参考文献和附录 A–C；目录年份按该 2025 年阅读版 |
| 正式出版 | ICASSP 2026 - 2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)，IEEE，pp. 921–925；Crossref published / published-print 为 2026-05-03，会议日期为 2026-05-03 至 05-08 |
| 正式 / 预印本 DOI | [ICASSP: 10.1109/ICASSP55912.2026.11465020](https://doi.org/10.1109/ICASSP55912.2026.11465020)；[arXiv: 10.48550/arXiv.2509.11254](https://doi.org/10.48550/arXiv.2509.11254) |
| 官方核对来源 | [arXiv v1](https://arxiv.org/abs/2509.11254v1)、[IEEE 提交的 Crossref 元数据](https://api.crossref.org/works/10.1109/ICASSP55912.2026.11465020)、[IEEE Xplore](https://ieeexplore.ieee.org/document/11465020/)、[ICASSP 官方日程 SPTM-P2.2](https://www.cmsworkshops.com/ICASSP2026/view_paper.php?PaperNum=6804&bare=1) |
| 全文、引用与许可 | [官方 v1 全文](https://arxiv.org/pdf/2509.11254v1)、[source.md](source.md)、[citation.bib](citation.bib)；上传版为 arXiv 非独占分发许可，按仓库约定不公开复制附件 PDF |

**范围声明：** 本笔记完整阅读的是实际上传的 19 页 v1，所有页码为 PDF 物理页码；正式会议记录为 5 页，正式 PDF 未取得，未完成两版逐段对照。IEEE 直接页面出现验证限制；正式题名、作者顺序、日期和 pp. 921–925 由出版社提交的 Crossref 核实，会议日程独立核对题名与作者。正式题名的 For / With 大小写按正式记录保留。核对日期：2026-10-12。

## 摘要

PowerSGD 用单步 power iteration 跟踪梯度的低秩子空间，并用 error feedback（EF）保留未传输残差。本文构造满足其假设的随机优化反例，说明该子空间可能被锁在与有效梯度正交的方向，残差回馈本身不足以恢复收敛。PowerSGD+ 每隔若干步对**全局 EF 校正更新**做 SVD，重新取得 rank-r 子空间，其余步骤保持单步迭代；原文给出 MSGD 的期望平均梯度平方范数上界（pp. 3–7、11–18）。实验使用 4 张 RTX 4090：RoBERTa-Base / GLUE 的原表平均分为 86.28，PowerSGD 为 85.73；LLaMA-60M / 130M 的 C4 预训练结果在四个 rank / 模型配置中有三个 PPL 优于 PowerSGD（pp. 6、8–9）。它是同步分布式全参数训练的梯度通信压缩方法，没有给出差分隐私机制，也未验证 7B 联邦 LoRA 场景。

## 背景、已有方法不足与贡献

- **背景（原文）：** 数据并行训练需要交换完整梯度；低秩结构支持减少传输元素。与量化、稀疏化相比，PowerSGD 的共同基底使压缩表示能够通过 All-Reduce 聚合，QR 较频繁 SVD 更便宜（pp. 1–2）。
- **问题（原文）：** 单步迭代复用上一步辅助基底，隐含主子空间变化较慢；快速变化 / 高噪声下，投影可能保持错误方向。历史 EF 残差继续沿同一不合适子空间投影时，不能仅凭“有 EF”认定存在统一收缩常数（pp. 3–6）。
- **贡献（原文）：** 给出不收敛反例；引入周期性最优 rank-r 压缩 safeguard；推导 MSGD 收敛界；在语言模型微调 / 预训练中比较固定低秩压缩（pp. 2、6–9）。
- **阅读边界（整理者归纳）：** 反例否定的是一般保证，不能改写成所有 PowerSGD 训练都会失败；收敛指标是驻点相关的平均梯度平方范数，不是任意非凸问题的全局最优值保证。

## 问题定义、压缩器与假设

各节点共享模型矩阵，优化目标为（p. 1，式 (1)）：

$$
\min_{X\in\mathbb R^{m\times n}} f(X),\qquad
f(X)=\frac1N\sum_{i=1}^{N}f_i(X),\qquad
f_i(X)=\mathbb E_{\xi^{(i)}\sim D_i}F(X;\xi^{(i)}),\quad m\ge n.
$$

这里  $`N`$  是同步 workers 数， $`r`$  是压缩秩， $`1\le r\le n`$ 。压缩对象是梯度 / 更新矩阵；模型权重和训练参数并未因此变成 LoRA 适配器。

**收缩定义与最优 SVD 压缩（原文，p. 3，式 (2)–(6)）：**

$$
\mathbb E_{\mathcal C}\lVert\mathcal C(\Delta)-\Delta\rVert_F^2
\le (1-\delta)\lVert\Delta\rVert_F^2,\qquad 0<\delta\le1.
$$

$$
\mathcal C_P(W)=PP^\top W,\qquad P^\top P=I_r,\qquad
\lVert\mathcal C_P(W)-W\rVert_F^2+\lVert\mathcal C_P(W)\rVert_F^2=\lVert W\rVert_F^2.
$$

取  $`W=U\Sigma V^\top`$  的前  $`r`$  个左奇异向量作为  $`P`$ ，原文得到  $`\delta=r/n`$  的误差界。式 (5) 的最优化写法须结合定义 2 的半正交约束理解，不能无约束地解释为任意矩阵优化。

| 理论假设 | 原文内容与出处 | 使用范围 |
| --- | --- | --- |
| Assumption 1 | 全局目标下有界且 L-smooth（p. 3） | 非凸分析；未要求全局凸性 |
| Assumption 2 | 各节点随机梯度无偏，局部方差不超过 sigma 平方（p. 3） | 是随机梯度噪声条件，未定义 DP 加噪机制 |
| Assumption 3 | 全局真梯度平方范数不超过 omega 平方；全局随机梯度二阶矩可用 G 平方界定（p. 4） | 不能自行换成无条件适用于任意 LLM 的事实 |

原文记  $`G^2=\sigma^2+\omega^2`$ 。本文的  $`\delta=r/n`$  是压缩收缩系数， $`\sigma^2`$  是随机梯度方差， $`\epsilon`$  是优化精度；都不是本仓库其他 DP 论文中同名符号的隐私参数。

## 算法流程：EF、共同基底与周期性 safeguard

### 本地更新、误差缓存与模型更新

算法 2 / 式 (7)（pp. 4–5、7）每步先计算本地随机梯度，加入本地历史残差：

$$
g_t^{(i)}=\nabla F(X_t;\xi_t^{(i)}),\qquad
\Delta_t^{(i)}=g_t^{(i)}+e_t^{(i)},\qquad
\Delta_t=\frac1N\sum_i\Delta_t^{(i)}.
$$

压缩器分别返回本地近似和全局近似；残差必须按**本地近似**更新，而模型使用全局平均近似：

$$
e_{t+1}^{(i)}=\Delta_t^{(i)}-\widehat\Delta_t^{(i)},\qquad
m_t=\mu m_{t-1}+\widehat\Delta_t,\qquad
X_{t+1}=X_t-\eta m_t.
$$

原算法初始化  $`e_0^{(i)}=0`$ 、 $`m_{-1}=0`$ ， $`0\le\mu<1`$ ，辅助矩阵  $`Q_{-1}\in\mathbb R^{n\times r}`$ 。本地 EF 缓存通常仍为完整  $`m\times n`$  矩阵；本文没有证明优化器状态或全部训练显存同时变成低秩大小。

### SSP-Comp：两次 All-Reduce 与共享投影

算法 1（p. 4）先在各节点计算  $`P_t^{(i)}=\Delta_t^{(i)}Q_{t-1}`$ ，对这类  $`m\times r`$  矩阵 All-Reduce Mean，再对共同结果做 economic QR。原文的 QR 函数只返回半正交基底。随后每节点用共同基底得到  $`n\times r`$  的坐标矩阵，执行第二次 All-Reduce：

$$
P_t=\frac1N\sum_i\Delta_t^{(i)}Q_{t-1},\qquad
\widetilde P_t=\mathrm{QR}(P_t),\qquad
Q_t^{(i)}=(\Delta_t^{(i)})^\top\widetilde P_t,\qquad
Q_t=\frac1N\sum_i Q_t^{(i)}.
$$

$$
\widehat\Delta_t^{(i)}=\widetilde P_t(Q_t^{(i)})^\top,\qquad
\widehat\Delta_t=\widetilde P_tQ_t^\top
=\widetilde P_t\widetilde P_t^\top\Delta_t.
$$

这是单步 power iteration，而非迭代到最优 SVD 方向。基底只需在该步骤对各节点共同；它会随时间更新，不是 FFA-LoRA 的永久冻结因子。算法 2 使用名称 QR-COMP，算法 1 使用 SSP-Comp，结合第 3 节可理解为同一单步压缩路径（pp. 4–7）。图中红色 PowerSGD 行与绿色 PowerSGD+ 分支表示两种替代方案，不应在同一步重复执行两遍 QR 压缩。

### SVD-Comp：刷新步骤确实交换完整矩阵

当  $`t\bmod\tau=0`$ （含  $`t=0`$ ）时，PowerSGD+ 用 SVD-Comp 替换 SSP。算法 1 先 All-Reduce 完整  $`\Delta_t^{(i)}`$ ，得到全局 EF 校正更新  $`\Delta_t`$ ，再求其 SVD，并以左奇异向量前 r 列更新共同基底。之后仍生成本地  $`Q_t^{(i)}`$ 、平均  $`Q_t`$ 、本地与全局近似（pp. 4、6–7）。

**整理者归纳：** 它没有 AutoEncoder、TGAP 训练或长期收集训练梯度的阶段；但 safeguard 不是只传低秩因子，周期性全矩阵通信和 SVD 都有成本。实现需保证共同 Q 初始化、QR / SVD 基底一致性及数值退化处理；文中没有给出完整种子、广播或确定性同步方案。

## 不收敛反例与收敛保证的边界

### PowerSGD 的反例

原文式 (10)（p. 6）令  $`X\in\mathbb R^{2\times2}`$ 、 $`D=(1,-1)^\top`$ 、B 为全 1 的 2×2 矩阵， $`f_i(X)=\psi(D^\top XD)`$ 。函数在  $`|s|\le1`$  时为  $`\psi(s)=s^2`$ ，其余为  $`\psi(s)=2|s|-1`$ 。随机梯度为：

$$
g_t^{(i)}=\nabla f(X_t)+\xi_t^{(i)}\bigl(\sigma B-\nabla f(X_t)\bigr),
\qquad \Pr(\xi_t^{(i)}=1)=\Pr(\xi_t^{(i)}=-1)=\frac12.
$$

各节点随机变量独立。附录 A（pp. 11–13）在所有节点初始噪声符号均为 +1 的事件下，跟踪秩 1 的错误基底：更新沿 B，目标梯度沿  $`A=DD^\top`$ ，两者正交；EF 即使积累 A 方向残差，也可能继续被该投影消去。事件概率为  $`2^{-N}`$ 。原文定理 1 / 附录定理 3 声称存在满足假设的例子，使  $`\mathbb E\lVert\nabla f(X_t)\rVert_F^2\ge\epsilon_0>0`$ ，不限于选定的学习率或所举基础优化器（pp. 6、11）。

**待核实的证明细节：** p. 11 的目标为 `x11-x12-x21+x22`，随后梯度式的 psi 参数却为 `x11+x12-x21-x22`；初始基底使 `a+b=0` 或 sigma 为 0 时，该页直接断言 QR 输出固定 C 的步骤需要零矩阵分支定义。正的 epsilon0 也要求初始目标梯度非零。p. 12 的位移展开符号与式 (7c) 的减号不同，但“属于 B 的线性张成空间”的论证不因整体符号改变。这里记录作者的证明思路与疑点，未完成独立形式化证明，不把该结论扩大到所有名为 PowerSGD 的软件变体。

### PowerSGD+ 的定理和有限步依赖

附录 B 先证明普通投影误差不超过输入范数、SVD 刷新为 delta 收缩，进而约束**全局平均残差**和动量（pp. 13–16，Lemma 1–4）。关键界为：

$$
\mathbb E\left\lVert\frac1N\sum_i e_t^{(i)}\right\rVert_F^2
\le\frac{45\tau^2G^2}{\delta^2},\qquad
\mathbb E\lVert m_t\rVert_F^2\le\frac{92\tau^2G^2}{(1-\mu)^2\delta^2}.
$$

定理 4（pp. 16–18）在  $`\eta\le(1-\mu)/(2L)`$  的步长条件下给 MSGD 的界；令  $`\Delta F=f(X_0)-\min_X f(X)`$ ：

$$
\frac1T\sum_{t=0}^{T-1}\mathbb E\lVert\nabla f(X_t)\rVert_F^2
\le\frac{4(1-\mu)\Delta F}{\eta T}
+\frac{2L\eta\sigma^2}{(1-\mu)N}
+\frac{548L^2\eta^2\tau^2G^2}{(1-\mu)^4\delta^2}.
$$

原文定理 2 / Corollary 1 给出适当步长选择后的形式（pp. 7、18）：

$$
\frac1T\sum_{t=0}^{T-1}\mathbb E\lVert\nabla f(X_t)\rVert_F^2
\le\sqrt{\frac{32L\sigma^2\Delta F}{NT}}
+\frac{8L\Delta F}{T}
+\frac{6\sqrt[3]{274}(L\tau G\Delta F)^{2/3}}
{T^{2/3}\delta^{2/3}(1-\mu)^{2/3}}.
$$

- **原文报告：** 固定其他参数，渐近主项为  $`O(1/\sqrt{NT})`$ ，Remark 1 称达到优化精度 epsilon 需要  $`O(1/(N\epsilon^2))`$  步，并称 linear speedup（p. 7）。
- **整理者归纳：** 有限 T 的第三项依赖 tau、r/n 与 momentum；较长刷新周期或更低秩可能使它主导。不能把渐近阶不含 tau 改写成任意配置下“刷新周期对收敛没有影响”，也不能用步数线性加速替代 GPU / 网络 wall-clock 加速。
- **待核实：** p. 17 式 (17) 用跨节点平均噪声的方差 `sigma^2/N`，需要条件独立 / 不相关等前提；Assumption 2 未单独完整列出此跨节点条件。算法及实验还需核实其实际采样实现。
- **适用范围：** 定理针对 MSGD；Adam / AdamW 被用于实验，未给出它们的对应 PowerSGD+ 收敛定理。非凸驻点界不等于全局最优解收敛。共同基底确定后，压缩对矩阵线性；数据依赖的基底选择整体不能被直接当作一个固定线性映射。

## 通信、计算与内存口径

表 2（p. 8）只列每步通信的矩阵元素规模；不含位宽、网络拓扑、节点数的 All-Reduce 传输倍数、协议、延迟和 SVD 时间。原文对照如下：

| 算法 | 原表 All-Reduce / EF | 原文每步元素规模 | 使用边界 |
| --- | --- | --- | --- |
| ATOMO | 否 / 是 |  $`mr+nr`$  | 原文称各节点局部 SVD 基底不一致，不能直接用相同基底的 All-Reduce |
| PowerSGD | 是 / 是 |  $`mr+nr`$  | 普通单步路径的两次小矩阵平均 |
| GaLore | 是 / 否 |  $`nr+mn/\tau`$  | 本文的分布式对照口径；不能自动套用所有 GaLore 实现 |
| PowerSGD+ | 是 / 是 |  $`mr+nr+mn/\tau`$  | 含周期性完整矩阵刷新这一量级项 |
| PowerSGD+，Approximation Top-r | 是 / 是 |  $`mr+nr`$  | 原文提出的替代收缩压缩器；本上传版未给该变体单独实验表 |

**整理者计算：** 相对每步完整 `mn` 元素，表 2 的摊销保留比为  $`r/m+r/n+1/\tau`$ ；其倒数只是等位宽下的元素比，不是测得的总网络收益。

若严格按算法 1，并用刷新步替换普通步：普通步传 `mr+nr`，刷新步传 `mn+nr`。一个完整 tau 步周期的平均是：

$$
\frac{(\tau-1)(mr+nr)+(mn+nr)}{\tau}
=mr+nr+\frac{mn-mr}{\tau}
\le mr+nr+\frac{mn}{\tau}.
$$

这是**整理者按伪代码计算**的逻辑元素数；表 2 是较粗的加法 / 量级口径，不直接称其数字错误。实际实现是否仍执行额外同步、分发共同基底或融合通信需核实。p. 8 的文字把通信对照称 Table 1，而实际通信表为 Table 2。

QR、矩阵乘法、周期性完整 SVD 与 EF 缓存均有代价。原文没有在本文给出累计网络字节、带宽、通信耗时、训练 tokens/sec、SVD 占比或峰值显存对照，故未建立端到端加速 / 显存减少结论。p. 8 指明 GaLore 使用 full optimizer state；不能把这里的比较直接当作 GaLore 内存优化实验。

## 实验设置与超参数

| 项目 | 原文内容与出处 |
| --- | --- |
| 环境 | 4 × NVIDIA RTX 4090，单卡 24 GB；数据并行度 4（pp. 8、18） |
| 微调 | RoBERTa-Base / GLUE，10 epochs，压缩 rank 4；AdamW；先对 PowerSGD 搜索配置，再迁移给其他方法（pp. 8、18–19） |
| 预训练 | LLaMA-60M / 130M，C4，10k / 20k steps；rank 4 或 8；附录 C.2 与表 5称标准 Adam（pp. 8、18–19） |
| 方法 | Full precision / Full rank、PowerSGD、GaLore、PowerSGD+；两种 PowerSGD 均有 EF（pp. 6、8–9） |
| DP / 隐私预算 | 未提供；不为其填写 epsilon、delta 隐私预算 |
| 不确定性 | 未报告多 seed 均值 / 标准差、置信区间和显著性检验；原表 Avg 是任务分数均值，不是重复训练均值 |

GLUE 的逐任务配置来自 p. 19 表 4；每项均训练 10 epochs，rank 4，AdamW betas 为 `(0.9,0.999)`，linear scheduler，warmup ratio 0.06，最大序列长度 512：

| 任务 | 总 batch | learning rate | weight decay | restart steps |
| --- | --- | --- | --- | --- |
| RTE | 16 | 2e-5 | 0.01 | 50 |
| CoLA | 32 | 2e-5 | 0.02 | 80 |
| SST-2 | 32 | 2e-5 | 0.01 | 80 |
| MNLI | 64 | 2e-5 | 0.01 | 200 |
| QQP | 32 | 2e-5 | 0.02 | 200 |
| STS-B | 32 | 2e-5 | 0.01 | 50 |
| MRPC | 64 | 4e-5 | 0.02 | 80 |
| QNLI | 32 | 2e-5 | 0.01 | 100 |

附录 C.1 明确 restart steps 仅用于 PowerSGD+ 与 GaLore，不用于不刷新的 PowerSGD（p. 18）。C4 表 5（p. 19）共同配置为：全局 batch 512、每设备 batch 128、序列长 256；warmup 10%，linear warmup 后 cosine decay 到 0；learning rate 搜索 `1e-3 / 2e-3 / 4e-3`，weight decay 0，gradient clipping 1.0。60M / 130M 分别训练 10k / 20k steps，warmup 1000 / 2000，token 数 1,310,720,000 / 2,621,440,000；PowerSGD+ 的 restart steps 为 200。

**待核实：** C.2 还写 C4 预训练“10 epochs”，未说明其与固定 steps / token 数、数据子集的关系；第 5 节总体描述 AdamW，C.2 / 表 5 写 Adam，需分任务核对。表 5 没有单列 GaLore 配置；库版本、模型 revision、数据 split、非矩阵梯度处理、SVD 同步和各配置最终 learning rate 未完整给出。

## 主要结果与平均分核算

### RoBERTa-Base / GLUE

以下按 p. 6 表 1 转置整理。八项原文报告均为 score，原文未逐任务明确 MRPC 的 Accuracy / F1、STS-B 的相关系数类型、MNLI 的子集等口径；不统一改写为 Accuracy。原文称 test results，但未给评估 split / 提交编号，仍待核实。压缩器均 rank 4，非 DP 实验：

| 任务 / 统计 | Full precision | PowerSGD | GaLore | PowerSGD+ | 数字性质 |
| --- | --- | --- | --- | --- | --- |
| CoLA | 62.89 | 60.58 | 62.64 | 62.85 | 原文报告 |
| STS-B | 90.29 | 90.65 | 89.68 | 90.67 | 原文报告 |
| MRPC | 92.41 | 91.68 | 91.96 | 92.54 | 原文报告 |
| RTE | 79.78 | 78.33 | 77.62 | 79.42 | 原文报告 |
| SST-2 | 94.38 | 94.15 | 94.15 | 94.38 | 原文报告 |
| MNLI | 87.20 | 87.47 | 87.50 | 87.08 | 原文报告 |
| QQP | 91.74 | 91.17 | 90.53 | 91.14 | 原文报告 |
| QNLI | 92.42 | 92.07 | 92.07 | 92.13 | 原文报告 |
| 原表 Avg | 86.35 | 85.73 | 85.70 | 86.28 | 原文报告 |
| 表内八项算术均值 | 86.38875 | 85.76250 | 85.76875 | 86.27625 | 整理者计算，基于表内已舍入分数 |

表注明 Avg 是跨任务均值，但前三列重新计算到两位小数分别为 86.39 / 85.76 / 85.77，与报告 86.35 / 85.73 / 85.70 不同；差异超过八项各自两位小数舍入所能解释的均值误差。PowerSGD+ 的 86.28 与重新计算舍入相符。保留原值，平均分计算口径 / 原始结果待核实。

**整理者计算：** 若按原表 Avg，PowerSGD+ 相对 PowerSGD / GaLore 增加 0.55 / 0.58 分，比 Full precision 低 0.07 分；若按八项算术均值，差为约 +0.51 / +0.51 / -0.11 分。PowerSGD+ 在 MNLI 与 QQP 低于 PowerSGD，不能称所有任务都领先。没有多 seed 统计，不把这些差值写成显著提升或统计等效。

### LLaMA / C4 预训练

p. 9 表 3 报告 **best validation PPL，越低越好**。Full rank 为每模型一个无压缩对照，非 DP；共同配置和刷新周期见上述表 5：

| 模型 / rank | Full rank | GaLore | PowerSGD | PowerSGD+ | 相对 PowerSGD 的 PPL 差 |
| --- | --- | --- | --- | --- | --- |
| LLaMA-60M / 4 | 29.88 | 94.96 | 36.11 | 35.46 | -0.65，整理者计算 |
| LLaMA-60M / 8 | 29.88 | 92.91 | 32.57 | 32.63 | +0.06，整理者计算 |
| LLaMA-130M / 4 | 23.06 | 92.93 | 27.60 | 27.36 | -0.24，整理者计算 |
| LLaMA-130M / 8 | 23.06 | 70.55 | 26.24 | 26.11 | -0.13，整理者计算 |

表中各 PPL 为**原文报告**；最后一列为整理者相减。PowerSGD+ 在三项优于 PowerSGD，但并非全部；相对 Full rank 仍有可见差距，例如 60M / rank 4 高 5.58 PPL。原文表注称 GaLore 在 rank 4/8 “diverged”，同时给出有限 PPL，未给本文中的发散判据或完整训练曲线；不能自动补写成 NaN、程序失败或所有 GaLore 场景不收敛。

## 消融与泛化证据

- **原文实验：** 图 1（p. 5）展示反例上 MSGD / Adam 的损失走势；表 1 是八个 GLUE 任务；表 3 比较 60M / 130M 与 rank 4 / 8。它们支持该配置下的实证比较，不是 7B / 多网络部署泛化验证。
- **证据不足：** 未给独立 tau 扫描、EF 开关、SVD / Approximation Top-r / random projection 刷新器的完整消融；表 4 的不同任务采用不同 restart steps，不能当作其他条件固定的 tau 对照。
- **泛化范围：** 没有客户端掉线、部分参与、多本地步的 cross-device FL、隐私噪声攻击或 C-Eval / MMLU 实验；不能用本篇小模型数值给本仓库 7B 方法排直接名次。

## 隐私分析与未覆盖范围

本文只证明优化收敛性质。All-Reduce、低秩投影与 EF 不构成经过证明的加密、secure aggregation 或差分隐私。刷新步骤会在 worker 集合内交换完整 EF 校正更新；普通步骤也发布数据依赖的投影 / 坐标。论文未指定攻击者、邻接关系、裁剪 / DP 噪声、privacy accountant、epsilon / delta 预算或统计量发布保护。与 DP 压缩器结合时，基底、残差、刷新消息与预算组合均需重新分析，不能把原文随机梯度方差直接当作隐私噪声。

## 与已有六篇论文的关系

以下为**整理者基于各篇已读版本的比较**；不是作者已经验证的组合方案，不能跨模型 / 数据 / 隐私条件直接排名。

| 论文 | 联系、区别与文献依据 |
| --- | --- |
| [CG-FedLLM](../2025-wu-cg-fedllm/notes.md) | CG 用 TGAP 真实时间序列因子训练 AutoEncoder，再在 FAF 中编码 / 重建（CG pp. 4–6、19）；PowerSGD+ 用当前 EF 校正更新做 power iteration / 周期 SVD，无学习压缩器预训练，但含周期完整矩阵通信（本篇 pp. 4–8）。两种“压缩比例”不能忽略各自阶段成本后排名 |
| [DR-Encoder](../2024-wu-dr-encoder/notes.md) | DR 用均值 / 标准差合成先验训练 AutoEncoder，并讨论 GDP / RDP（DR pp. 3–6、9）；PowerSGD+ 的方差假设和驻点收敛界没有提供 DP。本文可提供子空间刷新思路，不能证明 DR 的 learned encoder 为同一收缩算子 |
| [FFA-LoRA](../2024-sun-ffa-lora/notes.md) | FFA 共享冻结 A，使增量聚合线性（FFA pp. 4–6）；PowerSGD 的共享 P 让坐标平均对应压缩更新平均（本篇 p. 4 算法 1、p. 13）。后者基底随时间 / 数据变化，且训练的是完整参数梯度，不是永久冻结 LoRA 因子 |
| [FLASC](../2024-kuo-flasc/notes.md) | FLASC 保持本地 LoRA 稠密训练，Top-K 仅用于适配器上下行传输（FLASC pp. 4–7）；本篇压缩同步全参数梯度并用 EF / All-Reduce，通信表达式与达到目标效用的累计通信口径不同 |
| [AdaLoRA](../2023-zhang-adalora/notes.md) | AdaLoRA 分配可训练增量的方向 / 秩预算（AdaLoRA pp. 4–6）；PowerSGD+ 的 r 是梯度传输投影秩。动态 r 会改变 delta、基底维度和刷新设计，本篇固定秩定理不能不经分析直接套用 |
| [SVD-LLM](../2025-wang-svd-llm/notes.md) | SVD-LLM 白化主干权重 / 校准输出并做截断与恢复（SVD-LLM pp. 3–5）；本篇对全局校正更新周期做 SVD，不压缩部署权重，也没有白化校准目标。两者的 SVD 输入和误差定义不同 |

共同基底的聚合等式为（整理者展开算法 1）：

$$
\widetilde P_t\left(\frac1N\sum_i Q_t^{(i)}\right)^\top
=\frac1N\sum_i\widetilde P_t(Q_t^{(i)})^\top.
$$

它不同于对各客户端各自学习的 A、B 分别平均再相乘；此处没有不同客户端 P 因子之间的双重乘积项。它保证的是同一投影下的聚合一致性，不保证投影无误差，也不自动证明差分隐私。将周期 safeguard、EF、learned encoder、稀疏传输、冻结 LoRA 因子或动态秩结合，均为**未验证研究设想**，需要重做消息、状态、成本和收敛 / 隐私分析。

## 代码与复现信息

上传 PDF 未给出 PowerSGD+ 作者代码地址；2026-10-12 的题名 / 作者 / GitHub 检索未核实可归属于本文作者的官方实现。相关的 [epfml/powersgd](https://github.com/epfml/powersgd) 明确是早期 PowerSGD 参考实现，并说明其当前代码与原论文版本存在差异；不能当作本篇 PowerSGD+ 官方代码或已验证的反例实现。

复现前需取得：模型 / tokenizer revision、GLUE 评估 split 与指标脚本、C4 数据版本和采样量、全部 seeds、基础优化器的逐任务选择及最终学习率、初始化共同 Q、QR 零 / 秩亏输入规则、SVD 基底同步、残差缓存精度、非矩阵参数压缩规则、GaLore full optimizer state 的具体实现、刷新器和通信日志。附录 A–B 是证明，C / 表 4–5 是实验配置；不能把这些配置记录写成成功复现实验。本次未执行训练、反例数值实验、网络测速、形式化证明或隐私攻击。

## 阅读总结与局限

**整理者归纳：** 本文将“能做低秩近似”与“在整个随机优化过程中存在足够收缩 / 收敛控制”区分开。周期性 safeguard 给出明确的算法改动和有限步依赖，但需要额外完整矩阵通信与 SVD；理论与实证使用的基础优化器范围不同。当前证据适用于给定假设的同步 MSGD 分析，以及小规模语言模型的所列实验。平均分口径、部分证明记号、Adam / AdamW 与 C4 epochs 描述、官方代码和端到端性能仍待核实。

## 单光子 LiDAR 参数

不适用。本文没有探测器、阵列、距离、目标速度、SNR/SBR、每像素光子数、采集时间、成像帧率或定位误差。压缩秩、训练 steps、模型规模和 PPL 不能替代这些物理参数。

[返回总览](../../README.md) · [跨论文比较](../../comparison.md) · [版本与许可](source.md) · [引用](citation.bib)
