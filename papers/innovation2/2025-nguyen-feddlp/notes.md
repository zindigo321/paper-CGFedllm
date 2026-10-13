# Federated Multimodal Learning with Dual Adapters and Selective Pruning for Communication and Computational Efficiency

## 文献信息与阅读对象

| 项目 | 记录 |
| --- | --- |
| 方法真实名 | **FEDDLP / FedDLP：Federated Dual LoRA Pruning**（PDF p.1），不是FedDPA |
| 作者，上传版顺序 | Duy Phuong Nguyen、J. Pablo Muñoz、Tanya Roosta、Ali Jannesari |
| 阅读版本 | **arXiv2503.07552v1**，2025-03-10；10页，创建 / 修改时间2025-03-11 02:24:57UTC |
| 官方版本 / 全文 | [arXivv1](https://arxiv.org/abs/2503.07552v1)；[官方PDF](https://arxiv.org/pdf/2503.07552v1) |
| 正式出版关系 | 官方arXiv comments：Accepted at CCGrid2025；[作者实验室](https://swapp.cs.iastate.edu/publications)列CCGrid2025、pp.1–10，并链接 [DOI10.1109/CCGRID64434.2025.00011](https://doi.org/10.1109/CCGRID64434.2025.00011) / [IEEE记录11044852](https://ieeexplore.ieee.org/abstract/document/11044852) |
| 许可 / 原件 | 官方**v1** license为 **CC BY4.0**；原字节收录上传预印本 [paper.pdf](paper.pdf)，不以IEEE会议版权覆盖v1许可，见 [source.md](source.md) |
| 阅读范围 / 核对 | 2026-10-13；上传10页全文，含p.10参考文献，无另列附录；未取得或完整阅读IEEE正式PDF，未运行实验 |

以下页码为上传PDF**物理页码**。官方arXiv作者索引为J. Pablo **Munoz**，上传首页为**Muñoz**；保留上传拼写。正式稿作者元数据未完整取得，不把第三方Tanya G. Roosta替换进上传名单。区分**原文报告**、**整理者归纳 / 计算**与**待核实**。

## 摘要

**整理者归纳，pp. 1–2、5–7。** 以冻结CLIP为backbone，每客户端维护较大的local LoRA（initialrank4）与较小global LoRA（rank2）。两路分别更新、交替冻结，用各自classificationCE和双向logitKD交换知识；local adapter按SoRA式gate稀疏化以减少容量 / 过拟合，global adapter在服务器加权平均。

实验是CLIP image/text encoder**分别**添加adapter后的个性化图像分类，四数据集、10客户端、Dirichlet0.1/0.01。论文标题“Multimodal”来自CLIP的image-text模型，不等于已经验证missing modality、image-only/audio-only客户端混合或MLLM生成任务。p.10也把扩展到multi-modal tasks列为futurework。

## 背景、已有方法不足与贡献

**原文，pp. 1–4。** 非IID客户端单一同构LoRA易过拟合；local SoRA pruning改善个体适配，却使各客户端rank/结构不同，难直接聚合。方案将heterogeneous pruned local adapter留设备，同时保留一致global adapter进行共享。与FedDAT比较，作者强调两路独立训练而非组成一个combined model，并对local分支gate剪枝。

**原文，p.3图2。** Flowers102、10clients、Dirichlet0.1、imageencoder、rank2、不通信，SoRA比vanillaLoRA的后期local精度更稳定；这是单个preliminarysetup，不是通用structuredpruning收敛理论。

**贡献 / 边界，整理者归纳：** 核心是local personalization与低容量global share的结构分离 + mutualKD + localpruning。没有新的梯度codec、DP / 安全聚合或正式通信下界；global smallrank降低每轮交换对象，localpruning本身不一定直接降低发送字节，见协议冲突记录。

## 方法与核心公式

### 模型与双路损失

**原文，pp. 4–6；p.2图1、p.5图3。** 以冻结base $\Delta$ 和每客户端local/global adapter $\theta_k^{\mathrm{loc}},\theta_k^{\mathrm{glob}}$ 形成两条可分别计算logits的分支，优化client-data weighted loss。CLIP图像分类比较图像embedding与“a photo of a [class]”文本embedding的temperature-scaled cosine，选择最高类分数。p.4标题zero-shot evaluation是CLIP分类形式；训练阶段CE利用本地标签进行adapterfinetuning，不应称整个实验无监督/完全zero-shot。

**原文，p.6：**

$$
\mathcal L_{\mathrm{loc}}=\operatorname{CE}(z_{\mathrm{loc}},y)
+\alpha D_{\mathrm{KL}}(z_{\mathrm{loc}}\|z_{\mathrm{glob}}),
$$
$$
\mathcal L_{\mathrm{glob}}=\operatorname{CE}(z_{\mathrm{glob}},y)
+D_{\mathrm{KL}}(z_{\mathrm{glob}}\|z_{\mathrm{loc}}).
$$

论文式中直接写logits，真正KL需要概率分布；softmax、distillationtemperature、teacherdetach等实现细节主文未展开。保留原方向，不自行套成teacher-to-student的另一KL方向。

更新local时global冻结，更新global时local冻结。$\alpha$只控制localKD，globalKD权重固定1；本文$\alpha$不是Dirichlet浓度（该参数记为$\beta$），也不等于LoRAscaling。独立分支/知识蒸馏不应改写成简单相加两份低秩权重的训练架构。

### Pruning与发送内容

**原文，p.6 V-G：** localSoRA gate更新

$$
g_k^{t+1}\leftarrow T_\xi\left(g_k^t-\mu\nabla_{g_k}\mathcal L_{\mathrm{loc}}(\theta_k^t)\right),
\qquad\xi=5\times10^{-5}.
$$

$T_\xi$被正文称broadcasting thresholdfunction，去除不重要gate / 分量；主文未展开thresholdoperator的精确形式与最终rank分布。p.4关于SoRA的SVD / SV说明是作者对相关方法的介绍，此论文没有给完整SVD实施步骤；不把它增补为已实现的额外codec。

**协议的相互不一致，须保留：**

| 位置 | 原文陈述 |
| --- | --- |
| p.1、p.2图1、p.6V-E | Localadapter保持clientprivate，**只有globaladapter上传/下发并FedAvg加权**；inference=frozenbase+localLoRA |
| p.1另一段、p.5图3caption | 剪枝localadapter减通信 / 把prunedlocal和smaller global都聚合到server |

**整理者归纳：** 方法正文communicationsection与overview支持“onlyglobalshare”，本笔记采用它作为主协议；p.5caption等说法与此冲突，没有自行发明heterogeneous-localadapteraggregation。若只发送fixedglobalrank2，则localpruning对通信收益可能通过更快达到threshold而间接作用；需代码/正式版本确认，不能直接说“剪掉localweights就少上传这些weights”。

Inference只使用local分支见p.2caption；某些一般描述说两adaptercombined，不能将trainingKD与inferenceensembling混在一起。

## 实验设置

**原文，pp.7–8。**

| 项目 | 配置 |
| --- | --- |
| Model / scope | CLIP ViT-B/32，base冻结；在textencoder或imageencoder所有linearmodules分别加LoRA |
| Datasets | Oxford-IIITPet、Oxford102Flowers、FGVC-Aircraft、DescribableTexturesDataset(DTD) |
| Splits | 75%train/25%test随机split；10clients，Dirichlet$\beta=0.1$与0.01；评估各client自身testset平均accuracy |
| Training | 100rounds、各client每轮1localepoch、B32、AdamW；singleA10040GB |
| Adapters | FedDLP localinitialrank4、globalrank2；FLoRA rank2；FedDAT双rank2；Localrank2；FedCLIP两FCadapter |
| Seeds | 0,1,42三randomseeds，表I/II mean±std；表III/IV另列**跨clientstd与最差clientaccuracy** |
| Search | LoRA lr $5\times10^{-4}$ 至 $10^{-7}$ 共8候选；FedCLIP lr $5\times10^{-3}$ 至 $10^{-5}$ 共6候选；KD$\alpha$=100,10,1,0.1,0.01,0.001 |
| Pruning | $\xi=5\times10^{-5}$；gate-finalrank、rank随round变化未详细列表 |

原文p.8明确**on a testing set**选择gridsearch最佳设置；没有说明独立validation。可能存在testset参与选择的评估偏差，不能改写成完全独立held-outvalidation选择超参数。

## 主要结果与适用范围

### Meanaccuracy不是统一globaltestaccuracy

**原文，p.7表I/II；four-dataset平均为作者表值，±为三seedstd。**

| Adapter位置 / $\beta$ | FedDLP 平均accuracy | FedDAT 平均accuracy | FLoRA 平均accuracy | FedDLP相对FedDAT，百分点 |
| --- | --- | --- | --- | --- |
| Text / 0.1 | 81.03±0.56% | 79.05±0.72% | 71.22±0.69% | +1.98 |
| Image / 0.1 | 82.40±0.20% | 81.94±0.77% | 76.61±0.43% | +0.46 |
| Text / 0.01 | 81.58±1.18% | 78.13±2.30% | 63.77±0.89% | +3.45 |
| Image / 0.01 | 87.15±0.88% | 84.85±0.63% | 73.26±1.00% | +2.30 |

差为**整理者计算**，不表示显著性test。表内参数列text **0.223M**、image **0.334M** 与FedDAT / FLoRA相同；未明确该列是shared / totaltrainable / prune后实际parameter数的全部口径，不据此宣称本地总参数完全相同。

**原文具体行，p.7：** image/$\beta$0.01 Aircraft FedDLP **67.52±1.55%** vsFedDAT61.65±0.24%；text/$\beta$0.1 Flowers FedDLP95.26±0.19% vsFedDAT95.57±0.07%，并非所有dataset项都领先。正文p.8部分数字与表不符（DTD FedDAT写79.49/FLoRA72.60，表text分别78.49/62.22；Flowers也有混写），本笔记以可目视核对的表I为准并保留差异，不搬用错误叙述。

### Client公平性并非每个场景更好

**原文，p.8表III/IV。** text/$\beta$0.1 Pets：FedDLP跨clientstd3.13、lowest86.18%，FedDAT3.29/82.89%。但image/$\beta$0.01 Pets：FedDLP **std16.13 / lowest44.66%**，FedDAT **13.54 / 52.72%**，FedDLP更差；text/$\beta$0.01 Aircraft std7.64也高于FedDAT6.75。不能把betterworstcase / lower variance推广到所有表行。

这里跨clientstd不等于表I/II的三seedstd；局部均值accuracy与minimumclientaccuracy不同，不写成globalmodelaccuracy。

### 达标累计通信

**原文，p.9表V/VI；以下是到各自目标accuracy的累计MB，不能直接充当单轮compressionratio。**

| 条件 / target | FedDLP | 比较对象 | 原表比例 / 解释 |
| --- | --- | --- | --- |
| Text Flowers、$\beta$0.1、91% | 11.93MB | FedDAT15.34MB | 0.78×，约少22% |
| Text Aircraft、$\beta$0.01、50% | 34.08MB | FedDAT132.91MB | 0.26×，约少74% |
| Image Flowers、$\beta$0.1、90% | 15.30MB | FedDAT25.50、FLoRA48.45MB | 对FLoRA0.32×，约少68% |
| Image Aircraft、$\beta$0.01、44% | 7.65MB | FedDAT30.60、FLoRA48.45MB | 对FLoRA0.16×，约少84% |

“0.32×”是传输大小比例，不是减少0.32倍或压缩率32×。表VtextAircraft/$\beta$0.1：97.13MB→27.26MB，表却标0.46×，**整理者计算约0.281×**；保留原值/错位疑点，不拿该比例用于统一结论。其余表项target随dataset / beta不同，不能跨任务合并成固定节省百分比。

表V/VI单位仅MB，正文称computation/communicationcost但未给各方法训练seconds、FLOPs、energy、峰值memory或双向packet计数细则；不能用MB直接证实完整computational加速。

## 消融与局限

**原文，p.9表VII/VIII。** Separate dualadapters对combinedsetup，image/$\beta$0.01 Flowers **97.51% vs93.80%**，DTD **86.48% vs75.51%**、Aircraft **68.26% vs50.65%**；text/$\beta$0.01 DTD82.09% vs71.40%。这些是**消融表自己的值**，不替换主表II Flowers97.85 / DTD86.81 / Aircraft67.52。消融未给±/seed口径说明，不能混成一张三seed主结果。

**整理者评估：**

- 主要只有separate/combinedadapter消融；没有完整的removepruning、removeKD、globalrank/localrank或threshold对照，不能单独量化每组件贡献。
- 论文协议文字/图caption冲突：是否上传prunedlocal、inference用何分支，需要官方实现/正式全文进一步核对。
- 没有形式化convergence、DP或攻击evaluation；localadapterprivate不代表global共享adapter不会泄漏。
- 10clients、四imageclassificationdataset、单机simulation；没有缺失模态、multimodal生成、更大MLLM、asynchrony / hardware异构实测。
- Gridsearch在testset选参；最差client / 方差改善存在反例；正文数字、表V比例与主/消融表口径需谨慎。
- 三seed支持mean±std但未提供全部statisticaltests；两个分支的本地forward/KD与pruning成本不应被累计MB掩盖。

## 复现信息与阅读结论

**已取得 / 未执行。** 完整阅读10页和参考文献；Poppler核对首页、trainingschematic和主/通信表；官方arXivv1核对四authors、acceptedCCGrid和CCBY4.0；作者实验室核对正式DOI。未取得IEEEformalPDF、未执行训练；正文无可确认的本方法codeURL，本次不把FLoRA/SoRA引用仓库当FedDLP代码。

复现需要：gridsearch选中learningrate / $\alpha$、rankgateoperator与schedule、alternatingupdate顺序、KDprobability/temperature、实际servercommunicatedfields、seed/partition文件、inferencebranch以及MB计数方向。论文提供的全局流程与疑点都已记录，无空白模板。

**整理者结论：** 可以明确保存“分离local/globalLoRA、双向KD、localgatepruning”与在CLIP个性化分类的证据；同时保持publicprotocol冲突、testset选参与client公平性反例。不要把本篇扩写成已验证missing-modality或MLLMgeneration方案。

[来源与原件](source.md) · [BibTeX](citation.bib) · [仓库总览](../../../README.md) · [跨论文比较](../../../comparison.md)
