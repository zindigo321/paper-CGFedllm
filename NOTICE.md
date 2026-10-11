# 文档、论文与再分发范围

本仓库是中文阅读整理，不改变论文作者、出版者或代码项目的权利。未为整个仓库授予统一开源许可证；尤其**论文 PDF 不属于整理者自写文档的开源许可证范围**。作者代码、数据、预训练权重也各自遵循其来源许可。

## 已收录的原始 PDF

以下两个文件仅将上传件改名为 `paper.pdf`，内容和字节保持不变；完整作者、题名、原始文件名、版本、来源、SHA-256 与许可证据见相应 `source.md`。

| 文件 | 作者署名 | 上传版本 | 论文适用许可 |
| --- | --- | --- | --- |
| [DR-Encoder PDF](papers/2024-wu-dr-encoder/paper.pdf) | Huiwen Wu, Deyi Zhang, Xiaohan Li, Xiaogang Xu, Jiafei Wu, Zhe Liu | arXiv:2412.17053v1 | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)，本仓库非商业原样分享，保留署名 / 来源，不分发改编 PDF |
| [FFA-LoRA PDF](papers/2024-sun-ffa-lora/paper.pdf) | Youbang Sun, Zitao Li, Yaliang Li, Bolin Ding | arXiv:2403.12313v1 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，保留署名、来源与许可链接；PDF 未作修改 |

这里的版本许可依据 arXiv **对应版本页**的 “view license” 链接，核对日期为 2026-10-11。

## 仅链接全文的上传版本

| 论文 | 实际阅读上传版 | 处理方式 |
| --- | --- | --- |
| [AdaLoRA](papers/2023-zhang-adalora/source.md) | arXiv:2303.10512v2 | arXiv 非独占分发许可；本仓库第三方再分发权未确认，仅保留来源与笔记 |
| [Federated LoRA with Sparse Communication](papers/2024-kuo-flasc/source.md) | arXiv:2406.05233v1 | 同上；2026 正式 VOR 的 CC BY 记录不自动覆盖上传的 2024 年版 |
| [SVD-LLM](papers/2025-wang-svd-llm/source.md) | arXiv:2403.07378v5 | arXiv 非独占分发许可；不把其他版本 / 官方代码的许可当作上传 PDF 的许可 |

[arXiv 非独占许可正文](https://arxiv.org/licenses/nonexclusive-distrib/1.0/)所列分发权授予 arXiv，而非自动授予所有第三方。上述文件未提交到 Git 历史，也未创建空白或虚假的 `paper.pdf`。获得这些特定上传版本的明确再分发许可后，可原样补充。

## 整理原则

- 英文完整题名与作者按版本保留，会议 / 预印本 DOI 分开。
- 笔记以实际上传全文为依据；未取得的正式版全文明确注明。
- 数值标注 PDF 物理页码、表 / 图和实验条件；整理者的推断与计算明确标识。
- 仅复述研究结论与必要公式、选取必要数据进行比较，不复制全文文字或成套图表。
- 仓库用途是阅读与研究索引，不宣称实现、复现或作者背书。

[返回总览](README.md) · [验证记录](verification.md)
