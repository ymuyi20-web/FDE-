# Day 08 学习计划：品种 × 播期 × 生育期进度看板

## 今日主题

Day 6：把数据入口管住。

Day 7：把数据变成业务摘要。

Day 8：把摘要进一步变成“育种人最想看的那张表”：

```text
品种/材料 × 播期 × 当前生育期
```

也就是你朋友选的 B 方案。

## 今天先替用户做合理假设

因为朋友最近忙，还没给完整需求，所以我们先基于常见育种基地/田间试验工作流做一版“默认假设”。

### 问题 1：一般一个材料会有几个播期？

默认按 3 个播期处理：

```text
第一播期
第二播期
第三播期
```

理由：

- 2 个播期太少，不够体现播期差异；
- 3 个播期足够覆盖早、中、晚或错期观察；
- 第一版看板不会太复杂。

### 问题 2：播期用“第一播期”还是具体日期？

第一版两个都保留：

```text
sowing_batch：第一播期
sowing_date：2026-05-01
```

页面上优先展示“第一播期”，同时在单元格里显示播种日期。

理由：

- 育种人员现场沟通时常说“第一播期、第二播期”；
- 程序做排序、提醒、间隔计算时需要真实日期。

### 问题 3：常用生育期阶段有哪些？

第一版用水稻常见阶段：

```text
播种
出苗
分蘖
拔节
孕穗
抽穗
灌浆
成熟
收获
```

这是为了先统一入口，避免同一个阶段被写成多种叫法。

### 问题 4：除了当前生育期，要不要显示下一步？

要显示。

第一版显示：

```text
当前生育期
最近观察日期
下一步观察事项
```

理由：

- 只看“当前生育期”还不够指导现场工作；
- 育种人还需要知道“下一次该看什么”；
- 这会自然发展成后续的“今日待办”功能。

## 今日目标

你今天要学会：

1. 读取多品种、多播期、多小区记录；
2. 提取每个“品种 + 播期”的最近生育期；
3. 生成一个矩阵式 Markdown 看板；
4. 生成一个更接近产品的 HTML 看板；
5. 区分“看板呈现”和“育种判断”的边界。

## 新增文件

- `DAY08-学习计划.md`
- `BREEDING_BOARD_ASSUMPTIONS.md`
- `data/breeding_stage_records.example.csv`
- `generate_stage_board.py`
- 运行后生成：
  - `breeding_stage_board.generated.md`
  - `breeding_stage_board.generated.html`

## 运行命令

在项目根目录运行：

```powershell
python .\exercises\fde-16week\week-01\day-08\generate_stage_board.py --data .\exercises\fde-16week\week-01\day-08\data\breeding_stage_records.example.csv --md-out .\exercises\fde-16week\week-01\day-08\breeding_stage_board.generated.md --html-out .\exercises\fde-16week\week-01\day-08\breeding_stage_board.generated.html
```

运行成功后，打开：

```text
breeding_stage_board.generated.md
breeding_stage_board.generated.html
```

## 今日观察重点

看生成结果时重点看：

- 每个品种是不是按行展示；
- 每个播期是不是按列展示；
- 每个格子里是不是显示当前生育期、播种日期、最近观察日期；
- 没有记录的播期是不是显示“未记录”；
- 下一步观察事项是否清晰。

## 今日复盘问题

1. 为什么育种看板第一列应该是“品种/材料”，而不是“地块”？
2. 为什么播期既要有“第一播期”这种名称，又要有真实播种日期？
3. 今天这个看板里，哪些内容是事实摘要，哪些内容已经接近业务提醒？
4. 如果要给你朋友试用，第一版最应该让他验证哪 3 件事？

## 今日提交建议

```text
feat: 添加 Day 8 育种生育期进度看板练习
```

