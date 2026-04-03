#!/usr/bin/env python3
"""Version manager for generated crush skills.

Usage:
    python version_manager.py --action <backup|rollback|list> --slug <slug> --base-dir <path> [--version <v>]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


TRACKED_FILES = ("memory.md", "persona.md", "SKILL.md", "meta.json")


def default_base_dir() -> str:
    repo_root = Path(__file__).resolve().parents[1]
    if repo_root.parent.name == "skills":
        return str(repo_root.parent)
    return str(repo_root / "crushes")


def backup(base_dir: str, slug: str) -> str:
    skill_dir = Path(base_dir) / slug
    versions_dir = skill_dir / "versions"
    meta_path = skill_dir / "meta.json"

    if not meta_path.exists():
        print(f"错误：找不到 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with meta_path.open("r", encoding="utf-8") as file:
        meta = json.load(file)

    versions_dir.mkdir(parents=True, exist_ok=True)
    current_version = meta.get("version", "v0")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{current_version}_{timestamp}"
    backup_dir = versions_dir / backup_name
    backup_dir.mkdir(parents=True, exist_ok=True)

    for file_name in TRACKED_FILES:
        src = skill_dir / file_name
        if src.exists():
            shutil.copy2(src, backup_dir / file_name)

    print(f"已备份版本：{backup_name}")
    return backup_name


def rollback(base_dir: str, slug: str, version: str) -> None:
    skill_dir = Path(base_dir) / slug
    versions_dir = skill_dir / "versions"

    if not versions_dir.is_dir():
        print("错误：还没有历史版本可回滚。", file=sys.stderr)
        sys.exit(1)

    target_dir = None
    for candidate in sorted(versions_dir.iterdir(), reverse=True):
        if candidate.is_dir() and (candidate.name == version or candidate.name.startswith(version)):
            target_dir = candidate
            break

    if target_dir is None:
        print(f"错误：找不到版本 {version}", file=sys.stderr)
        list_versions(base_dir, slug)
        sys.exit(1)

    backup(base_dir, slug)
    for file_name in TRACKED_FILES:
        src = target_dir / file_name
        if src.exists():
            shutil.copy2(src, skill_dir / file_name)

    print(f"已回滚到版本 {target_dir.name}")


def list_versions(base_dir: str, slug: str) -> None:
    versions_dir = Path(base_dir) / slug / "versions"
    if not versions_dir.is_dir():
        print("没有历史版本。")
        return

    versions = [entry.name for entry in sorted(versions_dir.iterdir(), reverse=True) if entry.is_dir()]
    if not versions:
        print("没有历史版本。")
        return

    print(f"历史版本（共 {len(versions)} 个）：\n")
    for version in versions:
        print(f"  {version}")


def main() -> None:
    parser = argparse.ArgumentParser(description="crush Skill 版本管理器")
    parser.add_argument("--action", required=True, choices=["backup", "rollback", "list"])
    parser.add_argument("--slug", required=True, help="暗恋对象代号")
    parser.add_argument("--base-dir", default=default_base_dir(), help="基础目录")
    parser.add_argument("--version", help="目标版本")
    args = parser.parse_args()

    if args.action == "backup":
        backup(args.base_dir, args.slug)
    elif args.action == "rollback":
        if not args.version:
            print("错误：rollback 需要 --version 参数", file=sys.stderr)
            sys.exit(1)
        rollback(args.base_dir, args.slug, args.version)
    else:
        list_versions(args.base_dir, args.slug)


if __name__ == "__main__":
    main()
