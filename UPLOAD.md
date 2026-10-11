# 上传到现有 GitHub 仓库

目标仓库：[zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，已有公开仓库，默认分支为 `main`。本次复用了原仓库并保留其初始 README 与提交历史。

## 本次远程操作状态

GitHub 插件可以读取该仓库，但 Git 数据写入接口和文件 Contents 写入接口均返回 `403 Resource not accessible by integration`。本地 Git 也没有可用于 HTTPS 推送的登录凭据。因此，**本次只创建本地提交，尚未将新增文件推送到 GitHub**；不把仓库现有页面当作新增笔记的发布页面。

压缩包包含完整工作文件夹 `paper-CGFedllm/`、Git 历史包 `paper-CGFedllm.bundle` 和 `DELIVERY.txt`。Git 历史包包含原有提交与本次本地提交，不包含 Git 配置或凭据。下面两种方式任选其一。

## 方式一：从 Git 历史包继续提交

需要本机已安装 Git，并有该仓库的推送权限。解压后，在压缩包所在目录运行：

```bash
git clone --branch main paper-CGFedllm.bundle paper-CGFedllm-git
cd paper-CGFedllm-git
git remote set-url origin https://github.com/zindigo321/paper-CGFedllm.git
git fetch origin
git rebase origin/main
git push origin main
```

若本机尚未登录，可先使用 GitHub 官方认证方式，例如安装 GitHub CLI 后执行 `gh auth login --hostname github.com`。通过登录流程认证即可，无需把访问令牌写进上述命令、仓库文档或提交。

`git fetch` / `git rebase` 将接入远程最新历史；若期间已有其他修改产生冲突，应合并相关内容后继续，避免覆盖他人文件。不要使用强制推送。

## 方式二：复制工作文件到自己的现有检出

1. 在自己的已有检出中更新远程历史；或先执行 `git clone https://github.com/zindigo321/paper-CGFedllm.git`。
2. 将压缩包内 `paper-CGFedllm/` 的文件按相对路径合并到检出中；压缩包工作文件夹不含 `.git`，不会替换 Git 历史。保留远程期间新增的文件，合并 README 改动。
3. 查看差异与文件清单后提交、推送：

```bash
git diff
git status --short
git add README.md comparison.md NOTICE.md verification.md UPLOAD.md checksums.sha256 metadata papers
git commit -m "docs: add verified Chinese notes for five LoRA and LLM papers"
git push origin main
```

## 推送后的最后检查

- 在 GitHub 打开根目录 README，点击五篇 `notes.md`、`citation.bib`、`source.md` 与比较文档，确认相对路径正确。
- 打开 DR-Encoder 与 FFA-LoRA 两份 `paper.pdf`，确认能显示；其他三篇通过 `source.md` 打开官方全文。
- 检查笔记中的数学表达式和表格；本地已做语法、渲染和链接检查，但 GitHub 在线显示尚未验证。
- 在仓库根目录执行 `sha256sum -c checksums.sha256`，确认文件未在复制 / 解压中改变。如果自行修改文档，应在复核后重新生成校验清单。
- 实际推送成功后更新 [verification.md](verification.md) 中的远程状态。不要把未核实的 DOI、代码地址或不允许再分发的 PDF 补入仓库。

[返回总览](README.md) · [再分发范围](NOTICE.md)
