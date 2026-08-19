# Day 10 学习计划：农事操作日志

## 今天的目标

Day 8 做了“品种/材料 × 播期 × 生育期进度看板”。  
Day 9 做了“今日观察待办”。  
Day 10 做第三个方向：

> 农事操作日志：把播种、施肥、打药、拍照、巡田、测量这些操作按日期串起来。

你朋友说“农事操作日期很多、播期也繁杂”，那这个模块就很贴近真实痛点。

## 今天你要理解的 FDE 点

### 1. 操作日志不是学习笔记

操作日志记录的是现场发生过什么。

比如：

- 2026-05-01，稻香A，第一播期，A-01 小区，完成播种；
- 2026-06-20，稻香A，第一播期，A-01 小区，喷施防病药剂；
- 2026-07-18，稻香A，第一播期，A-01 小区，拍照记录抽穗。

这些是可追溯记录，不是个人感想。

### 2. 一个好的日志要能追溯责任

所以 Day 10 的数据里会有：

- 操作日期；
- 品种/材料；
- 播期；
- 小区；
- 操作类型；
- 操作内容；
- 负责人；
- 是否需要复查；
- 备注。

如果未来出了问题，比如“这个小区为什么长势异常”，就可以回头查：

- 有没有漏施肥；
- 有没有打药；
- 谁记录的；
- 哪天做的。

### 3. 日志是事实，结论是判断

日志可以写：

> 2026-06-20 喷施防病药剂。

但不应该直接写：

> 这个材料抗病性很好。

后者是育种判断，需要更多证据。

## 今天的学习阶段

### 阶段一：阅读操作日志字段说明

先阅读：

- `OPERATION_LOG_CONTRACT.md`

重点看：

- 哪些字段必须填；
- 为什么要有负责人；
- 哪些内容属于事实记录，哪些内容不能乱写。

### 阶段二：运行日志生成脚本

如果你在项目根目录：

```powershell
python .\exercises\fde-16week\week-01\day-10\generate_operation_log.py --data .\exercises\fde-16week\week-01\day-10\data\breeding_operations.example.csv --md-out .\exercises\fde-16week\week-01\day-10\operation_log.generated.md --html-out .\exercises\fde-16week\week-01\day-10\operation_log.generated.html
```

如果你当前位置是：

```text
D:\CodexProjects\FDE学习项目\exercises\fde-16week
```

运行：

```powershell
python .\week-01\day-10\generate_operation_log.py --data .\week-01\day-10\data\breeding_operations.example.csv --md-out .\week-01\day-10\operation_log.generated.md --html-out .\week-01\day-10\operation_log.generated.html
```

### 阶段三：打开 HTML 日志

打开：

- `operation_log.generated.html`

重点观察：

- 最上面的操作类型统计；
- 时间线是否容易看懂；
- 按材料/播期汇总是否能帮助回溯。

### 阶段四：改一条样例数据

你可以打开：

- `data/breeding_operations.example.csv`

新增一条：

```csv
OP20260720003,2026-07-20,稻香B,第二播期,B-02,拍照,拍照记录拔节后株型,王工,否,补充影像资料
```

然后重新运行脚本，观察结果是否变化。

## 今日复盘问题

1. 农事操作日志和 Day 8 的生育期看板有什么区别？
2. 为什么操作日志里要有负责人？
3. “已喷施防病药剂”是事实，还是业务判断？
4. 如果朋友说“我想知道每个材料从播种到抽穗都做过哪些操作”，Day 10 的日志可以变成什么功能？

## 今日交付物

完成后，你应该有：

- `OPERATION_LOG_CONTRACT.md`
- `data/breeding_operations.example.csv`
- `generate_operation_log.py`
- `operation_log.generated.md`
- `operation_log.generated.html`

