# Day 05 学习计划：写一份陌生人能用的 README

## 今天的目标

把 Day 3 的代码和 Day 4 的测试，整理成一份可交付说明。

FDE 的 README 不是学习笔记，而是交付入口。它要让一个没听你口头解释的人，也能回答四个问题：

- 这个工具解决什么问题？
- 我该怎么运行？
- 我怎么知道结果对不对？
- 它明确不能做什么？

一句话：

> README 是让交付物离开作者之后还能活下去的说明书。

## 今天的文件

- `README_DRAFT.md`：今天要审阅的 README 草稿。
- `HANDOFF_CHECKLIST.md`：交付前检查清单。
- `verify_readme_commands.py`：检查 README 里的关键命令是否还能运行。

## 阶段 1：先读 README_DRAFT

打开：

```text
D:\CodexProjects\FDE学习项目\exercises\fde-16week\week-01\day-05\README_DRAFT.md
```

先不要改，读的时候只看它有没有回答：

- 用户是谁；
- 输入是什么；
- 输出是什么；
- 怎么运行；
- 怎么测试；
- 明确不做什么；
- 哪些地方必须人工确认。

## 阶段 2：运行 README 检查脚本

在终端运行：

```powershell
cd "D:\CodexProjects\FDE学习项目"
python .\exercises\fde-16week\week-01\day-05\verify_readme_commands.py
```

你希望看到：

```text
README 命令检查通过
```

这个脚本会做两件事：

- 跑一次 `--area 100`；
- 跑一次 Day 4 的 10 条测试。

## 阶段 3：人工审阅 README

打开：

```text
D:\CodexProjects\FDE学习项目\exercises\fde-16week\week-01\day-05\HANDOFF_CHECKLIST.md
```

按清单逐项看 `README_DRAFT.md`。

今天不是让你盲目相信 README，而是让你像交付审核人一样检查它。

## 阶段 4：主动改一处 README

你至少主动改一处，可以很小，比如：

- 把某句话改得更像农业生产管理人员能看懂；
- 增加一个“不能用于真实采购”的提醒；
- 增加一个“价格有效日期必须人工确认”的说明；
- 补一句你认为新洋丰智慧农业研究员岗位会关心的边界。

改完以后重新运行：

```powershell
python .\exercises\fde-16week\week-01\day-05\verify_readme_commands.py
```

## 今日不要做

- 不要改根目录 `README.md`；
- 不要发布仓库；
- 不要把这个工具说成施肥推荐系统；
- 不要接入作物模型；
- 不要删除之前那个遗留的 `README.md` 改动。

## 今日验收

- [ ] 能说清楚 README 和学习笔记的区别；
- [ ] `verify_readme_commands.py` 检查通过；
- [ ] 至少主动修改一处 README_DRAFT；
- [ ] README 里写清楚“只做成本核算，不构成施肥处方”；
- [ ] README 里写清楚价格来源、有效日期、模拟数据边界；
- [ ] GitHub Desktop 只提交 Day 5 目录，不混入根目录 `README.md`。

## 建议提交信息

```text
docs: 添加 Day 5 交付 README 草稿
```

## 今日复盘题

1. README 和学习笔记最大的区别是什么？
2. 为什么 README 里要写“明确不做什么”？
3. 对智慧农业研究员岗位来说，README 里最重要的人工确认点是什么？
4. 如果陌生人按 README 运行失败，这更像代码问题、说明问题，还是交付问题？
