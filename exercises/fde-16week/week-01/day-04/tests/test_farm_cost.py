"""Day 04 tests for the Day 03 deterministic cost core."""

import importlib.util
from pathlib import Path

import pytest


DAY03_MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "day-03"
    / "src"
    / "farm_cost.py"
)

spec = importlib.util.spec_from_file_location("day03_farm_cost", DAY03_MODULE_PATH)
farm_cost = importlib.util.module_from_spec(spec)
spec.loader.exec_module(farm_cost)


def make_item(name="肥料", cost_per_mu=200.0):
    return {
        "name": name,
        "cost_per_mu": cost_per_mu,
        "unit": "元/亩",
        "source": "模拟数据",
        "effective_date": "2026-07-26",
        "is_mock": True,
    }


def test_single_item_cost_per_mu():
    items = [make_item("肥料", 200.0)]

    assert farm_cost.calculate_cost_per_mu(items) == 200.0


def test_multiple_items_cost_per_mu():
    items = [
        make_item("种子", 60.0),
        make_item("肥料", 200.0),
        make_item("植保", 95.0),
        make_item("灌溉", 120.0),
    ]

    assert farm_cost.calculate_cost_per_mu(items) == 475.0


def test_decimal_total_cost():
    total_cost = farm_cost.calculate_total_cost(12.5, 475.35)

    assert total_cost == pytest.approx(5941.875)


def test_zero_cost_item_is_allowed():
    items = [make_item("示范补贴项", 0.0)]

    report = farm_cost.build_cost_report(100, items)

    assert report["cost_per_mu"] == 0.0
    assert report["total_cost"] == 0.0


def test_empty_items_return_zero_cost():
    report = farm_cost.build_cost_report(100, [])

    assert report["cost_per_mu"] == 0
    assert report["total_cost"] == 0


def test_missing_cost_per_mu_field_raises_error():
    item = make_item()
    del item["cost_per_mu"]

    with pytest.raises(farm_cost.CostInputError, match="cost_per_mu"):
        farm_cost.build_cost_report(100, [item])


def test_text_cost_per_mu_raises_error():
    items = [make_item(cost_per_mu="200")]

    with pytest.raises(farm_cost.CostInputError, match="亩成本必须是数字"):
        farm_cost.build_cost_report(100, items)


def test_negative_cost_per_mu_raises_error():
    items = [make_item(cost_per_mu=-1)]

    with pytest.raises(farm_cost.CostInputError, match="亩成本不能小于 0"):
        farm_cost.build_cost_report(100, items)


def test_zero_area_raises_error():
    items = [make_item()]

    with pytest.raises(farm_cost.CostInputError, match="种植面积必须大于 0"):
        farm_cost.build_cost_report(0, items)


def test_negative_area_raises_error():
    items = [make_item()]

    with pytest.raises(farm_cost.CostInputError, match="种植面积必须大于 0"):
        farm_cost.build_cost_report(-10, items)
