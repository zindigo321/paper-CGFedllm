# paper-CGFedllm
some papers about CGFedllm

中文文献知识库，整理与 **LoRA、federated learning、differential privacy、LLM compression、distributed optimization、learned image compression 和 personalized FL** 有关的九篇独立上传论文。保留上面原仓库说明及已有提交历史。逐篇笔记记录方法、核心公式、实验条件、定量结果、消融、局限与复现信息，并区分原文、整理者归纳和待核实内容。

## 阅读范围与版本

九篇独立上传全文共 **188 页**（此前七篇 138 页，加 ISER 33 页、FedALA-WR 17 页），已读完整正文、参考文献与各自存在的附录；本次三个附件中的 PowerSGD 是既有第七篇的字节相同副本，记录文件名别名，不重复计数；没有将摘要页、论文列表或出版网页当作全文。页码统一使用**实际上传 PDF 的物理页码**。本仓库未实际执行论文模型训练或复现实验。

上传内容没有单光子 LiDAR 论文，相关探测器、距离、速度、SNR/SBR、光子数、采集时间、重建帧率、分辨率与定位误差均标为“不适用”；不会将图像输入尺寸或 LLM 吞吐混作 LiDAR 参数。

目录年份固定采用上传 PDF 版本所示年份，以保持路径稳定；正式发表年份单独列出。DR-Encoder 已正式发表于 AAAI 2025，但读取的是 2024 年预印本；FLASC 已有 CAIS 2026 正式记录，但读取的是 2024 年 v1；SVD-LLM 读取的是 ICLR 2025 / arXiv v5，不混用早期版本或 SVD-LLM V2。CG-FedLLM 读取的是 2025 年 arXiv v3 扩展版，目录按 2025 年，不用 2024 年初版或会议 DOI 替代扩展版；当前出版网页的 2026 年在线日期另记。

PowerSGD+ 读取的是 2025 年 arXiv:2509.11254v1，19 页；已核实 ICASSP 2026、pp. 921–925 的正式书目，但未取得正式 5 页 PDF，不能将预印本全文分析直接当作两版内容一致性验证。

ISER 和 FedALA-WR 均读取 2026 年完整期刊版，目录年为2026；两者无已核实的独立 arXiv 阅读版本。ISER 明确扩展 CVPR 2025 LoRA-comp，但新增实验不归属于前作；FedALA-WR 的 PDF 生成于8月21日，正式在线出版日期为7月24日。两篇的作者代码可访问，静态审计发现论文 / 代码差异，未运行复现。

## 论文索引

作者列按**上传版本**顺序列全；会议 DOI 与 arXiv DOI 明确分开。AdaLoRA 的会议引用作者列表与上传 v2 不同，详情见笔记。已有五篇的元数据核对日期为 2026-10-11；CG-FedLLM、PowerSGD+、ISER 与 FedALA-WR 的版本、许可和出版元数据核对日期为 2026-10-12。

