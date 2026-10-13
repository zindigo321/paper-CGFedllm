# Federated Fine-Tuning on Heterogeneous LoRAs With Error-Compensated Aggregation

## 文献信息与阅读对象

| 项目 | 核对结果 |
| --- | --- |
| 作者 | Wanyi Ning, Jingyu Wang, Qi Qi, Haifeng Sun, Daixuan Cheng, Cong Liu, Lei Zhang, Zirui Zhuang, Jianxin Liao（PDF p. 1） |
| 发表渠道 | IEEE Transactions on Neural Networks and Learning Systems，36(10)，October 2025，17826–17840 |
| 实际阅读版本 | IEEE Xplore 正式排版件，15 物理页；主文至 p. 13、参考文献 pp. 13–14、作者简介 pp. 14–15；无独立附录；页脚含机构下载水印 |
| 版本日期 | PDF p. 1：2024-11-27 received、2025-04-29 revised、2025-06-26 accepted、2025-07-17 publication、2025-10-09 current version；目录年依上传正式版本为2025，不依文件下载日期 |
| DOI | [10.1109/TNNLS.2025.3586545](https://doi.org/10.1109/TNNLS.2025.3586545) |
| 官方代码 | [ningwanyi/ECLoRA](https://github.com/ningwanyi/ECLoRA)，上传 p. 2 脚注指向并已核实作者仓库 |
| 许可与引用 | IEEE All rights reserved，公开目录未含原 PDF；[source.md](source.md)；[citation.bib](citation.bib) |

阅读全文、47 条参考文献及作者简介；页码一律为用户上传件物理页码。元数据及作者代码静态核验日期2026-10-13。以下区分论文主张、直接表中结果和整理者判断；未运行训练或复现实验。目录分类只按用户提供压缩包，不解释用户创新点。

## 摘要

ECLoRA 允许各客户端使用不同 LoRA rank，服务器先重构各客户端完整维度更新 $`B_iA_i`$ 并按数据量平均，再加入上一轮服务器分解残差，以 randomized SVD（RSVD）近似低秩分解，按客户端 rank 截断下发。目的同时避免最弱客户端限制共同 rank 和全量 SVD 的服务器开销。100 客户端、10% 参与、rank∈{4,8,16,32,64} 的 RoBERTa-base/MRPC 上，表 II 的最佳评估指标为88.7±1.4，FedIT为83.8±1.1；聚合0.33s，FlexLoRA为9.64s（pp. 8–10）。论文报告平均 round-to-target speedup 1.54–3.01×，它是通信轮数收益，不是整体墙钟时间加速。公开代码的核心 EC 调用与论文公式有差异，见复现段落。

## 背景、不足与贡献

- **原文问题**：客户端资源异质时，同秩 LoRA 常取最小rank，限制有更多资源的客户端。不同rank直接平均因子又维度不一致（pp. 1–3，图 1）。
- **基线不足（原文）**：HETLORA零填充/截断丢信息；FLoRA堆叠需要下发较大模块及周期重初始化；FlexLoRA重构后经典SVD耗时高（pp. 2–3）。
- **贡献（原文）**：完整维度的更新聚合、RSVD降分解开销、服务器跨轮EC；给出泛化/收敛分析及β选择讨论；四种基础模型、六任务和更多异质/动态rank场景（pp. 2、4–8、10–13）。
- **整理者机制归纳**：EC处理服务器低秩分解误差；它不是top-k残差反馈，也不是可学习codec压缩。聚合 $`B_iA_i`$ 可避免单独平均A/B的额外交叉项，但客户端本地漂移和各自截断仍存在。

p.3表I以RoBERTa-base/MRPC说明rank预算折衷：rank1/4/64/128分别有592,898 / 2,362,370 / 37,751,810 / 75,500,546可训练参数，GPU memory8,094 / 8,116 / 8,570 / 9,618MB，throughput4.29 / 4.13 / 3.83 / 3.75 iterations/s，FL accuracy74.5 / 80.1 / 85.0 / 88.0。这是背景示例表；表I的rank4 accuracy80.1不等于表II FedIT83.8，原文未在该表完整给出两组条件，本笔记不把它们合成同一实验。

## 方法流程与核心公式

预训练主干 $`W_0`$ 冻结，客户端 $`i`$ 训练 $`B_i\in\mathbb R^{d\times r_i}`$、$`A_i\in\mathbb R^{r_i\times m}`$。论文省略LoRA常数缩放，表示为 $`W'=W_0+B_iA_i`$（p. 2，式 1）。每轮重构并聚合（p. 4，式 3–4）：

$$
\Delta W_t=\sum_{i\in S_t}\frac{|D_i|}{\sum_{j\in S_t}|D_j|}B_{i,t}A_{i,t}.
$$

服务器补偿、分解和残差递推（p. 4，式 5–8；p. 5，算法 1）：

$$
\widehat{\Delta W}_t=\Delta W_t+\beta e_t,
\qquad
(U_r,\Sigma_r,V_r)=\operatorname{RSVD}_r(\widehat{\Delta W}_t),
$$

$$
B_t=U_r\Sigma_r,\quad A_t=V_r^\top,
\qquad
e_{t+1}=\widehat{\Delta W}_t-B_tA_t.
$$

这里 $`r`$ 为 involved rank set 最大值，$`e_t`$ 为上一轮残差，β默认1。上述将原文索引统一成算法1的前后轮关系，便于理解；不是另提新机制。按各自rank下发 $`A_t[:r_i,:]`$、$`B_t[:,:r_i]`$。原文算法1从t=0循环却下发 $`\theta^{t-1}`$、未显式给 $`e_0`$；复现需明确初始化和索引，不照抄越界。

RSVD先生成 $`\Omega\in\mathbb R^{m\times p}`$，默认oversampling维度 $`p=2r`$，然后（p. 5，式 9–12、图 3）：

$$
Y=\widehat{\Delta W}_t\Omega,\quad
Q=\operatorname{Orth}(Y),\quad
G=Q^\top\widehat{\Delta W}_t,
$$

$$
G=U_G\Sigma V^\top,\qquad U=QU_G.
$$

论文采用小矩阵SVD获取Orth，不直接规定QR。p. 5式12把中间因子维度写成p，而方法最终rank仍为r；引用的Lemma1及公开 `rsvd` 函数最后截断到目标r。应区分oversampling投影维度p和下发适配器rank r。

**复杂度（原文）**：RSVD为 $`O(2dmp+2dp^2+mp^2)`$，经典SVD为 $`O(\min(d^2m,dm^2))`$（p. 5，式13–14）；p.6正文将SVD随尺寸增长写成“exponentially”，与给出的多项式复杂度不一致，不据此声称指数复杂度。

**理论及范围**（pp. 6–8）：定理1假设loss/模型对更新权重Lipschitz且参数在有界球内，引入RSVD近似误差相关覆盖数；有关样本界的分母须满足正值，不能把更大rank必然提高实际精度当作无条件保证。定理2假设L-smooth、无偏随机梯度、有界局部/全局方差及梯度，并要求有uniform相对误差界的biased compressor：

$$
\|Q(x)-x\|^2\le q_Q^2\|x\|^2,\qquad 0\le q_Q<1.
$$

作者推导服务器EC的条件性 $`O(1/\sqrt{TKN})`$ 收敛趋势，K为本地步数；p.8明确其分析是完整维度SGD、LoRA特有的严格分析留待未来。p.7用于虚拟迭代消去残差的式17采用β=1的递推，不能直接给任意β套用同一消去关系。

β稳定性：若完整更新范数有界 $`G_u`$，则 $`\|e_{t+1}\|\le q_QG_u+q_Q\beta\|e_t\|`$，要求 $`|q_Q\beta|<1`$，可给出 $`\|e_\infty\|\le q_QG_u/(1-q_Q\beta)`$（pp.7–8，式19–25）。在这些假设下0<β≤1可满足稳定条件；论文没有证明真实RSVD在所有任意矩阵上都具有同一uniform q_Q。

## 实验设置

| 项目 | 原文条件 |
| --- | --- |
| 主模型 | RoBERTa-base 125M / large355M、DeBERTa-XXL1.5B、LLaMA-3.1-8B（p.8） |
| 任务/指标 | MRPC、QNLI、RTE accuracy；CoLA Matthews correlation；CoNLL03 F1；SQuAD exact match。表II报告各方法**最佳评估指标**，不是统一最终轮accuracy（p.9） |
| 客户端与rank | N100，每轮10%；FedIT同秩4；其余方法各客户端随机选{4,8,16,32,64}（p.8） |
| 优化 | 默认200 rounds；AdamW，lr2×10⁻⁴，前三轮warmup，之后linear decay；batch8；SQuAD max tokens384，其余128；β1；p2r；attention线性层LoRA（pp.5、8） |
| 随机统计 | 3 seeds，表II给标准差（p.8–9） |
| 环境 | Ubuntu22.04，4×RTX4090，Intel i9-13900K，125GB RAM（p.8） |
| 主要对比 | FedIT、HETLORA、FLoRA、FlexLoRA；补偿/投影/秩/Dirichlet/参与率/target module/epochs消融（pp.8–13） |

主设置p.8未明确本地epochs及Dirichlet α的默认值；p.11只给扩展的alpha集合0.6/1/10/100、IID和local epochs1/2/3。官方 `func_utils.py` 当前main默认local_epochs2、dirichlet_alpha1，但这是代码默认值，未当作论文每行实际使用值。复现应固定客户端rank分配、划分、每层缩放、随机投影种子及评估方式。

## 主要定量结果

p.9表II，3 seeds最佳指标均值±标准差：

| 模型/任务 | FedIT | FlexLoRA | ECLoRA |
| --- | --- | --- | --- |
| RoBERTa-base/MRPC | 83.8±1.1 | 87.5±1.5 | 88.7±1.4 |
| RoBERTa-large/MRPC | 86.2±0.9 | 88.7±1.2 | 89.7±1.1 |
| RoBERTa-large/RTE | 68.6±1.6 | 78.3±1.7 | 82.3±1.4 |
| DeBERTa-XXL/QNLI | 95.6±0.2 | 95.5±0.2 | 95.7±0.3 |
| LLaMA-3.1-8B/MRPC | 85.0±1.5 | **89.2±1.4** | 88.2±1.2 |

ECLoRA**并非所有任务最佳**：LLaMA/MRPC低于FlexLoRA；RoBERTa-base/CoLA 55.3±1.0低于FlexLoRA55.8±1.6，多个任务为并列。RoBERTa-base/MRPC相对FedIT+4.9是**百分点**（整理者相减），不是相对提升4.9%。表II六种不同指标的Avg列是原文混合平均，只作原文摘要，不能作为单一通用accuracy。

**达到目标轮数**（p.9表III；p.10）：ECLoRA对FedIT的模型平均speedup为base3.01×、large2.49×、DeBERTa1.59×、LLaMA1.54×。RoBERTa-large/MRPC目标85%，为4.16×；RTE目标67%，5.30×；LLaMA平均FlexLoRA1.68×高于ECLoRA1.54×。这些是轮数比，原文没有等同条件的全流程墙钟或累计上下行字节测量。

**聚合时间**（p.9表II）：FlexLoRA/ECLoRA：base9.64/0.33s、large15.25/0.52s、DeBERTa71.51/1.65s、LLaMA261.83/7.87s。整理者比值分别约29.2/29.3/43.3/33.3×；摘要“约40×”不是每个模型固定40×。对比FedIT更简单平均，ECLoRA本身更贵（large0.52s vs0.04s）。p.5的16384²单矩阵分解173.53s vs0.038s是另一个分解微基准，不与模型整体聚合时间混算。

## 消融、适用条件与局限性

- **分解与EC（原文）**：RoBERTa-large/MRPC，表VI目标86%（与主表III目标85%不同），SVD / SVD+EC / RSVD / RSVD+EC的Acc=88.7/89.9/88.2/89.7；speedup=2.70/2.83/2.77/3.31×；aggregation=15.25/15.33/0.46/0.52s；GFLOPs=1236.9/1236.7/54.7/54.9（p.11表VI；p.12）。本消融最优accuracy为SVD+EC89.9，完整ECLoRA胜在成本折衷。
- **β和p**：β∈{0,0.5,0.8,1}，β1曲线最佳；p2/3/4/5倍r的比较中默认2倍表现最好（pp.10–11，图5–6）。这是指定任务经验，不是普适最优定理。
- **秩配置**：RoBERTa-large/MRPC，{1,2,4,8,16,32} / {4,8,16,32,64} /整数[1,32] /整数[4,64]，ECLoRA89.2/89.7/88.7/89.7（p.10表IV）。
- **参与比例**：γ0.1/0.3/0.6/1下ECLoRA89.7/87.9/89.4/88.4，并非更多参与必定更高accuracy（p.11表V）。
- **多任务**：Natural Instructions v2，1613客户端各持不同任务，unseen clients加权ROUGE-L/1为57.7/65.5；FlexLoRA57.6/65.5（pp.12–13，表VII）。表头模型为`datajuicer/LLaMA-1B-dj-refine-150B`，正文称LLaMA-1.3B；记录两种原文名称，不自行认定参数完全一致。
- **动态rank**：每轮重新从{4,8,16,32,64}抽客户端rank，MRPC的RoBERTa-large/LLaMA曲线显示保持优势（p.13图10）；未提供可逐点引用的精确表格，不估读曲线数值。
- **label flipping**：RoBERTa-base/MRPC，25%恶意客户端时ECLoRA83.8%、FedIT/FlexLoRA均79.1%；0%时ECLoRA88.7%（p.13表VIII）。原文称“privacy attacks”，但这是投毒稳健性实验；不能据此证明抵抗成员推断、梯度反演或提供DP。
- **作者明确限制**：未修改RSVD本身；需改进分解效率及LoRA专属EC严格收敛分析（p.13）。
- **整理者判断**：服务器仍存储完整维度聚合矩阵和残差；只给服务器全局分解做EC，不单独补偿每个小rank客户端的截断损失。异构rank的预算与FedIT rank4不同，效用提高包含更高rank客户端能力；网络条件和安全保证需独立验证。

## 官方代码、数据与复现信息

已静态读取 [官方main入口](https://github.com/ningwanyi/ECLoRA/blob/main/main.py)、[run_eclora.py](https://github.com/ningwanyi/ECLoRA/blob/main/run_eclora.py)、[参数设置](https://github.com/ningwanyi/ECLoRA/blob/main/func_utils.py)。公开main分支在核验日可变，此处不宣称它是论文实验的固定commit。

**核心复现风险**：`run_eclora.py`计算`compensated_whole_param`后，实际调用`rsvd(whole_param[n], max_rank)`，输入仍为未补偿矩阵；残差随后才用补偿矩阵更新。该调用也没有使用参数`compensation_beta`。这与PDF p.4式8要求分解补偿矩阵不同；直接运行当前代码不能视作已经实现论文的EC。另该文件在分解前对重构聚合模型评估，与测量压缩下发模块的指标需区分。以上是静态核查，未验证训练表现、未修改作者代码。

官方参数文件默认local_epochs2、Dirichlet α1；公开`rsvd`将p设为min(2r,输入列数)，最后截断r，有助于区分论文的p/r记号。正式复现应先固定作者代码commit、确认EC输入及β、头部参数处理、rank-dependent LoRA scaling和目标指标；再执行3 seeds，分别计本地计算、服务器重构/分解及总通信。本次未安装模型、下载数据或运行复现实验。

## 阅读总结

**原文解决的问题**：资源不同的客户端以不同rank协作时，服务器兼顾完整更新聚合、快速低秩重分解和分解残差补偿。

**整理者归纳**：应将轮数收益、聚合时间和最终指标分开比较，并在复现前检查真正分解的张量是否包含上一轮残差。本文有针对异构LoRA的实验证据，严格收敛结论与正式隐私保障仍有明确范围。

## 单光子 LiDAR 参数

不适用。六种语言任务及Natural Instructions不涉及单光子器件、测距、阵列、光子统计或采集/重建时间。

[返回总览](../../../README.md) · [跨论文比较](../../../comparison.md) · [来源与许可](source.md)
