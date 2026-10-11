# 验证记录、文件清单与待补充信息

核对日期：2026-10-11。阅读对象为用户实际上传的五份完整 PDF，共 92 页。以下区分首次发布检查、数学格式修订、本地验证与尚待补充的资料。

## GitHub 与提交状态

- 目标是现有公开仓库 [zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，默认分支 `main`；无需另建同名仓库。
- 用户已通过 GitHub Desktop 成功推送；[首次发布提交 e98c352](https://github.com/zindigo321/paper-CGFedllm/commit/e98c35274f380d6d5b17dd1664364c238871466c) 的父提交为原有 `718be8c5815d3486c4d5771e5fc73da80285968a`，原 README 开头与历史保留。
- 首次发布版本的 27 个文件与原交付包逐字节一致，26 项校验清单全部通过；两份原始 PDF 的 SHA-256、页数与字节数保持一致。工作区里的 LF / CRLF 提示没有改变该次远程提交的文件内容。
- 检查 GitHub 返回的 README、comparison 与五篇 notes 网页：全部 HTTP 200，21 个表格存在，渲染出的内部文件链接均指向仓库内真实路径；Markdown 全部 123 个内部文件链接也在该次远程检出中验证通过。
- 两份公开 PDF 的远程 raw 地址均返回 HTTP 200，文件头为 `%PDF-`，完整文件已经通过 Git 检出和原件校验。三个未获再分发授权的 PDF 未进入提交或历史。
- 首次页面检查发现 234 个数学表达式中只有 167 个被识别为数学组件，另 67 个行内表达式受到相邻中文标点 / Markdown 解析影响。当前修订将全部行内表达式改为 [GitHub 官方支持的反引号数学定界格式](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)，并添加定界符外的空格；逐式确认数学内容、顺序和数量不变。
- 修订后的 comparison 与五篇 notes 已通过 GitHub Markdown 渲染 API 预览：HTTP 200，234 个数学组件、19 个表格，未发现遗留的未识别数学源码；其他文档仍含其原有表格，本地总计 25 个表格。KaTeX 严格解析也再次通过。
- 上述“网页检查”指 GitHub 实际返回的 HTML、链接、表格和数学组件，加上原有本地排版目视检查；未宣称逐页完成浏览器截图目视复查。首次本地检查快照保留在 metadata 中，公式修订的实际检查结果以本节为准。
- 初始自动写入环境的 GitHub 接口曾返回 403，但用户的 GitHub Desktop 推送已经成功；后续按 [UPLOAD.md](UPLOAD.md) 更新即可。

## 已完成的本地检查

| 检查项 | 结果与范围 |
| --- | --- |
| 实际全文 | 5 个原上传件均可解析，分别为 17、17、20、17、21 页；读取正文、参考文献和附录，核对关键公式 / 数据所在原 PDF 页面 |
| PDF 完整性 | 入库 2 份 `paper.pdf` 与原件字节数、页数、SHA-256 完全一致；另 3 份未混入工作文件或 Git 历史 |
| 文献信息 | 对照上传版、arXiv 对应版本页、官方会议记录、作者项目与出版者提交的 Crossref 元数据；正式 / 预印本记录分开 |
| BibTeX | 5 份文件、10 条记录，可由 BibTeX 解析器读取；键唯一，必需字段和括号完整 |
| 相对链接 | 首次远程发布版 123 个内部文件链接通过；修订后继续检查所有目标，不给未入库 PDF 创建虚假链接；首次快照见 [链接检查记录](metadata/link-checks.json) |
| 公式与表格 | 234 处数学表达式的内容保持不变；KaTeX 严格解析及修订后的 GitHub 渲染 API 预览通过，无未闭合定界符；本地 25 个表格可解析，首次本地快照见 [渲染检查记录](metadata/markdown-checks.json) |
| 显示范围 | 本地检查中文、关键公式与主要结果表格；另检查 GitHub 首次网页与修订预览的 HTML。浏览器逐页截图目视复查未实施 |
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

原始交付压缩包外层另含 `paper-CGFedllm.bundle` 与 `DELIVERY.txt`，供历史备份；它们没有入库。首次发布提交已更新 **27 个仓库文件**，包括修改原 README 和新增其他 26 个文件。当前数学格式与状态修订仅更新既有文件，目录和 PDF 收录范围保持不变。

## 待补充的信息

- 浏览器逐页截图目视复查；本记录对在线检查的描述仅覆盖已经实际检查的网页 HTML、数学组件、链接和 PDF 可访问性。
- AdaLoRA、FLASC 2024 v1、SVD-LLM v5 的特定上传版本尚无明确第三方公开再分发授权；公开仓库按要求仅保留全文来源链接与笔记。
- DR-Encoder 的 AAAI 2025 正式 PDF 与 FLASC 的 CAIS 2026 正式 PDF 本次未取得；正式元数据已核实，但笔记分析仍基于实际上传版本。
- DR-Encoder 与 FFA-LoRA 的官方代码仓库未核实；不把第三方实现认作官方代码。
- DR-Encoder 的统计量发布隐私机制、完整 delta、Qwen 轮数、梯度算子和通信字节口径需核实。
- AdaLoRA 的预算调度公式、摘要训练配置和成本表标签存在正文 / 附录不一致；SVD-LLM 的 W-only 表格数值、部分单位和更新顺序存在差异；已逐篇标明页码。
- 三篇 ICLR 论文的独立会议 DOI 在所核对官方记录未提供，保留 arXiv DOI 并明确其类型，不能编造。
- 没有运行模型训练、联邦通信、差分隐私或压缩实验，不宣称复现成功；所有数字为原文数据或明确标注的整理者计算。

[仓库总览](README.md) · [比较](comparison.md) · [版权范围](NOTICE.md)