| 上传版完整题名 | 上传版作者 | 年份：正式 / 阅读版 | 发表渠道 | 研究方向 | DOI | PDF / 全文 | 中文笔记 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning | Qingru Zhang, Minshuo Chen, Alexander Bukharin, Nikos Karampatziakis, Pengcheng He, Yu Cheng, Weizhu Chen, Tuo Zhao | 2023 / 2023 | ICLR 2023；上传 arXiv v2 | 自适应秩、PEFT 预算 | 会议未提供；[arXiv: 10.48550/arXiv.2303.10512](https://doi.org/10.48550/arXiv.2303.10512) | [来源链接，PDF 未入库](papers/2023-zhang-adalora/source.md) | [notes.md](papers/2023-zhang-adalora/notes.md) |
| DR-Encoder: Encode Low-rank Gradients with Random Prior for Large Language Models Differentially Privately | Huiwen Wu, Deyi Zhang, Xiaohan Li, Xiaogang Xu, Jiafei Wu, Zhe Liu | 2025 / 2024 | AAAI 2025，39(26):27706–27714；上传预印本 v1 | 随机先验、梯度压缩、DP | [AAAI: 10.1609/aaai.v39i26.34985](https://doi.org/10.1609/aaai.v39i26.34985)；[arXiv DOI](https://doi.org/10.48550/arXiv.2412.17053) | [paper.pdf](papers/2024-wu-dr-encoder/paper.pdf) | [notes.md](papers/2024-wu-dr-encoder/notes.md) |
| Federated LoRA with Sparse Communication | Kevin Kuo, Arian Raje, Kousik Rajesh, Virginia Smith | 2026 / 2024 | CAIS 2026 正式题名为 FLASC: Federated LoRA with Sparse Communication；上传 v1 为预印本 | 稀疏通信、cross-device FL | [CAIS: 10.1145/3786335.3813151](https://doi.org/10.1145/3786335.3813151)；[arXiv DOI](https://doi.org/10.48550/arXiv.2406.05233) | [来源链接，PDF 未入库](papers/2024-kuo-flasc/source.md) | [notes.md](papers/2024-kuo-flasc/notes.md) |
| Improving LoRA in Privacy-preserving Federated Learning | Youbang Sun, Zitao Li, Yaliang Li, Bolin Ding | 2024 / 2024 | ICLR 2024；上传 arXiv v1 为会议论文版本 | FFA-LoRA、聚合一致性、客户端 DP-SGD | 会议未提供；[arXiv: 10.48550/arXiv.2403.12313](https://doi.org/10.48550/arXiv.2403.12313) | [paper.pdf](papers/2024-sun-ffa-lora/paper.pdf) | [notes.md](papers/2024-sun-ffa-lora/notes.md) |
| SVD-LLM: Truncation-aware Singular Value Decomposition for Large Language Model Compression | Xin Wang, Yu Zheng, Zhongwei Wan, Mi Zhang | 2025 / 2025 | ICLR 2025；上传 arXiv v5，初版 2024 | 主干低秩压缩、白化、顺序恢复 | 会议未提供；[arXiv: 10.48550/arXiv.2403.07378](https://doi.org/10.48550/arXiv.2403.07378) | [来源链接，PDF 未入库](papers/2025-wang-svd-llm/source.md) | [notes.md](papers/2025-wang-svd-llm/notes.md) |
| CG-FedLLM: How to Compress Gradients in Federated Fune-tuning for Large Language Models（Extended Version，保留原题拼写） | Huiwen Wu, Xiaogang Xu, Deyi Zhang, Xiaohan Li, Jiafei Wu, Zhe Liu | 2025 / 2025 | ECAI 2025；上传 arXiv v3 扩展版，正式题名为 Fine-Tuning；当前网页在线日期 2026 年另记 | 学习梯度压缩、TGAP / FAF、client-level DP 分析 | [ECAI: 10.3233/FAIA251320](https://doi.org/10.3233/FAIA251320)；[arXiv DOI](https://doi.org/10.48550/arXiv.2405.13746) | [paper.pdf](papers/2025-wu-cg-fedllm/paper.pdf) | [notes.md](papers/2025-wu-cg-fedllm/notes.md) |
| From PowerSGD to PowerSGD+: Low-Rank Gradient Compression for Distributed Optimization with Convergence Guarantees | Shengping Xie, Chuyan Chen, Kun Yuan | 2026 / 2025 | ICASSP 2026，IEEE，pp. 921–925；上传 arXiv v1 | 低秩梯度通信、共同基底、EF、周期性 SVD、MSGD 收敛 | [ICASSP: 10.1109/ICASSP55912.2026.11465020](https://doi.org/10.1109/ICASSP55912.2026.11465020)；[arXiv DOI](https://doi.org/10.48550/arXiv.2509.11254) | [来源链接，PDF 未入库](papers/2025-xie-powersgd-plus/source.md) | [notes.md](papers/2025-xie-powersgd-plus/notes.md) |
| ISER: Instance-Specific Early Stopping with Dynamic Low-Rank Adaptation for Learned Image Compression | Unki Park, Seongmoon Jeong, Sangmin Kim, Jeungsub Lee, Gyeong-Moon Park, Jong Hwan Ko | 2026 / 2026 | Electronics 15(17), article 3807；LoRA-comp 的期刊扩展 | 每图 TTFT、SVD-LoRA、ISRA / ISES / MSTS、图像码流 | [期刊: 10.3390/electronics15173807](https://doi.org/10.3390/electronics15173807) | [paper.pdf](papers/2026-park-iser/paper.pdf) | [notes.md](papers/2026-park-iser/notes.md) |
| FedALA-WR: personalized federated learning with adaptive local aggregation and weighted replay | Tinku Singh, Nguyen Khoa, Bhawnesh Kumar, Taehong Kim | 2026 / 2026 | Cluster Computing 29(9), article 580 | pFL、熵选样回放、mixture loss、聚合 / 停止、CNN | [期刊: 10.1007/s10586-026-06366-5](https://doi.org/10.1007/s10586-026-06366-5) | [来源链接，PDF 未入库](papers/2026-singh-fedala-wr/source.md) | [notes.md](papers/2026-singh-fedala-wr/notes.md) |

## 目录与引用

| 路径 | 用途 |
| --- | --- |
| `papers/年份-第一作者-简短英文标题/notes.md` | 完整中文阅读笔记，保留英文原题与术语 |
| 同目录 `citation.bib` | 存在独立预印本 / 正式版时分列；两篇已读期刊 VOR 引用本身，关联前作条目明确注明仅作关系引用，不增加已读数量 |
| 同目录 `source.md` | 原文件名、版本、全文来源、原始 SHA-256、许可证据与 PDF 入库决定 |
| 同目录 `paper.pdf` | 仅存在于允许再分发的 DR-Encoder、FFA-LoRA、CG-FedLLM 与 ISER 目录；上传件字节不变 |
| [comparison.md](comparison.md) | 问题 / 方法 / 实验条件 / 结果 / 局限性比较，不做跨条件直接排名 |
| [NOTICE.md](NOTICE.md) | 文档与论文的许可边界及逐篇再分发说明 |
| [metadata/papers.json](metadata/papers.json) | 机器可读的上传件清单、页数、字节数、版本和校验值 |
| [metadata/publication-verification.json](metadata/publication-verification.json) | 正式出版元数据来源及版本差异记录 |
| [verification.md](verification.md) | 文件清单、链接和渲染验证结果、未完成 / 待补充信息 |
| [UPLOAD.md](UPLOAD.md) | GitHub Desktop 增量更新步骤、本次文件范围及推送后检查 |
| [checksums.sha256](checksums.sha256) | 本次提交文件的 SHA-256 清单，清单自身除外 |

建议先读 [比较文档](comparison.md)，再进入各篇方法 / 实验笔记。需要引用时使用对应 `citation.bib` 中的明确版本：2024 FLASC 结果应引用其 arXiv v1；AAAI 2025 DOI 用于 DR-Encoder 正式出版，不能用它假装已读其正式全文。CG-FedLLM 的扩展版结果引用其 arXiv v3，会议书目单独引用 ECAI 2025 记录。

PowerSGD+ 的算法、证明、表格与配置按实际阅读 v1 引用，正式书目另用 ICASSP 2026 条目。它压缩同步训练梯度，未提供 DP 机制；本篇的 delta、sigma 和 epsilon 不能按同名符号解释为隐私预算。

## 准确性与公开 PDF

DR-Encoder 原始上传件按 **CC BY-NC-ND 4.0** 在非商业文献整理用途下原样分享；FFA-LoRA 原始上传件按 **CC BY 4.0** 原样分享；CG-FedLLM v3 原始上传件按 **CC BY-NC-SA 4.0** 在本非商业文献整理用途下原样分享，保留署名、来源与许可。ISER 的期刊版按 **CC BY 4.0** 原样分享。AdaLoRA、FLASC、SVD-LLM、PowerSGD+ 四个上传版本仅有 arXiv 非独占分发许可，本仓库第三方再分发权未确认，故保留官方全文链接而不上传 PDF；FedALA-WR 为 Springer 独占出版许可，未确认公开再分发权，也只链接全文。详情见 [NOTICE.md](NOTICE.md)。没有把论文 PDF 纳入整理文档的统一开源许可证。

官方元数据可核实而全文未取得的版本会明确标明；论文中的冲突配置、单位疑点和缺失复现资料均记录在笔记及 [验证记录](verification.md)。数字以对应页码 / 表格为准，不能把不同数据集、模型、隐私粒度、预算、硬件或离线处理结果直接排成优劣顺序。
