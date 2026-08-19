# Day 07 学习计划：从数据模板生成业务摘要

## 今日主题

Day 6 我们学的是：

```text
数据进来之前，要先校验。
```

Day 7 学的是：

```text
数据进来之后，要变成业务能看懂的摘要。
```

FDE 不能只把 CSV 读出来，也不能只说“程序跑通了”。你要让业务方看到：

- 有多少品种；
- 有多少播期；
- 每个品种当前记录到哪个生育期；
- 哪些小区最近有观察记录；
- 这份数据能不能作为后续提醒、看板、报告的基础。

## 今日目标

你今天要学会：

1. 读取已经校验过的 CSV 数据；
2. 按“品种 + 播期”分组；
3. 生成业务摘要；
4. 输出一份 Markdown 报告；
5. 理解“数据摘要”和“业务判断”的边界。

## 文件说明

今天新增：

- `DAY07-学习计划.md`：今天这份学习说明；
- `generate_breeding_summary.py`：读取 CSV 并生成摘要报告；
- `EXPECTED_SUMMARY.md`：你运行后大致应该看到的报告结构。

今天复用 Day 6 的示例数据：

- `../day-06/data/breeding_observations.example.csv`

## 运行命令

在项目根目录运行：

```powershell
python .\exercises\fde-16week\week-01\day-07\generate_breeding_summary.py --data .\exercises\fde-16week\week-01\day-06\data\breeding_observations.example.csv --out .\exercises\fde-16week\week-01\day-07\breeding_summary.generated.md
```

运行成功后，你会看到：

```text
Day 07 育种记录摘要报告生成
报告已生成：...
```

然后打开：

```text
breeding_summary.generated.md
```

## 今天重点理解

### 1. 摘要不是判断

程序可以说：

```text
稻香A 第一播期 最近记录：抽穗，2026-07-18
```

但程序不能直接说：

```text
稻香A 表现很好，建议推广。
```

前者是数据摘要，后者是业务判断。

### 2. FDE 要给业务一个能继续讨论的结果

原始 CSV 对业务方不友好。

摘要报告更友好，因为它把数据整理成：

- 总览；
- 按品种分组；
- 按播期分组；
- 最近观察；
- 明确边界。

### 3. 这是未来看板的雏形

今天输出的是 Markdown 报告。

以后可以继续进化成：

- 网页看板；
- 日历提醒；
- 小区进度图；
- 品种生育期对比；
- 田间操作日志。

## 今日复盘问题

1. 原始 CSV 和业务摘要报告有什么区别？
2. 为什么“最近记录到抽穗期”是摘要，而“表现很好”是判断？
3. 今天脚本里哪些部分偏 Echo，哪些部分偏 Delta？
4. 如果朋友后续要做育种基地管理工具，今天这个摘要报告可以变成什么功能？

## 今日提交建议

如果你完成并确认运行通过，可以提交：

```text
feat: 添加 Day 7 育种记录摘要报告练习
```

