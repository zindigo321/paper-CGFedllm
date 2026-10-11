# 验证记录、文件清单与待补充信息

核对日期：2026-10-11。阅读对象为用户实际上传的五份完整 PDF，共 92 页。以下区分本地验证结果与尚未完成的远程操作。

## GitHub 与提交状态

- 目标是现有公开仓库 [zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，默认分支 `main`；无需另建同名仓库。
- 原有提交 `718be8c5815d3486c4d5771e5fc73da80285968a` 与原 README 开头保留。本次文件形成独立本地提交，压缩包内 Git bundle 保留完整历史。
- GitHub Git 数据接口与 Contents 文件接口的写入均返回 `403 Resource not accessible by integration`。本地 Git 的 HTTPS 推送检查也因没有登录凭据而失败。
- 再次读取远程分支确认其仍指向上述原提交，**本次没有成功推送文件，也未验证 GitHub 在线 PDF / Markdown 显示**。
- 可依照 [UPLOAD.md](UPLOAD.md) 在具备推送权限的本机发布；实际推送成功后应更新本节状态。

## 已完成的本地检查

| 检查项 | 结果与范围 |
| --- | --- |
| 实际全文 | 5 个原上传件均可解析，分别为 17、17、20、17、21 页；读取正文、参考文献和附录，核对关键公式 / 数据所在原 PDF 页面 |
| PDF 完整性 | 入库 2 份 `paper.pdf` 与原件字节数、页数、SHA-256 完全一致；另 3 份未混入工作文件或 Git 历史 |
| 文献信息 | 对照上传版、arXiv 对应版本页、官方会议记录、作者项目与出版者提交的 Crossref 元数据；正式 / 预印本记录分开 |
| BibTeX | 5 份文件、10 条记录，可由 BibTeX 解析器读取；键唯一，必需字段和括号完整 |
| 相对链接 | 逐个检查 Markdown 内部文件目标，不给未入库 PDF 创建虚假链接；结果见 [链接检查记录](metadata/link-checks.json) |
| 公式与表格 | Markdown 表格可解析；234 处数学表达式通过 KaTeX 严格解析，无未闭合数学定界符；结果见 [渲染检查记录](metadata/markdown-checks.json) |
| 本地显示 | 对 README、比较文档与 5 篇笔记生成 HTML / 排版预览，检查中文、公式与表格；此检查不等同于 GitHub 在线显示验证 |
| 外部链接 | 检查 DOI、官方网页、版本 PDF、许可与官方代码等 HTTP 响应；遇到出版平台访问限制时保留官方入口和准确的限制说明 |
| 敏感信息 | 文档无访问令牌、工具内部引用或上传凭据；压缩包不包含 Git 配置、浏览器会话或环境文件 |
| 校验与历史 | [checksums.sha256](checksums.sha256) 覆盖本次全部仓库文件，清单自身除外；Git bundle 包含原历史及本次提交 |

ACM DOI / 全文入口在当前访问环境返回 HTTP 403，部分 OpenReview 入口返回 HTTP 200 但展示浏览器验证页。它们不能被写成“全文已成功打开”，也不能仅凭访问限制判为失效链接。FLASC 2026 正式出版信息依据出版者提交的 Crossref 记录交叉确认。实际逐链接响应详见 JSON。

## 文件清单

根目录文件：

- [README.md](README.md)：总览、全文索引与目录说明。
- [comparison.md](comparison.md)：五篇论文的问题、方法、实验条件、主要结果与局限比较。
- [NOTICE.md](NOTICE.md)：版本、PDF 再分发许可与文档权利边界。
- [verification.md](verification.md)：本文件。
- [UPLOAD.md](UPLOAD.md)：保留历史的上传步骤和发布后检查。
- [checksums.sha256](checksums.sha256)：文件校验清单。

论文文件：

| 目录 | 笔记 | 文献引用 | 原件与许可记录 | 公开 PDF |
| --- | --- | --- | --- | --- |
| `papers/2023-zhang-adalora/` | [notes.md](papers/2023-zhang-adalora/notes.md) | [citation.bib](papers/2023-zhang-adalora/citation.bib) | [source.md](papers/2023-zhang-adalora/source.md) | 未入库，来源见 source.md |
| `papers/2024-wu-dr-encoder/` | [notes.md](papers/2024-wu-dr-encoder/notes.md) | [citation.bib](papers/2024-wu-dr-encoder/citation.bib) | [source.md](papers/2024-wu-dr-encoder/source.md) | [paper.pdf](papers/2024-wu-dr-encoder/paper.pdf)，原样 CC BY-NC-ND 4.0 |
| `papers/2024-kuo-flasc/` | [notes.md](papers/2024-kuo-flasc/notes.md) | [citation.bib](papers/2024-kuo-flasc/citation.bib) | [source.md](papers/2024-kuo-flasc/source.md) | 未入库，来源见 source.md |
| `papers/2024-sun-ffa-lora/` | [notes.md](papers/2024-sun-ffa-lora/notes.md) | [citation.bib](papers/2024-sun-ffa-lora/citation.bib) | [source.md](papers/2024-sun-ffa-lora/source.md) | [paper.pdf](papers/2024-sun-ffa-lora/paper.pdf)，原样 CC BY 4.0 |
| `papers/2025-wang-svd-llm/` | [notes.md](papers/2025-wang-svd-llm/notes.md) | [citation.bib](papers/2025-wang-svd-llm/citation.bib) | [source.md](papers/2025-wang-svd-llm/source.md) | 未入库，来源见 source.md |

机器可读记录：

- [metadata/papers.json](metadata/papers.json)：5 个原件的题名、版本、页数、字节数与 SHA-256。
- [metadata/publication-verification.json](metadata/publication-verification.json)：正式出版元数据与版本差异。
- [metadata/link-checks.json](metadata/link-checks.json)：相对链接与外部 HTTP 检查结果。
- [metadata/markdown-checks.json](metadata/markdown-checks.json)：数学、表格、BibTeX 与本地预览检查结果。

压缩包外层另包含 `paper-CGFedllm.bundle` 与 `DELIVERY.txt`；后者记录本地提交 SHA、原父提交、工作文件数及上传指引。GitHub 实际新增文件数仍为 **0**；上表为已经完成、等待推送的本地文件清单。

## 待补充的信息

- GitHub 写入权限 / 本机认证和实际推送；推送后的 GitHub 在线 Markdown、公式、表格与 PDF 检查。
- AdaLoRA、FLASC 2024 v1、SVD-LLM v5 的特定上传版本尚无明确第三方公开再分发授权；公开仓库按要求仅保留全文来源链接与笔记。
- DR-Encoder 的 AAAI 2025 正式 PDF 与 FLASC 的 CAIS 2026 正式 PDF 本次未取得；正式元数据已核实，但笔记分析仍基于实际上传版本。
- DR-Encoder 与 FFA-LoRA 的官方代码仓库未核实；不把第三方实现认作官方代码。
- DR-Encoder 的统计量发布隐私机制、完整 delta、Qwen 轮数、梯度算子和通信字节口径需核实。
- AdaLoRA 的预算调度公式、摘要训练配置和成本表标签存在正文 / 附录不一致；SVD-LLM 的 W-only 表格数值、部分单位和更新顺序存在差异；已逐篇标明页码。
- 三篇 ICLR 论文的独立会议 DOI 在所核对官方记录未提供，保留 arXiv DOI 并明确其类型，不能编造。
- 没有运行模型训练、联邦通信、差分隐私或压缩实验，不宣称复现成功；所有数字为原文数据或明确标注的整理者计算。

[仓库总览](README.md) · [比较](comparison.md) · [版权范围](NOTICE.md)
