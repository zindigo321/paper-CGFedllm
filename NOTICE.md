# 文档、论文与再分发范围

本仓库是中文阅读整理，不改变论文作者、出版者或代码项目的权利。未为整个仓库授予统一开源许可证；尤其**论文 PDF 不属于整理者自写文档的开源许可证范围**。作者代码、数据、预训练权重也各自遵循其来源许可。

## 已收录的原始 PDF

以下四个文件仅将上传件改名为 `paper.pdf`，内容和字节保持不变；完整作者、题名、原始文件名、版本、来源、SHA-256 与许可证据见相应 `source.md`。

| 文件 | 作者署名 | 上传版本 | 论文适用许可 |
| --- | --- | --- | --- |
| [DR-Encoder PDF](papers/2024-wu-dr-encoder/paper.pdf) | Huiwen Wu, Deyi Zhang, Xiaohan Li, Xiaogang Xu, Jiafei Wu, Zhe Liu | arXiv:2412.17053v1 | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)，本仓库非商业原样分享，保留署名 / 来源，不分发改编 PDF |
| [FFA-LoRA PDF](papers/2024-sun-ffa-lora/paper.pdf) | Youbang Sun, Zitao Li, Yaliang Li, Bolin Ding | arXiv:2403.12313v1 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，保留署名、来源与许可链接；PDF 未作修改 |
| [CG-FedLLM 扩展版 PDF](papers/2025-wu-cg-fedllm/paper.pdf) | Huiwen Wu, Xiaogang Xu, Deyi Zhang, Xiaohan Li, Jiafei Wu, Zhe Liu | arXiv:2405.13746v3 | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，本仓库非商业原样分享，保留署名 / 来源 / 许可；若分发改编材料，遵循相同方式共享要求 |
| [ISER 期刊 PDF](papers/2026-park-iser/paper.pdf) | Unki Park, Seongmoon Jeong, Sangmin Kim, Jeungsub Lee, Gyeong-Moon Park, Jong Hwan Ko | Electronics 2026, 15(17), article 3807，33页 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，首页 CC BY 与出版社提交的 Crossref VOR 许可一致，2026-10-12 核对；原样复制，保留署名 / 来源 / 许可 |

ISER 的期刊 PDF 原样分享，不单独抽取或改编其中注明 IEEE 转载许可的材料；代码 Apache-2.0、任务网络 / 数据 / 权重各自许可不混同。

这里原三篇的版本许可依据 arXiv **对应版本页**的 “view license” 链接，DR-Encoder / FFA-LoRA 核对日期为 2026-10-11，CG-FedLLM v3 为 2026-10-12（并核对 PDF 内嵌 License）。

CG-FedLLM 的正式 ECAI 出版记录 / 当前出版网页为 CC BY-NC 4.0，上传 v3 为 CC BY-NC-SA 4.0；本仓库 `paper.pdf` 依据后者。原样论文、独立阅读笔记和作者代码分别处理，未将论文许可自动扩展为全仓库统一许可证；具体来源和版本差异见 [source.md](papers/2025-wu-cg-fedllm/source.md)。

## 仅链接全文的上传版本

| 论文 | 实际阅读上传版 | 处理方式 |
| --- | --- | --- |
| [AdaLoRA](papers/2023-zhang-adalora/source.md) | arXiv:2303.10512v2 | arXiv 非独占分发许可；本仓库第三方再分发权未确认，仅保留来源与笔记 |
| [Federated LoRA with Sparse Communication](papers/2024-kuo-flasc/source.md) | arXiv:2406.05233v1 | 同上；2026 正式 VOR 的 CC BY 记录不自动覆盖上传的 2024 年版 |
| [SVD-LLM](papers/2025-wang-svd-llm/source.md) | arXiv:2403.07378v5 | arXiv 非独占分发许可；不把其他版本 / 官方代码的许可当作上传 PDF 的许可 |
| [PowerSGD+](papers/2025-xie-powersgd-plus/source.md) | arXiv:2509.11254v1，2025 年 19 页完整预印本 | arXiv 非独占分发许可，2026-10-12 核对对应版本页与 PDF metadata；仅保留全文链接、中文笔记和附件身份记录，不复制公开 PDF |
| [FedALA-WR](papers/2026-singh-fedala-wr/source.md) | Cluster Computing 2026, 29(9), article 580，17页期刊版 | PDF pp.1、17 与 Springer Rights and permissions 明确 exclusive licence；Crossref 的 TDM policy 不是公开再分发授权，仅保留阅读整理、身份校验和官方全文入口 |

