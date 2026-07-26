# Day 02：整理现有仓库，建立有意义的提交习惯

## 今天的目标

今天不创建新的嵌套仓库，也不提前重构成本计算代码。

`D:\CodexProjects\FDE学习项目` 已经是一个 Git 仓库，当前主分支是 `main`。今天要把它加入 GitHub Desktop，学会查看差异，并完成两次目的清楚的提交。

完成后，你应该能够：

- 分清“文件已保存”“文件已提交”“文件已上传”；
- 在 GitHub Desktop 中查看每个文件的 diff；
- 判断缓存、密钥、临时文件是否应该进入仓库；
- 把不同目的的修改拆成不同 commit；
- 用一句清楚的提交信息说明“这次完成了什么”。

预计用时：3 小时。

## 今天的核心概念

```text
保存 Save
只把文件写到电脑磁盘

提交 Commit
把一组有明确目的的修改存入 Git 历史

上传 Push
把本地提交发送到 GitHub 远程仓库
```

这三个动作不能混为一谈：

- 保存了，不代表已经提交；
- 提交了，不代表已经上传；
- 上传了，也不代表改动已经通过 PR 合并。

FDE 对应关系：

- `issue`：这次要解决什么；
- `diff`：实际改了什么；
- `commit`：一次可追溯的工作存档；
- `PR`：把一个或多个提交作为交付单提交审核。

## 今天使用的文件

```text
day-02/
├─ DAY02-学习计划.md
├─ COMMIT_PLAN.md
└─ day02_repo_audit.py
```

## 第一阶段：把现有项目加入 GitHub Desktop（25 分钟）

注意：不要点击“Create a New Repository”，因为当前项目已经有 `.git`。

操作步骤：

1. 打开 GitHub Desktop；
2. 点击 `File`；
3. 点击 `Add local repository...`；
4. 在 Local path 中选择：

   ```text
   D:\CodexProjects\FDE学习项目
   ```

5. 点击 `Add repository`；
6. 确认 Current repository 显示 FDE 学习项目；
7. 确认 Current branch 显示 `main`。

如果 GitHub Desktop 提示“此目录不是 Git 仓库”，先停止，不要新建仓库。

## 第二阶段：理解当前状态（25 分钟）

在 GitHub Desktop 的 `Changes` 页面查看：

- 左侧文件名：哪些文件发生了变化；
- 右侧红色行：删除的内容；
- 右侧绿色行：新增的内容；
- 左下角 Summary：本次提交的标题；
- Description：可选的详细说明。

目前可能看到：

- Day 1 项目契约的修改；
- Day 1 Issue 验收标准的修改；
- Day 2 新增的学习计划和仓库审计代码；
- README 的换行变化。

先观察，不要立即点击 Commit。

## 第三阶段：运行仓库审计工具（35 分钟）

在 VS Code 中打开：

```text
day02_repo_audit.py
```

运行：

```powershell
python .\exercises\fde-16week\week-01\day-02\day02_repo_audit.py
```

程序会检查：

- 当前目录是不是 Git 仓库；
- 当前所在分支；
- 是否存在尚未提交的改动；
- `.gitignore` 是否存在；
- 是否发现 `.env`、密钥或疑似敏感文件；
- 是否存在缓存、临时文件和名称带 `copy` 的疑似重复文件；
- 是否存在内容完全相同的重复文件。

这个工具只报告，不会删除或修改任何文件。

记录三个结果：

1. 当前分支是什么；
2. 有多少条未提交改动；
3. 审计报告中最值得处理的一条提醒是什么。

## 第四阶段：检查 `.gitignore`（25 分钟）

打开项目根目录的 `.gitignore`，确认至少包含：

```gitignore
.venv/
.env
*.key
__pycache__/
*.py[cod]
```

理解每一项：

- `.venv/`：本机 Python 环境，可重新安装，不应上传；
- `.env`：经常保存 API 密钥；
- `*.key`：密钥文件；
- `__pycache__/`、`*.pyc`：Python 自动生成的缓存。

不要因为文件“暂时没用”就直接删除。先判断它是：

- 项目源文件；
- 学习记录；
- 可重新生成的缓存；
- 敏感配置；
- 疑似重复文件。

今天只做分类，不做大规模删除。

## 第五阶段：完成第一次提交（35 分钟）

第一次提交只处理 Day 1 的业务边界和验收标准。

在 GitHub Desktop 左侧，只勾选：

```text
exercises/fde-16week/week-01/day-01/PROJECT_CONTRACT.md
exercises/fde-16week/week-01/day-01/ISSUE_DRAFT.md
```

查看 diff，确认新增内容是：

- 价格必须注明来源和有效日期；
- 模拟价格不得作为真实采购依据。

Summary 填写：

```text
docs: 补充价格来源与模拟数据边界
```

Description 可填写：

```text
完成 Day 1 主动审核，补充价格时效性和采购使用边界。
```

点击：

```text
Commit to main
```

提交完成后，切换到 `History`，找到刚才的提交并检查：

- 提交标题是否清楚；
- 是否只包含两个目标文件；
- 是否没有混入 Day 2 文件。

## 第六阶段：完成第二次提交（25 分钟）

回到 `Changes`，只勾选 Day 2 的三个文件：

```text
exercises/fde-16week/week-01/day-02/DAY02-学习计划.md
exercises/fde-16week/week-01/day-02/COMMIT_PLAN.md
exercises/fde-16week/week-01/day-02/day02_repo_audit.py
```

Summary 填写：

```text
chore: 添加 Day 2 仓库审计材料
```

Description 可填写：

```text
增加仓库状态、安全文件和重复文件检查工具。
```

提交后再次进入 `History`，确认两个提交的目的不同、文件范围不同。

## 第七阶段：复盘（10 分钟）

回答下面四题：

1. 保存、提交和上传有什么区别？
2. 为什么 `.env` 和密钥文件不能提交到仓库？
3. 为什么 Day 1 文档修改和 Day 2 审计工具要拆成两个提交？
4. 如果 Agent 一次修改了 20 个文件，你应该先看提交标题，还是先看 diff？为什么？

## 今天暂时不做

- 不发布当前完整学习项目到公开 GitHub；
- 不删除审计工具报告的疑似重复文件；
- 不合并或压缩历史提交；
- 不学习 rebase、stash 等高级 Git 操作；
- 不重构成本计算器业务代码。

## 今日验收清单

- [ ] 已把现有 FDE 学习项目加入 GitHub Desktop；
- [ ] 能解释保存、提交和上传的区别；
- [ ] 已运行仓库审计工具；
- [ ] 能说明 `.gitignore` 中至少 5 条规则的意义；
- [ ] 第一次提交只包含 Day 1 的两个文档；
- [ ] 第二次提交只包含 Day 2 的三个文件；
- [ ] 两次提交标题都能说明完成了什么；
- [ ] 能在 History 中查看两个提交及其文件范围。

## 提醒

GitHub Desktop 如果显示 `No local changes`，只代表当前没有未提交修改。

它不代表：

- 没有历史提交；
- 本地和 GitHub 一定同步；
- 当前分支和 `main` 没有差异。

