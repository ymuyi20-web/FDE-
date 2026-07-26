# Day 03 学习计划：整理确定性计算核心

## 今天的目标

把 Day 1 的“能运行脚本”整理成更像交付物的结构：

- 计算逻辑不依赖键盘输入；
- 计算逻辑不直接打印结果；
- 数据校验失败时给出明确错误；
- 换一份 JSON 数据，不需要改计算函数；
- 为 Day 4 的自动化测试留下接口。

一句话：今天不是加功能，而是把“算得对”整理成“别人能检查、能复用、能测试”。

## 你今天要学会的 3 个词

1. 核心逻辑

   只负责算和校验，不负责问用户、读文件、打印。

2. 运行入口

   负责接收参数、读取 JSON、调用核心逻辑、展示结果。

3. 业务边界

   程序只能做确定性成本核算，不能偷偷变成施肥建议、采购建议或作物模型。

## 今天的文件

- `src/farm_cost.py`：核心计算模块。
- `data/farm_inputs.example.json`：样例农资数据。
- `run_day03_demo.py`：最小运行入口。

## 阶段 1：先读代码，不运行

打开 `src/farm_cost.py`，重点看这几个函数：

- `validate_inputs(area_mu, items)`
- `calculate_cost_per_mu(items)`
- `calculate_total_cost(area_mu, cost_per_mu)`
- `build_cost_report(area_mu, items)`

你只需要先看懂一件事：

> 这些函数都没有 `input()`，也不直接让用户输入面积。

这说明它们可以被测试程序直接调用。

## 阶段 2：运行正常样例

在终端运行：

```powershell
cd "D:\CodexProjects\FDE学习项目"
python .\exercises\fde-16week\week-01\day-03\run_day03_demo.py --area 100
```

你应该看到：

- 每亩农资成本：475.00 元/亩
- 预计总成本：47500.00 元

## 阶段 3：观察错误边界

分别运行：

```powershell
python .\exercises\fde-16week\week-01\day-03\run_day03_demo.py --area 0
python .\exercises\fde-16week\week-01\day-03\run_day03_demo.py --area -10
python .\exercises\fde-16week\week-01\day-03\run_day03_demo.py --area abc
```

观察它们是否会继续计算。

注意：`abc` 这一条会由命令行参数解析直接拦住，这也算有效防线。

## 阶段 4：看数据契约

打开 `data/farm_inputs.example.json`，确认每个农资项目都有：

- `name`
- `cost_per_mu`
- `unit`
- `source`
- `effective_date`
- `is_mock`

今天新增这些字段，是为了提前贴近“智慧农业研究员”的工作：肥料决策不能只看价格数字，还要看来源、时效和是否为模拟数据。

## 今天不要做

- 不要接入 AI API；
- 不要生成施肥处方；
- 不要把作物模型接进来；
- 不要发布仓库；
- 不要提交 `README.md` 那个遗留改动。

## 今日验收

- [ ] 能运行 `--area 100` 并得到 475 和 47500；
- [ ] 面积为 0 或负数时不会继续计算；
- [ ] 能说清楚为什么核心函数里不放 `input()`；
- [ ] 能说清楚为什么价格数据要带来源和有效日期；
- [ ] GitHub Desktop 中只提交 Day 3 新增文件，不混入 README。

## 建议提交信息

```text
refactor: 整理 Day 3 成本计算核心
```

## 今日复盘题

1. 为什么 `calculate_cost_per_mu()` 不应该自己读取 JSON？
2. 为什么 `validate_inputs()` 要检查价格来源和有效日期？
3. 如果程序算出来是 47500 元，但价格来源是去年的，这属于代码错误还是业务错误？
4. 今天的 `src/farm_cost.py`，哪些部分属于 Delta？哪些地方是在保护 Echo？
