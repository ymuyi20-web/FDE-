# Day 09 学习计划：从生育期看板到“今日待办”

## 今天的目标

今天继续围绕育种朋友的 B 方向：`品种/材料 × 播期 × 生育期进度看板`。

Day 8 已经能回答“现在各材料到什么阶段了”。  
Day 9 要继续回答一个更接近日常管理的问题：

> 今天我应该优先去看哪些材料、哪些播期、哪些小区？

这就是从“展示信息”走向“辅助执行”。

## 今天你要理解的 FDE 点

### 1. 同一份数据，可以生成不同交付物

Day 8 用 CSV 生成了进度看板。  
Day 9 仍然用同一份 CSV，但生成的是观察待办。

这说明 FDE 交付里，数据结构一旦设计对了，后面可以不断长出新功能。

### 2. 待办不是育种判断

今日待办只回答：

- 哪些记录距离上次观察太久；
- 哪些阶段需要更高频复查；
- 哪些材料/播期应该优先去现场确认。

它不回答：

- 哪个材料最好；
- 哪个材料应该淘汰；
- 哪个组合最有推广价值。

这些仍然属于育种专家判断。

### 3. 规则要写出来，而不是藏在代码里

比如：

- 播种后 7 天内要看出苗；
- 抽穗期 3 天左右就应该复查；
- 孕穗期 5 天左右需要关注抽穗节点。

这些是业务规则。  
如果未来朋友说“我们抽穗期 2 天就要看一次”，你应该能改规则，而不是重写整个程序。

## 今天的学习阶段

### 阶段一：阅读业务规则

先阅读：

- `OBSERVATION_RULES.md`

重点看懂：

- 为什么不同生育期的复查间隔不一样；
- 哪些是事实记录；
- 哪些是提醒规则。

### 阶段二：运行待办生成脚本

在项目根目录运行：

```powershell
python .\exercises\fde-16week\week-01\day-09\generate_observation_tasks.py --data .\exercises\fde-16week\week-01\day-08\data\breeding_stage_records.example.csv --today 2026-07-27 --md-out .\exercises\fde-16week\week-01\day-09\observation_tasks.generated.md --html-out .\exercises\fde-16week\week-01\day-09\observation_tasks.generated.html
```

如果你现在的位置是：

```text
D:\CodexProjects\FDE学习项目\exercises\fde-16week
```

则运行：

```powershell
python .\week-01\day-09\generate_observation_tasks.py --data .\week-01\day-08\data\breeding_stage_records.example.csv --today 2026-07-27 --md-out .\week-01\day-09\observation_tasks.generated.md --html-out .\week-01\day-09\observation_tasks.generated.html
```

### 阶段三：打开 HTML 看板

打开：

- `observation_tasks.generated.html`

你重点观察：

- 哪些任务是“逾期”；
- 哪些任务是“今日到期”；
- 哪些任务是“正常跟踪”；
- 最上方的统计数字是否能帮你快速判断基地状态。

### 阶段四：改一个日期再运行

把命令里的日期改成：

```text
2026-06-20
```

再运行一次，观察待办列表如何变化。

你要理解：

> 同一份 CSV，不同的“今天日期”，会生成不同的执行清单。

这就是业务系统里的时间上下文。

## 今日复盘问题

1. 为什么 Day 9 的输入仍然可以沿用 Day 8 的 CSV？
2. “当前生育期是抽穗”是事实，还是提醒？
3. “抽穗期 3 天后复查”是事实，还是规则？
4. 如果朋友说“我们基地抽穗期必须每天看”，你应该改数据，还是改规则？

## 今日交付物

完成后，你应该有：

- `OBSERVATION_RULES.md`
- `generate_observation_tasks.py`
- `observation_tasks.generated.md`
- `observation_tasks.generated.html`

