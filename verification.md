# 验证记录、文件清单与待补充信息

当前阅读范围为六份实际上传全文、119 页：已有五篇 92 页（原核对日期 2026-10-11），加 CG-FedLLM v3 扩展版 27 页（本次核对日期 2026-10-12）。以下区分本次增量准备、历史发布检查、数学修订与待补充资料。

## 2026-10-12：全部 notes 的公式兼容性审核与修正

本次基于用户已推送的 [9df64e5](https://github.com/zindigo321/paper-CGFedllm/commit/9df64e5098d09c514a841a9f5547b6009cc4991e) 检查六篇笔记。通过 GitHub 插件确认 `main`，另以只读浏览器检查六个 notes 页面及 comparison 的实际公式输出；不是仅检查 HTML 中是否存在数学组件。修正文件由用户自行提交 / 推送，未写入远程。

### 当前发布版的实际显示结果

| 笔记 | 公式总数 | 宏被拒绝的公式数 | `operatorname` 出现次数 | 其他发现 |
| --- | --- | --- | --- | --- |
| AdaLoRA | 32 | 0 | 0 | 未发现本次同类问题 |
| FLASC | 34 | 4 | 5 | Top / LocalSGD / AdamUpdate |
| FFA-LoRA | 63 | 1 | 1 | DP-SGD 的 Clip |
| DR-Encoder | 53 | 0 | 0 | 现有 `mathrm` Enc / Dec 及算子复合已显示为 MathML |
| SVD-LLM | 32 | 1 | 1 | rank 约束 |
| CG-FedLLM | 66 | 4 | 10 | 另有 eta 和 GDP 感叹号两个显示问题 |

六篇合计 280 个组件，270 个有 MathML 输出，10 个明确显示 `The following macros are not allowed: operatorname`，0 个仍在等待。comparison 的 24 个公式均有 MathML 输出且无报错，共计检查 304 个组件。MathML 输出并不等于科学内容已获证明；CG 中两个静默显示问题即属例外。

### 修正内容与依据

- 四篇 notes 中的 17 处 `operatorname` 改用 `mathrm`，覆盖 10 个报错公式，保留函数名、参数、上下标和公式顺序。该写法已在本仓库 DR-Encoder 公式的实际 GitHub 页面验证。GitHub 官方 [数学格式文档](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions) 说明其数学渲染方式；[github/markup #1688](https://github.com/github/markup/issues/1688) 记录了同类宏报错，但该讨论不等于平台承诺修复时间。
- CG-FedLLM 更新公式中的 `eta` 补为 `\eta`：附件物理 p. 5 算法 1 确认为希腊字母步长，与笔记紧接其后的解释一致。
- CG-FedLLM GDP 公式删去两处 `\!` 负间距指令，保留 `\Phi\left(...)`。当前 GitHub 页面把它们显示为两个感叹号，已在 MathML 的 `mo` 节点中确认；附件物理 p. 9 式 (6) 没有感叹号。只调整间距表示，不更改概率公式。
- 原有行内反引号数学定界格式和独占行的双美元块格式保留。AdaLoRA、DR-Encoder、comparison、所有 PDF、source、citation 和文献元数据逐字节保持本次基准内容。

### 本次检查与后续要求

- 六篇笔记的公式数量和次序保持；已知被拒绝宏及块公式中易被 Markdown 消耗的标点转义清零。全部 304 个数学表达式通过本地 KaTeX 严格解析；表格、相对链接、JSON、BibTeX、PDF 身份和校验清单按定稿文件复查。详细数量与记录见 [metadata/markdown-checks.json](metadata/markdown-checks.json)。
- 六篇 notes 和 comparison 生成本地 HTML / 排版预览；目视复查四篇改动公式及 CG 的步长 / GDP 显示。该结果仅属于本地预览。
- 交付 9 个修改文件、0 个新增或删除：四篇 notes、metadata 下两份检查记录、verification、UPLOAD 和 checksums。校验清单仍为 30 项；复制增量文件与应用补丁均在全新发布基准副本上验证。
- **尚未执行：修正后文件的 GitHub 在线最终显示验证。** 本次实际浏览器结果属于当前发布基准，其错误已确认；本地修正尚待用户推送。推送后须逐篇检查实际公式输出、报错及 eta / GDP 两处，不能只统计数学组件。
- **对历史验证的补充限定：** 以下历史记录中“KaTeX 严格解析通过”“数学组件被识别”只覆盖相应本地语法 / HTML 阶段，不足以判定 GitHub 最终显示正确。历史日期和统计保留，不能用其覆盖本次浏览器发现。

## 2026-10-12：CG-FedLLM 第六篇增量准备

- 通过 GitHub 插件读取现有仓库元数据、分支和完整文件树，检出基准为 `main` 的 [e9bf347](https://github.com/zindigo321/paper-CGFedllm/commit/e9bf34708eb5597a840095f3b2c495d7078cf32a)。仓库内未发现 AGENTS.md。已有 README、比较、许可、验证、上传说明、metadata 和五篇 notes / source / citation 均用于理解整理约定。
- 按用户“让我自己更新”的要求交付增量文件。本次没有自动写入远程、创建 PR 或合并；本轮新增内容不宣称已在 GitHub 发布。所有提交与发布由用户按 UPLOAD.md 完成；原提交历史和原 README 开头保留。
- 新增 CG-FedLLM 的 notes / source / citation / 原样 PDF 共 4 个文件；修改根目录 6 个文件、metadata 4 个记录和 DR-Encoder notes 共 11 个。共 15 个变更、0 个删除；更新后应有 31 个仓库文件，校验清单含除自身外的 30 项。
- 完整解析附件 27 页并读取正文、参考文献和附录 A–E / 图页；额外目视核对首页、压缩表 / 算法 / DP 公式、主结果表、配置表和噪声 / API 表等关键页。未宣称逐页截图审查所有图页。
- 附件与新 `paper.pdf` 完全一致：8,788,962 bytes、27 页、SHA-256 `b878337481740d7343413b72cf9a54dca5ca3bf1f339ed6007526fc6cf889e4e`。arXiv v3 页与 PDF 内嵌许可均为 CC BY-NC-SA 4.0；非商业原样收录，保留署名、来源和许可。
- 正式 DOI、题名、作者、年份按出版社提交的 Crossref、IOS 出版页和第一作者主页核对；ECAI 为第 28 届，上传 p. 1 脚注为第 26 届。Crossref 日期 2025-10-21、IOS / 作者主页 2025-10-22、SAGE 页面在线日期 2026-08-25 分开记录。正式版 CC BY-NC 4.0 不替代阅读 v3 的 CC BY-NC-SA 4.0。
- 本次取得正式版书目 / 网页信息，但正式 PDF 地址返回出版信息 HTML，未取得正式 PDF、未完整审读正式 HTML。扩展版结果不写成会议版独立验证结果；官方 CG-FedLLM 实现未核实。

### 本次实际检查结果

| 检查 | 结果与范围 |
| --- | --- |
| 增量与历史 | 15 个新增 / 修改文件、0 个删除；其余四篇 notes 与所有已有 source / BibTeX / PDF 逐字节保持；DR 原文完整保留，仅新增比较与链接段落；原 HEAD 未变 |
| 源件与 PDF | 新 PDF 与附件字节完全一致；三份公开 PDF 均可解析，页数 / 字节数 / SHA-256 与 metadata 一致；六个源记录页数合计 119 |
| JSON 与 BibTeX | metadata 下四个 JSON 可解析；六份 BibTeX 共 12 条记录，键唯一、字段 / 括号检查通过 |
| 相对链接 | 153 个相对链接目标均存在，0 个错误；新文献双向链接在本地检查通过 |
| 数学与表格 | 17 个 Markdown，304 个数学表达式通过 KaTeX 严格解析，35 个表格可解析，0 个孤立表格行 / 列数错误；沿用美元符号与反引号的行内数学格式 |
| 本地渲染 | 8 个新增 / 修改 Markdown 生成本地 HTML / WeasyPrint 预览；目视核对中文、方法 / DP 公式、定量表、总览 / 比较 / 许可条目。仅作为本地预览，未声称与最终 GitHub 页面完全相同 |
| 外部入口 | 51 个 URL 的 HTTP / 内容类型采样：48 个 200、3 个 403；403 为两处 ACM 入口和 SAGE 直接请求的访问限制。IOS 正式 PDF URL 为 200 但返回 HTML，未当作成功取得 PDF |
| GitHub 渲染 | 新增内容的最终在线页面未检查；GitHub Markdown API 预览被自动审批拒绝，原因是会外传尚未发布的文档，已改用本地渲染；用户推送后目视检查 |
| 校验与打包 | 定稿后重新生成除清单自身外 30 项 SHA-256 并逐项核对；增量 ZIP 文件合并和二进制补丁均在全新基准副本上验证，与定稿 31 个文件逐字节一致 |

详细当前结果在 `metadata/link-checks.json` 与 `metadata/markdown-checks.json`；两份 JSON 的 `previous_snapshots` 保留 2026-10-11 首次检查快照，不将旧检查时间改写成本次执行。

### 新增待核实问题

- 表 1 的 1D CR 报告 3.21%，按张量形状计算为 3.125%；二维 1.56% 仅代表 encoder 输出 / 输入元素比，不含完整 TGAP、下行和协议成本。
- 基本 FAF 逐客户端解码后聚合，与第 4.5 节先聚合再解码的 DP 算子不同；第 4.4 / 附录 D.2 又描述先加噪再编码。裁剪对象、敏感度、sigma 单位、采样方式、delta、A/B 联合预算和 TGAP 发布范围未明确。
- 正文 Dolly 100-client / Dirichlet 与附录 10-client / 等量划分不同；跨数据集泛化的 MMLU / Dolly 描述、组号与相对 Cent 结论有冲突。
- 表 2 的同名 LLaMA Compress 26.6 / 26.2、正文 / 附录统计差异、API 打分和多个 seed 的区别已逐项保留。两个因子单独聚合还需结合 FFA-LoRA 的代数分析核实实际实现。
- 本次未执行训练、梯度重建攻击、DP accountant 实验或真实网络测速；新增公式的最终 GitHub 页面目视检查须由用户发布后完成。


## 2026-10-11 发布与数学修订记录（历史）

- 目标是现有公开仓库 [zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，默认分支 `main`；无需另建同名仓库。
- 用户已通过 GitHub Desktop 成功推送；[首次发布提交 e98c352](https://github.com/zindigo321/paper-CGFedllm/commit/e98c35274f380d6d5b17dd1664364c238871466c) 的父提交为原有 `718be8c5815d3486c4d5771e5fc73da80285968a`，原 README 开头与历史保留。
- 首次发布版本的 27 个文件与原交付包逐字节一致，26 项校验清单全部通过；两份原始 PDF 的 SHA-256、页数与字节数保持一致。工作区里的 LF / CRLF 提示没有改变该次远程提交的文件内容。
- 检查 GitHub 返回的 README、comparison 与五篇 notes 网页：全部 HTTP 200，21 个表格存在，渲染出的内部文件链接均指向仓库内真实路径；Markdown 全部 123 个内部文件链接也在该次远程检出中验证通过。
- 两份公开 PDF 的远程 raw 地址均返回 HTTP 200，文件头为 `%PDF-`，完整文件已经通过 Git 检出和原件校验。三个未获再分发授权的 PDF 未进入提交或历史。
- 首次页面检查发现 234 个数学表达式中只有 167 个被识别为数学组件，另 67 个行内表达式受到相邻中文标点 / Markdown 解析影响。当前修订将全部行内表达式改为 [GitHub 官方支持的反引号数学定界格式](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)，并添加定界符外的空格；逐式确认数学内容、顺序和数量不变。
- 修订后的 comparison 与五篇 notes 已通过 GitHub Markdown 渲染 API 预览：HTTP 200，234 个数学组件、19 个表格，未发现遗留的未识别数学源码；其他文档仍含其原有表格，本地总计 25 个表格。KaTeX 严格解析也再次通过。
- 上述“网页检查”指 GitHub 实际返回的 HTML、链接、表格和数学组件，加上原有本地排版目视检查；未宣称逐页完成浏览器截图目视复查。首次本地检查快照保留在 metadata 中，公式修订的实际检查结果以本节为准。
- 初始自动写入环境的 GitHub 接口曾返回 403，但用户的 GitHub Desktop 推送已经成功；后续按 [UPLOAD.md](UPLOAD.md) 更新即可。

## 2026-10-11 本地检查范围（历史）

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

## 当前文件清单

根目录文件：

- [README.md](README.md)：总览、全文索引与目录说明。
- [comparison.md](comparison.md)：六篇论文的问题、方法、实验条件、主要结果与局限比较。
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
| `papers/2025-wu-cg-fedllm/` | [notes.md](papers/2025-wu-cg-fedllm/notes.md) | [citation.bib](papers/2025-wu-cg-fedllm/citation.bib) | [source.md](papers/2025-wu-cg-fedllm/source.md) | [paper.pdf](papers/2025-wu-cg-fedllm/paper.pdf)，原样 CC BY-NC-SA 4.0 |

机器可读记录：

- [metadata/papers.json](metadata/papers.json)：6 个原件的题名、版本、页数、字节数与 SHA-256。
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
