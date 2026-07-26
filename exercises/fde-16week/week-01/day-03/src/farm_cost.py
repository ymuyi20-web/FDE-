"""Deterministic cost calculation for rice farm inputs.

The functions in this module do not ask for keyboard input and do not print.
That keeps the calculation easy to test and reuse.
"""

import json
from pathlib import Path


REQUIRED_FIELDS = {
    "name",
    "cost_per_mu",
    "unit",
    "source",
    "effective_date",
    "is_mock",
}


class CostInputError(ValueError):
    """Raised when farm input data cannot be trusted for calculation."""


def load_items(path):
    """Load farm input items from a UTF-8 JSON file."""
    with open(Path(path), "r", encoding="utf-8") as file:
        return json.load(file)


def validate_inputs(area_mu, items):
    """Validate area and farm input items before deterministic calculation."""
    if not isinstance(area_mu, (int, float)) or isinstance(area_mu, bool):
        raise CostInputError("种植面积必须是数字。")

    if area_mu <= 0:
        raise CostInputError("种植面积必须大于 0。")

    if not isinstance(items, list):
        raise CostInputError("农资配置最外层必须是列表。")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise CostInputError(f"第 {index} 项农资必须是对象。")

        missing_fields = REQUIRED_FIELDS - item.keys()
        if missing_fields:
            fields_text = "、".join(sorted(missing_fields))
            raise CostInputError(f"第 {index} 项农资缺少字段：{fields_text}。")

        if not isinstance(item["name"], str) or not item["name"].strip():
            raise CostInputError(f"第 {index} 项农资名称不能为空。")

        cost = item["cost_per_mu"]
        if not isinstance(cost, (int, float)) or isinstance(cost, bool):
            raise CostInputError(f"第 {index} 项农资亩成本必须是数字。")

        if cost < 0:
            raise CostInputError(f"第 {index} 项农资亩成本不能小于 0。")

        if item["unit"] != "元/亩":
            raise CostInputError(f"第 {index} 项农资单位必须是 元/亩。")

        if not isinstance(item["source"], str) or not item["source"].strip():
            raise CostInputError(f"第 {index} 项农资必须标注价格来源。")

        if not isinstance(item["effective_date"], str) or not item["effective_date"].strip():
            raise CostInputError(f"第 {index} 项农资必须标注价格有效日期。")

        if not isinstance(item["is_mock"], bool):
            raise CostInputError(f"第 {index} 项农资 is_mock 必须是 true 或 false。")


def calculate_cost_per_mu(items):
    """Calculate the total cost per mu from validated farm input items."""
    return sum(item["cost_per_mu"] for item in items)


def calculate_total_cost(area_mu, cost_per_mu):
    """Calculate total cost for a given planting area."""
    return area_mu * cost_per_mu


def build_cost_report(area_mu, items):
    """Validate inputs and return a complete cost report dictionary."""
    validate_inputs(area_mu, items)
    cost_per_mu = calculate_cost_per_mu(items)
    total_cost = calculate_total_cost(area_mu, cost_per_mu)
    return {
        "area_mu": float(area_mu),
        "cost_per_mu": cost_per_mu,
        "total_cost": total_cost,
        "items": items,
        "business_boundary": "仅用于成本核算，不构成施肥处方、采购依据或农艺建议。",
    }
