# GitHub Desktop 提交与后续更新

目标仓库：[zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，已有公开仓库，默认分支为 `main`。本次复用了原仓库并保留其初始 README 与提交历史。

## 发布状态

本仓库已由用户通过 GitHub Desktop 成功推送。首次发布提交为 [e98c352](https://github.com/zindigo321/paper-CGFedllm/commit/e98c35274f380d6d5b17dd1664364c238871466c)，保留原初始提交和 README 说明；发布检查与数学格式修订见 [verification.md](verification.md)。

最初自动环境的写入接口曾返回 `403 Resource not accessible by integration`，因此改用 GitHub Desktop 发布。该历史错误不能再被当作当前仓库“未推送”的状态。

## 使用 GitHub Desktop 更新

1. 打开已有的 `paper-CGFedllm` 仓库，确认当前分支为 `main`，点击 **Fetch origin**；如果远程存在新提交，先按界面提示同步。
2. 将更新包内文件按相同相对路径合并到仓库根目录。根目录直接包含 README、comparison、papers 和 metadata；不要在现有仓库中再套一层同名工作文件夹。原交付的 `DELIVERY.txt` 和 `.bundle` 历史包保存在仓库外。
3. 返回 **Changes**，查看并勾选本次需要提交的文件。数学格式修订应只涉及五篇 notes、comparison、verification、UPLOAD 与 checksums，共 9 个文件。
4. 在 **Summary** 填入下面的提交说明；**Description** 可留空。

```text
docs: fix GitHub math rendering and record publication
```

5. 点击 **Commit … files to main** 保存本地提交，然后点击顶部 **Push origin** 发布更新。Commit 与 Push 是两个步骤。
6. 点击 **Repository → View on GitHub**，打开公开页面检查文件与链接。官方操作说明见 [GitHub Desktop 提交文档](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop)。

## 检查与保留范围

- 在 GitHub 打开根目录 README，点击五篇 `notes.md`、`citation.bib`、`source.md` 与比较文档，确认相对路径正确。
- 打开 DR-Encoder 与 FFA-LoRA 两份 `paper.pdf`，确认能显示；其他三篇通过 `source.md` 打开官方全文。
- 检查笔记中的数学表达式和表格。当前格式修订已经通过 GitHub Markdown 渲染 API 预览；实际页面 HTML 和浏览器目视复查的范围见 verification。
- 在仓库根目录执行 `sha256sum -c checksums.sha256`，确认文件未在复制 / 解压中改变。如果自行修改文档，应在复核后重新生成校验清单。
- 后续更新应维护 verification 与校验清单。不要把未核实的 DOI、代码地址或不允许再分发的 PDF 补入仓库，不将访问令牌写入文档、提交或 URL。

[返回总览](README.md) · [再分发范围](NOTICE.md)
