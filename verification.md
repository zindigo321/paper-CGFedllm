# 验证记录、文件清单与待补充信息

## 2026-10-13：innovation 分类实际论文整理（第 1 批，本地准备）

基于远程 main `aabb70f318e9e7c213df8452133aa2f50f448c22`，累计新增 5 篇 / 91 页，现共 14 篇 / 279 页 / 5 份公开 PDF。每篇附件按物理页码完整阅读，缺失 supplementary 明确标记未取得；未运行训练或实验复现。

原九篇记录 / 论文文档与原四份公开 PDF 保留，新分类仅使用 innovation1 / innovation2，不生成创新点说明。十个附件哈希彼此不同，也不与旧九篇身份记录重复。

XMind 保留原 12 个工作表，更新目录并新增 5 个 Abstract / Introduction / Method / Experiments / Limitation 工作表，共 18 张。ZIP、双格式结构与资源可检查；环境没有可用的 XMind 主程序，未执行桌面打开测试。

实际本地校验范围与结果见 [metadata/innovation-checks.json](metadata/innovation-checks.json)。校验值指本地工作区字节，不代表不同 Git 换行配置的字节或最终 GitHub 渲染。新增页面需你推送后检查公式及链接。未提交、推送、创建 PR 或写入远程。

下方为此前日期与范围的历史记录。

## 2026-10-13：分类目录与文献树本地更新

基于远程 main 提交 `aabb70f318e9e7c213df8452133aa2f50f448c22` 下载的本地副本准备。新增 `papers/innovation1` 与 `papers/innovation2`；分类只记录中性名称，不添加创新点说明。当前未收到新增论文附件，两个目录只有说明和填写模板；原九篇 / 188 页 / 四份公开 PDF 的元数据与原文件保持。

更新 `literature-tree.md` 和 `CG-FedLLM-Literature-Trees-v3.xmind`。XMind 保留原 12 张工作表及 1,348 个主题，新增“13 文献目录”；原节点、样式和资源保留，现代 JSON 与传统 XML 同步。新分类链接在用户推送后才可从 GitHub 访问。文件名继续沿用 v3，便于更新原文件。

本地检查工具 [tools/update_literature.py](tools/update_literature.py) 可验证论文文档、现有公开 PDF 原件校验、目录统计、Markdown 相对链接、XMind ZIP 完整性 / JSON-XML 节点一致性、SHA-256 文件清单。实际交付检查结果记录在 [metadata/innovation-checks.json](metadata/innovation-checks.json)。

本次没有重新阅读九篇全文、运行模型实验、自动生成新论文内容、提交 / 推送或创建 PR。已验证 XMind 文件结构；环境中没有可用的 XMind 主程序，未执行桌面打开测试。新增文件的 GitHub 显示待用户自行上传后检查。下方保留旧日期与旧范围的历史记录。

当前阅读范围为**九篇独立上传全文、188页**：此前七篇138页，加 ISER 期刊版33页和 FedALA-WR 期刊版17页。此次三个附件中的 PowerSGD 与第七篇原件逐字节相同，记录别名、不重复计数。核对日期2026-10-12；以下保留原日期、原范围和历史发布记录。

## 2026-10-12：三份附件整理，新增 ISER / FedALA-WR

