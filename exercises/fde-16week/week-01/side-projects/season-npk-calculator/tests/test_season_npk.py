"""Tests for the seasonal N-P2O5-K2O calculator."""

import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "season_npk.py"
spec = importlib.util.spec_from_file_location("season_npk", MODULE_PATH)
season_npk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(season_npk)


def make_fertilizer(
    name="三个15复合肥",
    amount=40.0,
    n=15.0,
    p2o5=15.0,
    k2o=15.0,
):
    return {
        "fertilizer_name": name,
        "amount_kg_per_mu": amount,
        "n_percent": n,
        "p2o5_percent": p2o5,
        "k2o_percent": k2o,
        "source": "模拟数据",
        "is_mock": True,
    }


def make_plan():
    return {
        "crop": "水稻",
        "season": "示范季",
        "nutrient_basis": "N-P2O5-K2O",
        "stages": [
            {"stage_name": "底肥", "fertilizers": [make_fertilizer(amount=35)]},
            {
                "stage_name": "分蘖肥",
                "fertilizers": [make_fertilizer("尿素", 20, 46, 0, 0)],
            },
            {
                "stage_name": "穗肥",
                "fertilizers": [
                    make_fertilizer(amount=10),
                    make_fertilizer("氯化钾", 10, 0, 0, 60),
                ],
            },
        ],
    }


def test_single_fertilizer_nutrients():
    result = season_npk.calculate_fertilizer_nutrients(make_fertilizer(amount=40))

    assert result["n_kg_per_mu"] == 6.0
    assert result["p2o5_kg_per_mu"] == 6.0
    assert result["k2o_kg_per_mu"] == 6.0


def test_season_totals():
    report = season_npk.build_season_report(make_plan())

    totals = report["season_totals"]
    assert totals["n_kg_per_mu"] == pytest.approx(15.95)
    assert totals["p2o5_kg_per_mu"] == pytest.approx(6.75)
    assert totals["k2o_kg_per_mu"] == pytest.approx(12.75)


def test_negative_amount_raises_error():
    plan = make_plan()
    plan["stages"][0]["fertilizers"][0]["amount_kg_per_mu"] = -1

    with pytest.raises(season_npk.NutrientInputError, match="亩用量不能小于 0"):
        season_npk.build_season_report(plan)


def test_percent_over_100_raises_error():
    plan = make_plan()
    plan["stages"][0]["fertilizers"][0]["n_percent"] = 101

    with pytest.raises(season_npk.NutrientInputError, match="0 到 100"):
        season_npk.build_season_report(plan)


def test_missing_nutrient_basis_raises_error():
    plan = make_plan()
    plan["nutrient_basis"] = "N-P-K"

    with pytest.raises(season_npk.NutrientInputError, match="N-P2O5-K2O"):
        season_npk.build_season_report(plan)
