"""Verify the key commands documented in the Day 05 README draft."""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]


def run_command(command):
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main():
    demo_command = [
        sys.executable,
        r".\exercises\fde-16week\week-01\day-03\run_day03_demo.py",
        "--area",
        "100",
    ]
    test_command = [
        sys.executable,
        "-m",
        "pytest",
        r".\exercises\fde-16week\week-01\day-04\tests\test_farm_cost.py",
    ]

    demo_result = run_command(demo_command)
    if demo_result.returncode != 0 or "47500.00" not in demo_result.stdout:
        print("README 命令检查失败：正常样例没有得到预期总成本。")
        print(demo_result.stdout)
        print(demo_result.stderr)
        return 1

    test_result = run_command(test_command)
    if test_result.returncode != 0 or "10 passed" not in test_result.stdout:
        print("README 命令检查失败：自动化测试没有全部通过。")
        print(test_result.stdout)
        print(test_result.stderr)
        return 1

    print("README 命令检查通过")
    print("- 正常样例得到 47500.00 元")
    print("- Day 4 自动化测试显示 10 passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