[arXiv 非独占许可正文](https://arxiv.org/licenses/nonexclusive-distrib/1.0/)所列分发权授予 arXiv，而非自动授予所有第三方。上述四个 arXiv 非独占许可 PDF 和 FedALA-WR 的专有许可 PDF 未加入本次公开 Git 更新，也未创建空白或虚假的 `paper.pdf`。获得这些特定上传版本的明确再分发许可后，可原样补充。

PowerSGD+ 的 ICASSP 2026 正式出版记录与上传 v1 分开。IEEE 提交的 Crossref 记录列 IEEE policy-029 / policy-037，并非本次核实的 CC 再分发许可；未将正式记录、早期 PowerSGD 代码或其他版本的许可替代上传 PDF 的许可。该附件字节未被修改，也未放入本次增量包 / 补丁。独立阅读整理不改变作者、出版者的权利。

FedALA-WR 的作者代码根许可为 GPL-2.0，继承文件标注 GPLv2-or-later；README 的将来改 Apache 声明不等于当前许可，也不授权公开复制 Springer PDF。全文依据用户提供的附件阅读，不绕过订阅入口。本次 PowerSGD 附件仅换名、与原件逐字节相同，不新增 PDF 或改变其许可处理。

## 整理原则

- 英文完整题名与作者按版本保留，会议 / 预印本 DOI 分开。
- 笔记以实际上传全文为依据；未取得的正式版全文明确注明。
- 数值标注 PDF 物理页码、表 / 图和实验条件；整理者的推断与计算明确标识。
- 仅复述研究结论与必要公式、选取必要数据进行比较，不复制全文文字或成套图表。
- 仓库用途是阅读与研究索引，不宣称实现、复现或作者背书。

[返回总览](README.md) · [验证记录](verification.md)

## 2026-10-13 新增论文的版本与 PDF 处理

原四份公开 PDF 与原有仅链接全文的记录保留。新版本逐篇按以下证据处理；允许收录者只改名为 `paper.pdf`，不改字节、署名或内嵌许可。

| 论文 / 阅读版本 | 此版本许可或核验边界 | 本次处理 |
| --- | --- | --- |
| [AE-PSL](papers/innovation1/2026-meuwissen-ae-psl/source.md)，2607.17913v1 | arXiv non-exclusive distribution；[许可](https://arxiv.org/licenses/nonexclusive-distrib/1.0/) | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |
| [SNC](papers/innovation1/2026-almanifi-snc/source.md)，Elsevier typeset journal article, Internet of Things 40 (2026) 102113 | Elsevier All rights reserved | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |
| [ECLoRA](papers/innovation1/2025-ning-eclora/source.md)，IEEE typeset October 2025 issue, current version dated 2025-10-09 | IEEE All rights reserved; redistribution requires permission；[许可](https://www.ieee.org/publications/rights/index.html) | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |
| [Learned Parameter Compression](papers/innovation1/2024-chen-learned-parameter-compression/source.md)，IEEE Open Journal of the Communications Society Version of Record; current version 2024-06-25 | CC BY-NC-ND 4.0；[许可](https://creativecommons.org/licenses/by-nc-nd/4.0/) | [原样 paper.pdf](papers/innovation1/2024-chen-learned-parameter-compression/paper.pdf) |
| [LoRA-comp](papers/innovation1/2025-park-lora-comp/source.md)，CVF CVPR 2025 Open Access accepted version; printed pages 4430-4440; not the separately hosted supplementary material | CVF Open Access accepted version; no explicit third-party public redistribution grant verified | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |
| [MESH-FL](papers/innovation2/2026-phan-mesh-fl/source.md)，2607.06651v1 | CC BY-NC-ND 4.0；[许可](https://creativecommons.org/licenses/by-nc-nd/4.0/) | [原样 paper.pdf](papers/innovation2/2026-phan-mesh-fl/paper.pdf) |
| [FedDLP](papers/innovation2/2025-nguyen-feddlp/source.md)，2503.07552v1 | CC BY 4.0；[许可](https://creativecommons.org/licenses/by/4.0/) | [原样 paper.pdf](papers/innovation2/2025-nguyen-feddlp/paper.pdf) |
| [FedMLLM](papers/innovation2/2025-xu-fedmllm/source.md)，2411.14717v2 | arXiv non-exclusive distribution；[许可](https://arxiv.org/licenses/nonexclusive-distrib/1.0/) | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |
| [PFAdapter](papers/innovation2/2026-liu-pfadapter/source.md)，2607.12111v2 | arXiv non-exclusive distribution；[许可](https://arxiv.org/licenses/nonexclusive-distrib/1.0/) | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |
| [YOCO](papers/innovation2/2025-xu-yoco/source.md)，NeurIPS 2025 32-page conference-format camera-ready version; no arXiv version identified | Third-party redistribution permission for uploaded 32-page version not verified；[许可](https://nips.cc/FAQ/Copyright) | 仅保留官方全文入口与笔记 / 引用，不复制公开 PDF |

版本许可核对日期为 2026-10-13；证据见逐篇 source。公开下载、录用声明与作者代码许可证不替代该版本 PDF 的再分发授权。
