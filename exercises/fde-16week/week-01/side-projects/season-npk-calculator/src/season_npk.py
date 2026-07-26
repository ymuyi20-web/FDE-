"""Deterministic N-P2O5-K2O input calculator for a rice season."""

import json
from pathlib import Path


NUTRIENT_KEYS = ("n", "p2o5", "k2o")
FERTILIZER_REQUIRED_FIELDS = {
    "fertilizer_name",
    "amount_kg_per_mu",
    "n_percent",
    "p2o5_percent",
    "k2o_percent",
    "source",
    "is_mock",
}


class NutrientInputError(ValueError):
    """Raised when nutrient input data cannot be trusted for calculation."""


def load_plan(path):
    """Load a seasonal fertilizer plan from a UTF-8 JSON file."""
    with open(Path(path), "r", encoding="utf-8") as file:
        return json.load(file)


def empty_totals():
    return {
        "n_kg_per_mu": 0.0,
        "p2o5_kg_per_mu": 0.0,
        "k2o_kg_per_mu": 0.0,
    }


def validate_percent(value, field_name, item_index):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise NutrientInputError(f"第 {item_index} 个肥料的 {field_name} 必须是数字。")
    if value < 0 or value > 100:
        raise NutrientInputError(f"第 {item_index} 个肥料的 {field_name} 必须在 0 到 100 之间。")


def validate_fertilizer(fertilizer, item_index):
    if not isinstance(fertilizer, dict):
        raise NutrientInputError(f"第 {item_index} 个肥料必须是对象。")

    missing_fields = FERTILIZER_REQUIRED_FIELDS - fertilizer.keys()
    if missing_fields:
        fields_text = "、".join(sorted(missing_fields))
        raise NutrientInputError(f"第 {item_index} 个肥料缺少字段：{fields_text}。")

    if not isinstance(fertilizer["fertilizer_name"], str) or not fertilizer["fertilizer_name"].strip():
        raise NutrientInputError(f"第 {item_index} 个肥料名称不能为空。")

    amount = fertilizer["amount_kg_per_mu"]
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise NutrientInputError(f"第 {item_index} 个肥料亩用量必须是数字。")
    if amount < 0:
        raise NutrientInputError(f"第 {item_index} 个肥料亩用量不能小于 0。")

    validate_percent(fertilizer["n_percent"], "n_percent", item_index)
    validate_percent(fertilizer["p2o5_percent"], "p2o5_percent", item_index)
    validate_percent(fertilizer["k2o_percent"], "k2o_percent", item_index)

    if not isinstance(fertilizer["source"], str) or not fertilizer["source"].strip():
        raise NutrientInputError(f"第 {item_index} 个肥料必须标注数据来源。")

    if not isinstance(fertilizer["is_mock"], bool):
        raise NutrientInputError(f"第 {item_index} 个肥料 is_mock 必须是 true 或 false。")


def validate_plan(plan):
    """Validate the seasonal plan structure before calculation."""
    if not isinstance(plan, dict):
        raise NutrientInputError("施肥方案最外层必须是对象。")

    if plan.get("nutrient_basis") != "N-P2O5-K2O":
        raise NutrientInputError("养分口径必须明确为 N-P2O5-K2O。")

    stages = plan.get("stages")
    if not isinstance(stages, list) or not stages:
        raise NutrientInputError("施肥方案必须包含至少一个阶段。")

    for stage_index, stage in enumerate(stages, start=1):
        if not isinstance(stage, dict):
            raise NutrientInputError(f"第 {stage_index} 个阶段必须是对象。")
        if not isinstance(stage.get("stage_name"), str) or not stage["stage_name"].strip():
            raise NutrientInputError(f"第 {stage_index} 个阶段名称不能为空。")
        fertilizers = stage.get("fertilizers")
        if not isinstance(fertilizers, list):
            raise NutrientInputError(f"{stage['stage_name']} 的 fertilizers 必须是列表。")
        for item_index, fertilizer in enumerate(fertilizers, start=1):
            validate_fertilizer(fertilizer, item_index)


def calculate_fertilizer_nutrients(fertilizer):
    """Calculate N, P2O5 and K2O kg/mu for one fertilizer."""
    amount = fertilizer["amount_kg_per_mu"]
    return {
        "n_kg_per_mu": amount * fertilizer["n_percent"] / 100,
        "p2o5_kg_per_mu": amount * fertilizer["p2o5_percent"] / 100,
        "k2o_kg_per_mu": amount * fertilizer["k2o_percent"] / 100,
    }


def add_totals(left, right):
    return {
        "n_kg_per_mu": left["n_kg_per_mu"] + right["n_kg_per_mu"],
        "p2o5_kg_per_mu": left["p2o5_kg_per_mu"] + right["p2o5_kg_per_mu"],
        "k2o_kg_per_mu": left["k2o_kg_per_mu"] + right["k2o_kg_per_mu"],
    }


def calculate_stage_totals(fertilizers):
    """Calculate nutrient totals for one fertilizer stage."""
    totals = empty_totals()
    for fertilizer in fertilizers:
        totals = add_totals(totals, calculate_fertilizer_nutrients(fertilizer))
    return totals


def build_season_report(plan):
    """Validate inputs and build a stage-level and season-level nutrient report."""
    validate_plan(plan)

    stage_reports = []
    season_totals = empty_totals()

    for stage in plan["stages"]:
        stage_totals = calculate_stage_totals(stage["fertilizers"])
        season_totals = add_totals(season_totals, stage_totals)
        stage_reports.append(
            {
                "stage_name": stage["stage_name"],
                "fertilizers": stage["fertilizers"],
                "totals": stage_totals,
            }
        )

    return {
        "crop": plan.get("crop", "未注明作物"),
        "season": plan.get("season", "未注明季节"),
        "nutrient_basis": plan["nutrient_basis"],
        "stages": stage_reports,
        "season_totals": season_totals,
        "business_boundary": "仅用于养分投入量核算，不构成施肥处方、采购依据或农艺建议。",
    }