- 通过 GitHub 插件确认当前 `main` 为 [1c580e3](https://github.com/zindigo321/paper-CGFedllm/commit/1c580e38b1acfdbcecbf7da7b30a621d1e6b93dc)，新工作副本基于该提交；未发现 AGENTS.md。保留原README开头、已有内容及提交历史，按用户自行Commit/Push的偏好提供更新包，未写远程或创建PR。
- 新增7文件：ISER的notes/source/citation/原样PDF，FedALA-WR的notes/source/citation；修改根6文件、metadata四个、AdaLoRA/SVD-LLM/FFA-LoRA/CG四篇必要阅读联系及PowerSGD+ source别名，共15修改、0删除；定稿范围41文件，checksums应覆盖除自身外的40项。
- 新两篇全文共50页均已读，含完整正文 / 参考文献，无另列附录。额外目视核对ISER物理pp.1、12、13、18、20、28、29，FedALA-WR pp.7、8、12、15的题名 / 许可、公式、算法和结果；没有把“渲染了页面”写成逐页目视全部源图。
- ISER：33页、7,130,708 bytes、SHA-256 `b103275dbb10330b6decfd99be18a3ecd711019defb11dd7669d05fb25f83fe5`；MDPI / Crossref核实 Electronics 15(17),3807、2026-08-25及CC BY 4.0。早期页面读取429，后续直接官方PDF请求成功；完整出版社PDF与附件 / 仓库副本逐字节一致。PDF未经编辑。
- FedALA-WR：17页、2,701,745 bytes、SHA-256 `f8b0ceabe7394e2011b29e5db4ef05f8b17d6988d25b50ddec8e9997e4c0a653`；Springer / Crossref核实29(9),article580、VOR 2026-07-24；附件文档生成日期2026-08-21单记。出版社页面为subscription preview，全文来自附件，未获取官方PDF作字节对照；exclusive licence不授权本次公开复制，ZIP / 补丁无该PDF。
- 重复PowerSGD附件19页、659,326 bytes，SHA与原件同为 `42d02bd274f8054293cb99634b3d78a1184719c92e4a5635341ce1f92b7de5d0`；实际二进制比较相同，仅名称不同，编号7 / 笔记 / 引用 / 许可处理不变。
- metadata原有汇总字段仍为6篇 /119页，但实际7条记录合计138页；本次按记录和可取得附件 / 公开PDF修正当前汇总为9 /188 /4份公开PDF，并新增纠错历史。前七论文记录和前七正式出版记录逐项保持；不把两个关联前作算新已读附件。
- 官方代码已核实为 `unkipark/ISER` 和 `tinku1984/FedALA_WR`，固定commit、许可和静态检查范围记在笔记 / publication-verification；没有运行作者程序或复现实验。ISER的前作CVPR LoRA-comp、FedALA的前作AAAI仅核对相关书目 / 摘要 / 方法实现，不宣称另外完整阅读。

### 本次实际检查结果

| 检查 | 已执行结果与范围 |
| --- | --- |
| 全文 / 版本 / 许可 | 两篇50页已读；两个2026期刊记录、日期与权利核对；PowerSGD重复件逐字节去重；独立9篇 /188页 |
| 数字口径 | ISER的7% /98%为BD-Rate节省幅度相对增长，额外码率平均0.98%不代表每例低于1%；FedALA精度百分点、五次std、3.77%计时差与原文报告分开；冲突表格 / 配置保留 |
| 数学 / Markdown | 23个Markdown、429个数学表达式通过本地严格KaTeX解析；65个新增（ISER34、FedALA-WR31），多字母函数用mathrm，无已知被拒绝宏 / 块级标点转义；旧七篇公式源码 / 次序保持 |
| 相对链接 / 表格 / 引用 | 本次定稿后重新检查所有相对目标、70个Markdown表格、4个JSON、9份BibTeX共18条（含两条关联前作）；实际链接计数与逐项结果见metadata检查记录 |
| PDF / 旧内容 | 四份公开PDF均与元数据匹配；原三份字节保持，ISER与附件 / 官网三方相同；旧七份citation及未改source/PDF保持，四旧notes只增相关段落，其余三旧notes逐字节保持 |
| 本地排版 / 目视 | 两篇notes本地A3预览各8页已逐页查看，15个新增块公式另生成两页并逐项查看；检查中文、表格、数学上下标 / 取整 / 范数 / 分母，未见裁切 / 乱码；最终小改动另重新渲染检查 |
| 外部入口 | 新引入的18个Markdown URL作HTTP采样：16个200、两个Springer入口超时；MDPI PDF返回真实PDF且完整下载校验成功。官方Springer元数据已由另一只读reader取得；访问结果分开，不以HTTP200断言订阅全文取得 |
| GitHub显示 | 新文件尚未用户推送，**最终GitHub渲染未执行**；本地检查不替代在线运行时。上一已发布七篇364公式的成功检查另记下方，不覆盖未发布新增内容 |
| 打包 / 校验 | 40项SHA-256全部通过；增量复制和binarypatch均在全新基准副本成功应用，文件清单一致，全部41份定稿文件逐字节一致；ZIP完整性与仅含获许可ISER新PDF检查通过。写入此结果后再次生成清单与更新包，最后变更亦纳入校验 |

### 新增待核实 / 未执行项

- ISER的跨层全局秩预算与每层rank4 / 无index信令的关系；SV/image vsSV/total分母、被剪位置的熵估计 / 实际字节流；sum vsscaledmean、floor vsround和post-loop未见退出的公开实现差异；AdaLoRA不能按其宽泛表述改写为静态算法。
- FedALA-WR的localALA与serverattention、轮内回放 / 轮末纠正 / buffer更新顺序、表2 Dir0.1的68.02 vs表3的57.53、正文跨列数字及private best-test / HPO /停止口径；公开代码detach replay、cosine+norm、lr0.01、testaccuracy patience与期刊描述不同，正式修订对应代码尚需确认。
- ISER checkpoint / evaluator / 数据未下载校验；FedALA-WR独立publisherPDF未取得；两篇没有跑训练、计时、网络部署、攻击或形式化证明。代码可访问仅是复现入口，不是复现成功。
- 新增文件的最终GitHub页面需用户推送后检查实际数学输出、宏 / parse错误和等待状态。未向外部Markdown预览API发送未发布内容。

## 2026-10-12：第七篇已推送后的真实检查

用户已推送提交 [1c580e3](https://github.com/zindigo321/paper-CGFedllm/commit/1c580e38b1acfdbcecbf7da7b30a621d1e6b93dc)。此前包的17个变更文件与发布版逐字节一致，33项SHA-256全部通过，七篇source合计138页，14条BibTeX可解析。

实际GitHub页面逐篇检查PowerSGD+57、CG66、FLASC34、FFA63、DR53、SVD32、Ada32个数学表达式，comparison27个，共**364个输出MathML，0错误、0等待**。CG步长已显示希腊η，GDP公式无多余感叹号；代表PowerSGD+公式截图亦目视核对。本记录属于已发布七篇范围，不是对本次未发布两篇的在线验证；早期服务错误 / pending记录作为当时结果保留。

## 2026-10-12：新增第七篇 PowerSGD+（增量准备，历史）

- 通过 GitHub 插件确认最新 `main` 为 [667cb40](https://github.com/zindigo321/paper-CGFedllm/commit/667cb40b1a81d7ed964cb7801dde4cfa5b65af04)，已含上一轮宏兼容修正；另在该提交上检出独立工作副本。未发现 AGENTS.md，沿用既有目录、物理页码、引用、许可边界与检查记录。未写入远程或创建 PR，按用户现有偏好交付自行更新包。
- 新增 `papers/2025-xie-powersgd-plus/` 的 notes / source / citation 共 3 个文件；修改根目录 6 个文件、metadata 4 个文件、CG / DR / FFA / SVD 四篇 notes 的阅读联系，共 14 个修改、0 个删除；定稿为 34 个仓库文件，SHA-256 清单 33 项。
- 完整解析和阅读附件 19 页，含正文、参考文献与附录 A–C；关键首页、算法、定理、结果、配置与证明疑点页面另做目视核对。全部分析基于上传 v1，不把正式会议页码当作本笔记物理页码。
- 附件版本为 `2509.11254v1`，2025-09-14；659,326 bytes，SHA-256 `42d02bd274f8054293cb99634b3d78a1184719c92e4a5635341ce1f92b7de5d0`。PDF metadata 未提供独立创建 / 修改日期。
- 正式 ICASSP 2026 的题名、作者、IEEE、pp. 921–925、published-print 2026-05-03 和 DOI `10.1109/ICASSP55912.2026.11465020` 由出版社提交的 Crossref 核实，官方会议日程 SPTM-P2.2 对照题名 / 作者。IEEE Xplore 直接页面有验证限制；正式 PDF 未取得，未完成两版全文一致性对照。官方 PowerSGD+ 代码未核实。
- arXiv 对应版本页与 PDF License 均为非独占分发许可，沿用仓库规则不公开复制 PDF；仅记录全文入口和附件身份。原始附件未改字节，不进入本次补丁、增量包或 Git 历史；公开 PDF 仍为原三份。

### 本次实际检查结果

| 检查 | 结果与范围 |
| --- | --- |
| 阅读与版本 | 附件 19 页全文 / 参考文献 / 附录已读；v1 日期、作者、许可核对；七个 source 记录合计 138 页；正式版仅核对书目，未取得全文 |
| 数字与公式 | GLUE 原表八项分数及重新计算均值分列；核对 C4 四配置 PPL 与 token 数；理论针对 MSGD，区分渐近阶与有限步依赖；未将随机梯度参数写成 DP 预算 |
| Markdown / 数学 | 19 个 Markdown、364 个表达式通过本地 KaTeX 严格解析；已知被拒绝宏和块级标点转义检查；45 个表格结构检查，无列数错误 / 孤立行；新 notes 的 57 个公式按顺序保留 |
| 结构与引用 | 全部相对链接、4 个 JSON 和 7 份 BibTeX 共 14 条记录按定稿文件检查；实际数量及逐项结果见 metadata/link-checks.json / markdown-checks.json |
| PDF / 保留内容 | 原三份公开 PDF 的页数 / 字节 / SHA-256 与 metadata 一致；其余已有 source / BibTeX 保持；两篇未修改 notes 的字节保持；四篇相关 notes 仅增加必要阅读联系（CG 关系标题同步） |
| 本地预览 | 新 notes / source、README / comparison / NOTICE / verification / UPLOAD 生成本地预览，目视检查关键理论公式、算法、数据表与目录 / 许可说明；不等同最终 GitHub 输出 |
| 在线显示 | 用于复查的 GitHub CG 已发布页面返回服务错误，重载一次仍同；未取得实际数学输出。新增 / 修改内容未推送，最终在线显示未验证，也未发送未发布内容到外部预览 API |
| 打包与校验 | 定稿后生成 33 项 SHA-256；增量文件复制与补丁应用在全新发布基准副本验证，与全部 34 个定稿文件逐字节一致 |

本次 HTTP 检查覆盖新引入的外部入口，既有 URL 的旧响应 / 日期留在历史快照；遇到验证页或响应不是 PDF 时，不以 HTTP 200 认定取得全文。新公式沿用已修正定界格式，多字母函数用 `mathrm`，不引入 `operatorname`。

### 新增待核实问题

- 表 1 的 Full precision / PowerSGD / GaLore 原表 Avg 为 86.35 / 85.73 / 85.70，按表内八项分数重算到两位小数为 86.39 / 85.76 / 85.77；保留两套值，不擅自改原表。
- PowerSGD+ 的四个 C4 配置有一项略差于 PowerSGD；Full rank PPL 差距仍存在，原文 GaLore “diverged”的有限 PPL 与判据需核实；GLUE 指标 / split / 多 seed 资料不完整。
- 收敛保证针对 MSGD，不能自动扩展为 Adam / AdamW；有限步界依赖 tau、rank 和 momentum。附录中的符号、零 / 秩亏 QR 初始化、跨节点噪声独立性与基底同步细节待核实。
- 算法 1 包含完整更新矩阵刷新；表 2 是元素量级口径，非累计网络字节或 wall-clock。C4 的 10 epochs 与固定 steps 描述、Adam / AdamW 分任务配置、GaLore 细节需核实。
- 正式 PDF、官方 PowerSGD+ 代码、完整训练日志未取得；没有运行训练、反例实验、网络测速、隐私攻击或形式化证明。新增内容的最终 GitHub 显示待用户推送后检查。

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
- [comparison.md](comparison.md)：七篇论文的问题、方法、实验条件、主要结果与局限比较。
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
| `papers/2025-xie-powersgd-plus/` | [notes.md](papers/2025-xie-powersgd-plus/notes.md) | [citation.bib](papers/2025-xie-powersgd-plus/citation.bib) | [source.md](papers/2025-xie-powersgd-plus/source.md) | 未入库，仅保留官方 v1 全文链接 |

机器可读记录：

- [metadata/papers.json](metadata/papers.json)：7 个原件的题名、版本、页数、字节数与 SHA-256。
- [metadata/publication-verification.json](metadata/publication-verification.json)：正式出版元数据与版本差异。
- [metadata/link-checks.json](metadata/link-checks.json)：相对链接与外部 HTTP 检查结果。
- [metadata/markdown-checks.json](metadata/markdown-checks.json)：数学、表格、BibTeX 与本地预览检查结果。

原始交付压缩包外层另含 `paper-CGFedllm.bundle` 与 `DELIVERY.txt`，供历史备份；它们没有入库。首次发布提交已更新 **27 个仓库文件**，包括修改原 README 和新增其他 26 个文件。后续第六篇入库扩展为 31 个文件，数学兼容修正仅更新既有文件；本次第七篇新增 3 个文件后为 34 个，公开 PDF 仍为三份。

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
