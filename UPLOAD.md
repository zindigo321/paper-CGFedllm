# GitHub Desktop 提交与后续更新

目标仓库：[zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，已有公开仓库，默认分支为 `main`。本次复用了原仓库并保留其初始 README 与提交历史。

## 发布状态

本仓库已由用户通过 GitHub Desktop 成功推送。首次发布提交为 [e98c352](https://github.com/zindigo321/paper-CGFedllm/commit/e98c35274f380d6d5b17dd1664364c238871466c)，保留原初始提交和 README 说明；发布检查与数学格式修订见 [verification.md](verification.md)。

最初自动环境的写入接口曾返回 `403 Resource not accessible by integration`，因此改用 GitHub Desktop 发布。该历史错误不能再被当作当前仓库“未推送”的状态。

## 2026-10-12：新增第六篇 CG-FedLLM（本次更新）

本次基于远程 `main` 的 [e9bf347](https://github.com/zindigo321/paper-CGFedllm/commit/e9bf34708eb5597a840095f3b2c495d7078cf32a) 准备增量文件。按用户要求由用户自行更新；本次没有向远程仓库写入、创建 PR 或宣称已发布。原 Git 历史保留。

新增 `papers/2025-wu-cg-fedllm/` 中的 `notes.md`、`citation.bib`、`source.md`、`paper.pdf` 共 4 个文件；修改根目录 README / comparison / NOTICE / verification / UPLOAD / checksums 共 6 个文件、metadata 下 4 个记录、DR-Encoder 的 notes，共修改 11 个文件。合计 **15 个新增 / 修改文件**，没有删除文件；其余四篇笔记和已有两份 PDF 保持原样。

### 在 GitHub Desktop 中自行更新

1. 下载并解压本次 `CGFedLLM-update.zip` 到仓库外。先阅读包内 `START_HERE.txt`；真正入库的 15 个文件在 **files/** 内。
2. 在 GitHub Desktop 打开已有的 `paper-CGFedllm`，点击 **Fetch origin**，如有更新先同步。确认本地已有修改已妥善保留；若远程在上述基准之后又改过本次涉及文件，应先比较再合并。
3. 选择 **Repository → Show in Explorer / Finder**。将解压后 **files/ 内的内容**按相同相对路径合并到仓库根目录；不要把 `files` 文件夹本身套进仓库。已有 `papers` / `metadata` 目录应合并，保留其他文件；不要删除并替换整个目录。
4. 包内 `START_HERE.txt`、`CHANGESET.json` 和 `changes.patch` 留在仓库外；不复制 `.git`，不重新初始化仓库。补丁仅供会使用 Git 的用户选择，与复制文件二选一。
5. 回到 **Changes** 检查 15 个变更：新增 4 个、修改 11 个、删除 0 个。确认 CG-FedLLM PDF 及版本、许可与元数据齐全。提交前可在仓库根目录执行 `sha256sum -c checksums.sha256`（Git Bash 或 Linux / macOS）检查复制完整性。
6. Summary 填入下方说明，点击 **Commit … files to main**，再点击 **Push origin**。若自行选择了工作分支，按该分支提交 / 推送并自行处理 PR；Commit 与 Push 是两个不同步骤。
7. 用 **Repository → View on GitHub** 打开 README，检查六篇笔记、CG-FedLLM PDF、引用和比较表，并目视检查新增公式。发布后再将实际提交链接、日期和页面检查结果补入 verification；不要提前将本地检查写成远程发布验证。

```text
docs: add CG-FedLLM extended-version literature notes
```

### 本次发布后重点检查

- 当前范围为六篇、119 页；新增目录年份为 2025，读取的是 arXiv v3 扩展版。
- 公开 PDF 共三份；新增 PDF 保持上传字节，许可为 CC BY-NC-SA 4.0，会议记录许可单独列出。
- 新笔记和 DR-Encoder 双向链接、各 comparison 表中的第六篇条目能打开 / 显示。
- JSON / BibTeX、30 项校验清单与实际检查记录齐全。公式格式沿用现有 GitHub 定界方式；本地与在线检查的具体范围见 verification。

## 2026-10-11 数学格式修订步骤（历史）

1. 打开已有的 `paper-CGFedllm` 仓库，确认当前分支为 `main`，点击 **Fetch origin**；如果远程存在新提交，先按界面提示同步。
2. 将更新包内文件按相同相对路径合并到仓库根目录。根目录直接包含 README、comparison、papers 和 metadata；不要在现有仓库中再套一层同名工作文件夹。原交付的 `DELIVERY.txt` 和 `.bundle` 历史包保存在仓库外。
3. 返回 **Changes**，查看并勾选本次需要提交的文件。数学格式修订应只涉及五篇 notes、comparison、verification、UPLOAD 与 checksums，共 9 个文件。
4. 在 **Summary** 填入下面的提交说明；**Description** 可留空。

```text
docs: fix GitHub math rendering and record publication
```

5. 点击 **Commit … files to main** 保存本地提交，然后点击顶部 **Push origin** 发布更新。Commit 与 Push 是两个步骤。
6. 点击 **Repository → View on GitHub**，打开公开页面检查文件与链接。官方操作说明见 [GitHub Desktop 提交文档](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop)。

## 首次发布与数学修订的检查范围（历史）

- 在 GitHub 打开根目录 README，点击五篇 `notes.md`、`citation.bib`、`source.md` 与比较文档，确认相对路径正确。
- 打开 DR-Encoder 与 FFA-LoRA 两份 `paper.pdf`，确认能显示；其他三篇通过 `source.md` 打开官方全文。
- 检查笔记中的数学表达式和表格。当前格式修订已经通过 GitHub Markdown 渲染 API 预览；实际页面 HTML 和浏览器目视复查的范围见 verification。
- 在仓库根目录执行 `sha256sum -c checksums.sha256`，确认文件未在复制 / 解压中改变。如果自行修改文档，应在复核后重新生成校验清单。
- 后续更新应维护 verification 与校验清单。不要把未核实的 DOI、代码地址或不允许再分发的 PDF 补入仓库，不将访问令牌写入文档、提交或 URL。

[返回总览](README.md) · [再分发范围](NOTICE.md)
