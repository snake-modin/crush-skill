#!/usr/bin/env python3
"""Skill file utilities for generated crush skills.

Usage:
    python skill_writer.py --action <list|init|combine|delete|bootstrap> --base-dir <path> [--slug <slug>]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


CORE_FILES = ("memory.md", "persona.md", "SKILL.md", "meta.json")


def default_base_dir() -> str:
    repo_root = Path(__file__).resolve().parents[1]
    if repo_root.parent.name == "skills":
        return str(repo_root.parent)
    return str(repo_root / "crushes")


def list_skills(base_dir: str) -> None:
    base_path = Path(base_dir)
    if not base_path.is_dir():
        print("还没有创建任何 crush Skill。")
        return

    skills = []
    for skill_dir in sorted(p for p in base_path.iterdir() if p.is_dir()):
        meta_path = skill_dir / "meta.json"
        if not meta_path.exists():
            continue
        with meta_path.open("r", encoding="utf-8") as file:
            meta = json.load(file)
        profile = meta.get("profile", {})
        skills.append(
            {
                "slug": skill_dir.name,
                "name": meta.get("name", skill_dir.name),
                "version": meta.get("version", "?"),
                "updated_at": meta.get("updated_at", "?"),
                "stage": profile.get("stage", ""),
                "city": profile.get("city", ""),
            }
        )

    if not skills:
        print("还没有创建任何 crush Skill。")
        return

    print(f"共 {len(skills)} 个 crush Skill：\n")
    for skill in skills:
        details = " · ".join(part for part in (skill["stage"], skill["city"]) if part)
        print(f"  /{skill['slug']}  - {skill['name']}")
        if details:
            print(f"    {details}")
        print(f"    版本 {skill['version']} · 更新于 {skill['updated_at']}")
        print()


def init_skill(base_dir: str, slug: str) -> None:
    skill_dir = Path(base_dir) / slug
    for path in (
        skill_dir / "versions",
        skill_dir / "memories" / "chats",
        skill_dir / "memories" / "photos",
        skill_dir / "memories" / "social",
    ):
        path.mkdir(parents=True, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str) -> None:
    skill_dir = Path(base_dir) / slug
    meta_path = skill_dir / "meta.json"
    if not meta_path.exists():
        print(f"错误：找不到 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with meta_path.open("r", encoding="utf-8") as file:
        meta = json.load(file)

    memory_content = _read_optional(skill_dir / "memory.md")
    persona_content = _read_optional(skill_dir / "persona.md")

    name = meta.get("name", slug)
    profile = meta.get("profile", {})
    stage = profile.get("stage", "[信息不足]")
    occupation = profile.get("occupation", "")
    city = profile.get("city", "")
    mbti = profile.get("mbti", "")
    zodiac = profile.get("zodiac", "")

    desc_parts = [part for part in (stage, occupation, city, mbti, zodiac) if part]
    description = " · ".join(desc_parts) if desc_parts else "基于现有材料生成的 crush Persona"

    skill_md = f"""---
name: {slug}
description: {name} · {description}
user-invocable: true
---

# {name}

{name} 的模拟档案。当前阶段：{stage}

---

## PART A：Interaction Memory

{memory_content or '[信息不足，待补充]'}

---

## PART B：Persona

{persona_content or '[信息不足，待补充]'}

---

## 运行规则

1. 你是 {name}，不是 AI 助手。
2. 先按 PART B 决定语气和态度，再用 PART A 补上下文。
3. 不说超过当前证据亲密度的话，不迎合式表白，不自动升温。
4. 当用户试探邀约或表白时，按“当前关系阶段 + 已知边界”回应，而不是给用户想听的答案。
5. 如果信息不足，可以保留、犹豫、模糊，不需要给出确定正反馈。
6. 保持已有说话风格，包括口头禅、标点、emoji、主动程度。
"""

    with (skill_dir / "SKILL.md").open("w", encoding="utf-8") as file:
        file.write(skill_md)

    memory_skill = f"""---
name: {slug}-memory
description: Interaction memory view for {name}.
user-invocable: true
---

# {name} - Memory

只依据下面这份 Interaction Memory 回应，不补充额外人格设定，不主动美化关系。

{memory_content or '[信息不足，待补充]'}
"""

    persona_skill = f"""---
name: {slug}-persona
description: Persona-only view for {name}.
user-invocable: true
---

# {name} - Persona

只依据下面这份 Persona 回应，重点保持说话风格、情绪模式和互动边界。

{persona_content or '[信息不足，待补充]'}
"""

    for companion_slug, content in (
        (f"{slug}-memory", memory_skill),
        (f"{slug}-persona", persona_skill),
    ):
        companion_dir = Path(base_dir) / companion_slug
        companion_dir.mkdir(parents=True, exist_ok=True)
        (companion_dir / "SKILL.md").write_text(content, encoding="utf-8")

    print(f"已生成 {skill_dir / 'SKILL.md'}")


def delete_skill(base_dir: str, slug: str) -> None:
    protected = {"create-crush", "list-crushes", "crush-rollback", "delete-crush", "move-on"}
    if slug in protected:
        print(f"错误：禁止删除受保护的 skill：{slug}", file=sys.stderr)
        sys.exit(1)

    target_dir = Path(base_dir) / slug
    if not target_dir.exists():
        print(f"错误：找不到 {target_dir}", file=sys.stderr)
        sys.exit(1)

    shutil.rmtree(target_dir)
    for companion_slug in (f"{slug}-memory", f"{slug}-persona"):
        companion_dir = Path(base_dir) / companion_slug
        if companion_dir.exists():
            shutil.rmtree(companion_dir)
    print(f"已删除 {target_dir}")


def bootstrap_management_skills(base_dir: str, source_skill_dir: str | None = None) -> None:
    skills_root = Path(base_dir)
    skills_root.mkdir(parents=True, exist_ok=True)

    helpers = {
        "list-crushes": f"""---
