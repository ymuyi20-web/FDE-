"""Day 02：只读的 Git 仓库审计工具。

用途：
1. 查看当前仓库与分支状态；
2. 发现缓存、临时文件、疑似敏感文件和重复文件；
3. 帮助学习者在 commit 前决定“哪些文件应该进入仓库”。

本程序只读取和报告，不会删除、移动或修改任何文件。
"""

from __future__ import annotations

import hashlib
import subprocess
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]

SKIP_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "tmp",
}

SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    "credentials.json",
    "secrets.json",
}

SENSITIVE_SUFFIXES = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
}

GENERATED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
}

MAX_HASH_SIZE = 2 * 1024 * 1024


def run_git(*arguments: str) -> tuple[bool, str]:
    """运行只读 Git 命令，并返回是否成功和输出文本。"""
    command = ["git", "-C", str(PROJECT_ROOT), *arguments]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return False, "没有找到 Git，请确认 GitHub Desktop 已正确安装。"

    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode == 0, output


def iter_project_files():
    """遍历项目文件，跳过版本库、虚拟环境和缓存目录。"""
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file():
            continue

        relative_parts = path.relative_to(PROJECT_ROOT).parts
        if any(part in SKIP_DIRECTORIES for part in relative_parts):
            continue

        yield path


def classify_files(files):
    """找出疑似敏感、自动生成和命名可疑的文件。"""
    sensitive = []
    generated = []
    suspicious_names = []

    for path in files:
        lower_name = path.name.lower()

        if (
            lower_name in SENSITIVE_NAMES
            or path.suffix.lower() in SENSITIVE_SUFFIXES
            or any(word in lower_name for word in ("password", "secret", "token"))
        ):
            sensitive.append(path)

        if path.suffix.lower() in GENERATED_SUFFIXES:
            generated.append(path)

        if "copy" in lower_name or "副本" in lower_name:
            suspicious_names.append(path)

    return sensitive, generated, suspicious_names


def find_content_duplicates(files):
    """按文件内容哈希寻找完全相同的小文件。"""
    hashes = defaultdict(list)

    for path in files:
        try:
            if path.stat().st_size == 0 or path.stat().st_size > MAX_HASH_SIZE:
                continue

            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            hashes[digest].append(path)
        except OSError:
            continue

    return [group for group in hashes.values() if len(group) > 1]


def show_paths(title, paths):
    """以相对路径打印一组审计结果。"""
    print(f"\n{title}：{len(paths)}")

    if not paths:
        print("  未发现")
        return

    for path in paths[:20]:
        print(f"  - {path.relative_to(PROJECT_ROOT)}")

    if len(paths) > 20:
        print(f"  ……其余 {len(paths) - 20} 项未展开")


def main():
    print("Day 02 Git 仓库审计")
    print("=" * 48)
    print(f"项目目录：{PROJECT_ROOT}")

    is_repo, repo_message = run_git("rev-parse", "--is-inside-work-tree")
    print(f"Git 仓库：{'是' if is_repo and repo_message == 'true' else '否'}")

    if not is_repo:
        print(f"提示：{repo_message}")
        return

    branch_ok, branch = run_git("branch", "--show-current")
    print(f"当前分支：{branch if branch_ok and branch else '无法识别'}")

    status_ok, status = run_git("status", "--short")
    changed_lines = status.splitlines() if status_ok and status else []
    print(f"未提交改动：{len(changed_lines)} 项")

    for line in changed_lines[:15]:
        print(f"  {line}")

    if len(changed_lines) > 15:
        print(f"  ……其余 {len(changed_lines) - 15} 项未展开")

    gitignore_path = PROJECT_ROOT / ".gitignore"
    print(f".gitignore：{'存在' if gitignore_path.exists() else '缺失'}")

    files = list(iter_project_files())
    sensitive, generated, suspicious_names = classify_files(files)
    duplicate_groups = find_content_duplicates(files)

    print(f"参与审计的文件：{len(files)} 个")
    show_paths("疑似敏感文件", sensitive)
    show_paths("自动生成或临时文件", generated)
    show_paths("名称疑似重复的文件", suspicious_names)

    print(f"\n内容完全相同的文件组：{len(duplicate_groups)}")
    for index, group in enumerate(duplicate_groups[:10], start=1):
        print(f"  第 {index} 组：")
        for path in group:
            print(f"    - {path.relative_to(PROJECT_ROOT)}")

    if len(duplicate_groups) > 10:
        print(f"  ……其余 {len(duplicate_groups) - 10} 组未展开")

    print("\n结论")
    print("-" * 48)

    if sensitive:
        print("发现疑似敏感文件：提交前必须逐项确认，不能直接上传。")
    else:
        print("未发现明显的密钥或敏感配置文件。")

    if generated or suspicious_names or duplicate_groups:
        print("发现需要人工判断的文件：本工具只报告，不会自动删除。")
    else:
        print("未发现明显的缓存、临时文件或重复文件。")

    print("提交前仍需在 GitHub Desktop 中逐文件查看 diff。")


if __name__ == "__main__":
    main()
