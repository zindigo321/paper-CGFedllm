# innovation1 / innovation2：两批自行上传

目标仓库：[zindigo321/paper-CGFedllm](https://github.com/zindigo321/paper-CGFedllm)，默认分支 `main`。本次准备了论文笔记、来源、引用、版本元数据、比较文档、文献树和 XMind；**没有替你提交或上传**。分类只使用中性名称，不写创新点说明。

## 两个更新包

1. **innovation1-upload-update.zip**：含目录准备和 innovation1 五篇、91 页，先导入和上传。完成后共十四篇 / 279 页。
2. **innovation2-upload-update.zip**：在第一包基础上增加 innovation2 五篇、80 页，再导入和上传。完成后共十九篇 / 359 页。

第一包已包含前一轮目录准备文件。两包按上面顺序使用，第二包的共享索引包含第一批论文。每包附 `START_HERE.txt`、`CHANGESET.json`，列出基准、文件路径、数量和 SHA-256；真正入库的文件在 **files/**。

原九篇保留原路径。新增每篇采用 `papers/innovation1/阅读版本年份-第一作者-短名/` 或 innovation2 的同样子目录，内含 notes.md、source.md、citation.bib，版本允许公开再分发时原样收录 paper.pdf。未收录的 PDF 通过 source.md 官方全文入口阅读，笔记和引用仍完整。模板 `_template/` 不计数。两个原始 ZIP 和未授权再分发的 PDF 留在仓库外。

## 导入一批

1. 将本批 ZIP 解压到仓库外，读 START_HERE 与 CHANGESET。
2. 打开已有本地仓库，同步远端，保留个人改动。第一批基于 `aabb70f318e9e7c213df8452133aa2f50f448c22`；若此后改过包中同名文件，先比较合并。
3. 将 **files/ 里面的内容**按相同相对路径合并到仓库根。例如 files/papers/innovation1/... 合并到现有 papers/innovation1/...。合并 papers / metadata 并保留其他内容；外层说明留在仓库外。
4. 在仓库根检查。工具需要 Python 3.9 或更新版，只有 `py` 启动器时将 `python` 换成 `py -3`。

```powershell
python tools/update_literature.py --check
```

SHA-256 指本地实际字节。工具区别文本仅 LF / CRLF 差异与其他内容差异；先看 git diff 核实。仅换行不同可运行 `python tools/update_literature.py --refresh` 再 `--check`，重建本地清单。PDF 必须与身份记录完全一致；不要用刷新掩盖未审查变化。

## GitHub Desktop：分别上传

1. 选择已有 paper-CGFedllm。无本地克隆时用 `File → Clone repository… → URL` 输入仓库地址；有克隆但未添加时用 `File → Add local repository…`。[官方克隆说明](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop)
2. Current Branch 选 main；导入前点 Fetch origin，出现 Pull origin 时拉取。[官方同步说明](https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/syncing-your-branch-in-github-desktop)
3. 导入第一包，在 Changes 核对 CHANGESET：innovation1 五篇，innovation2 此时只有 README / 模板，共享索引十四篇 / 279 页。此时只导入第一包。
4. Summary 填 `docs: add innovation1 papers and update literature tree`，点 Commit to main，再点 Push origin。[官方提交说明](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop)
5. View on GitHub 检查第一批笔记、来源、引用、全文、文献树和公式。确认已推送，再导入第二包。
6. 第二批 Changes 以 innovation2 五篇及共享索引为主，共十九篇 / 359 页。Summary 填 `docs: add innovation2 papers and update literature tree`，再 Commit to main → Push origin，最后检查网页。

**Commit 保存本地版本；Push 才上传 GitHub。** 两批之间若远端改变同名文件，先同步并比较合并，重新检查后提交。

## Git：分别上传

在已有本地仓库根打开 PowerShell。无克隆时在所选目录执行 `git clone https://github.com/zindigo321/paper-CGFedllm.git`，再进入生成目录。第一批导入前：

```powershell
git status --short
git remote -v
git switch main
git pull --ff-only origin main
```

先妥善处理个人已有改动。合并第一包后，由你执行：

```powershell
python tools/update_literature.py --check
git status --short
git add -- papers/innovation1 papers/innovation2/README.md papers/innovation2/_template README.md comparison.md NOTICE.md verification.md UPLOAD.md INNOVATION_UPLOAD.md literature-tree.md CG-FedLLM-Literature-Trees-v3.xmind checksums.sha256 tools/update_literature.py metadata/papers.json metadata/publication-verification.json metadata/innovation-categories.json metadata/new-paper-outlines.json metadata/innovation-checks.json
git diff --cached --stat
git diff --cached --check
git diff --cached
git commit -m "docs: add innovation1 papers and update literature tree"
git push origin main
```

确认第一批已上传，再合并第二包并由你执行：

```powershell
python tools/update_literature.py --check
git status --short
git add -- papers/innovation2 README.md comparison.md NOTICE.md verification.md UPLOAD.md literature-tree.md CG-FedLLM-Literature-Trees-v3.xmind checksums.sha256 metadata/papers.json metadata/publication-verification.json metadata/new-paper-outlines.json metadata/innovation-checks.json
git diff --cached --stat
git diff --cached --check
git diff --cached
git commit -m "docs: add innovation2 papers and update literature tree"
git push origin main
```

清单覆盖两包路径；你另改了其他文件时，检查后用 `git add -- 相对路径` 明确加入。不要强制推送覆盖远端。[Git 官方暂存](https://git-scm.com/docs/git-add)、[推送](https://git-scm.com/docs/git-push)

## XMind 与以后追加

仓库沿用 `CG-FedLLM-Literature-Trees-v3.xmind` 原文件名。第一批保留原十二张，加目录及五篇分析，共十八张；第二批加五篇，共二十三张。各篇沿用 Abstract → Introduction → Method → Experiments → Limitation 五分支。单独交付的最终 XMind 与第二批相同，不必再存一份到仓库。

后续按模板补全文笔记 / 来源 / 引用，人工更新 README、comparison、NOTICE、verification、metadata/papers.json；XMind 公开论文概要在 metadata/new-paper-outlines.json。随后运行：

```powershell
python tools/update_literature.py --refresh
python tools/update_literature.py --check
```

工具只根据已填写资料同步文献目录、逐篇概要工作表与校验值，不阅读论文，不代写新笔记，不生成私密研究设想，不执行 Git 提交 / 上传。本次未运行模型复现实验，最终 GitHub 显示与桌面 XMind 打开由你检查。
