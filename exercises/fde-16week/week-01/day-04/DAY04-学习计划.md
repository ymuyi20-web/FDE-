# Day 04 学习计划：用 10 条测试建立交付证据

## 今天的目标

把 Day 3 的成本计算核心变成“可验证交付物”。

昨天我们已经把计算逻辑拆成了函数。今天要做的是：用 10 条自动化测试证明这些函数在关键场景下没有被改坏。

一句话：

> 测试不是为了证明程序永远正确，而是为了冻结当前承诺。

## 今天你要学会的 4 个词

1. 测试用例

   一组明确输入和明确预期结果。

2. assert

   程序里的“验收打勾”。条件成立就通过，不成立就失败。

3. pytest

   一个自动寻找并运行测试的工具。

4. 回归

   原来对的功能，被后来的改动弄坏了。

## 今天的文件

- `tests/test_farm_cost.py`：10 条自动化测试。

这个文件会测试 Day 3 的 `src/farm_cost.py`。

## 阶段 1：先运行测试

在终端运行：

```powershell
cd "D:\CodexProjects\FDE学习项目"
python -m pytest .\exercises\fde-16week\week-01\day-04\tests\test_farm_cost.py
```

你希望看到类似：

```text
10 passed
```

如果提示没有 pytest，运行：

```powershell
python -m pip install pytest
```

安装后再运行测试。

## 阶段 2：看懂测试保护了什么

打开 `tests/test_farm_cost.py`，重点看测试名字。

测试名字不是随便起的，它们就是交付承诺：

- 单个农资能算对；
- 多个农资能算对；
- 小数金额能算对；
- 成本为 0 可以接受；
- 空农资列表可以返回 0；
- 缺字段会报错；
- 非数字成本会报错；
- 负数成本会报错；
- 面积为 0 会报错；
- 面积为负数会报错。

## 阶段 3：故意制造一次失败

打开：

```text
D:\CodexProjects\FDE学习项目\exercises\fde-16week\week-01\day-03\src\farm_cost.py
```

找到：

```python
return sum(item["cost_per_mu"] for item in items)
```

临时改成：

```python
return sum(item["cost_per_mu"] for item in items) + 1
```

然后重新运行测试。你应该看到至少一条失败。

看完失败后，马上改回原来的：

```python
return sum(item["cost_per_mu"] for item in items)
```

再运行测试，确认重新通过。

## 阶段 4：提交前检查

GitHub Desktop 中只提交 Day 4 新增文件：

```text
exercises/fde-16week/week-01/day-04/
```

不要提交 `README.md`。

建议提交标题：

```text
test: 添加 Day 4 成本计算自动化测试
```

## 今日验收

- [ ] 运行测试能看到 `10 passed`；
- [ ] 故意改错公式后，测试能失败；
- [ ] 恢复公式后，测试重新通过；
- [ ] 能说清楚至少 3 条测试分别保护了什么业务承诺；
- [ ] 提交时没有混入 `README.md`。

## 今日复盘题

1. 为什么测试不是“证明程序永远正确”？
2. 今天哪一条测试最像农业业务边界，而不是纯数学计算？
3. 如果以后有人把“成本不能为负数”的校验删了，哪条测试会拦住？
4. 在 FDE 交付里，测试结果为什么可以作为 PR 的证据？