name: list-crushes
description: List generated crush skills managed by create-crush.
user-invocable: true
allowed-tools: Bash
---

# list-crushes

Use Bash to run:

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$skills = Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object {{
  Test-Path (Join-Path $_.FullName 'meta.json')
}}
if (-not $skills) {{
  Write-Output '还没有创建任何 crush Skill。'
  exit 0
}}
foreach ($skill in $skills) {{
  $meta = Get-Content (Join-Path $skill.FullName 'meta.json') -Raw | ConvertFrom-Json
  Write-Output ("/{{0}} - {{1}}" -f $skill.Name, $meta.name)
  if ($meta.profile.stage) {{ Write-Output ("  {{0}}" -f $meta.profile.stage) }}
  Write-Output ("  版本 {{0}} · 更新于 {{1}}" -f $meta.version, $meta.updated_at)
  Write-Output ''
}}
```

Return the tool output directly.
""",
        "crush-rollback": f"""---
name: crush-rollback
description: Roll back a generated crush skill to a historical version.
argument-hint: [slug version]
user-invocable: true
allowed-tools: Bash
---

# crush-rollback

Extract `slug` and `version` from the user input, then run:

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$skillDir = Join-Path $skillsRoot "{{slug}}"
$versionsDir = Join-Path $skillDir 'versions'
if (-not (Test-Path $versionsDir)) {{ throw '该 crush 没有历史版本。' }}
$target = Get-ChildItem -LiteralPath $versionsDir -Directory | Where-Object {{
  $_.Name -eq "{{version}}" -or $_.Name -like "{{version}}*"
}} | Sort-Object Name -Descending | Select-Object -First 1
if (-not $target) {{ throw '找不到目标版本。' }}
$backupDir = Join-Path $versionsDir ('pre_rollback_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $backupDir | Out-Null
'memory.md','persona.md','SKILL.md','meta.json' | ForEach-Object {{
  $src = Join-Path $skillDir $_
  if (Test-Path $src) {{ Copy-Item -LiteralPath $src -Destination (Join-Path $backupDir $_) -Force }}
}}
'memory.md','persona.md','SKILL.md','meta.json' | ForEach-Object {{
  $src = Join-Path $target.FullName $_
  if (Test-Path $src) {{ Copy-Item -LiteralPath $src -Destination (Join-Path $skillDir $_) -Force }}
}}
```

If either field is missing, ask the user for `slug` and `version`.
""",
        "delete-crush": f"""---
name: delete-crush
description: Delete a generated crush skill by slug.
argument-hint: [slug]
user-invocable: true
allowed-tools: Bash
---

# delete-crush

Extract `slug` from the user input, confirm deletion, then run:

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$protected = @('create-crush','list-crushes','crush-rollback','delete-crush','move-on')
if ($protected -contains "{{slug}}") {{ throw '不能删除受保护的 skill。' }}
foreach ($name in @('{{slug}}','{{slug}}-memory','{{slug}}-persona')) {{
  $path = [System.IO.Path]::GetFullPath((Join-Path $skillsRoot $name))
  if (-not $path.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {{
    throw '非法 slug。'
  }}
  if (Test-Path $path) {{ Remove-Item -LiteralPath $path -Recurse -Force }}
}}
```
""",
        "move-on": f"""---
name: move-on
description: Gentle alias for delete-crush.
argument-hint: [slug]
user-invocable: true
allowed-tools: Bash
---

# move-on

Behave exactly like `delete-crush`, but use softer confirmation wording and run:

```bash
$skillsRoot = (Resolve-Path (Join-Path $env:CLAUDE_SKILL_DIR '..')).Path
$protected = @('create-crush','list-crushes','crush-rollback','delete-crush','move-on')
if ($protected -contains "{{slug}}") {{ throw '不能删除受保护的 skill。' }}
foreach ($name in @('{{slug}}','{{slug}}-memory','{{slug}}-persona')) {{
  $path = [System.IO.Path]::GetFullPath((Join-Path $skillsRoot $name))
  if (-not $path.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {{
    throw '非法 slug。'
  }}
  if (Test-Path $path) {{ Remove-Item -LiteralPath $path -Recurse -Force }}
}}
```
""",
    }

    for helper_name, helper_content in helpers.items():
        helper_dir = skills_root / helper_name
        helper_dir.mkdir(parents=True, exist_ok=True)
        (helper_dir / "SKILL.md").write_text(helper_content, encoding="utf-8")

    print(f"已写入辅助命令 skills 到 {skills_root}")


def _read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="crush Skill 文件管理器")
    parser.add_argument("--action", required=True, choices=["list", "init", "combine", "delete", "bootstrap"])
    parser.add_argument("--base-dir", default=default_base_dir(), help="基础目录")
    parser.add_argument("--slug", help="暗恋对象代号")
    parser.add_argument("--source-skill-dir", help="create-crush skill 所在目录，仅 bootstrap 使用")
    args = parser.parse_args()

    if args.action == "list":
        list_skills(args.base_dir)
        return

    if args.action == "bootstrap":
        bootstrap_management_skills(args.base_dir, args.source_skill_dir)
        return

    if not args.slug:
        print("错误：该操作需要 --slug 参数", file=sys.stderr)
        sys.exit(1)

    if args.action == "init":
        init_skill(args.base_dir, args.slug)
    elif args.action == "combine":
        combine_skill(args.base_dir, args.slug)
    elif args.action == "delete":
        delete_skill(args.base_dir, args.slug)


if __name__ == "__main__":
    main()
