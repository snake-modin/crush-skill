#!/usr/bin/env python3
"""QQ chat export parser for crush-skill."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


MSG_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)(?:\((\d+)\))?\s*$")


def parse_qq_txt(file_path: str, target_name: str) -> dict:
    messages = []
    current = None

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")
            match = MSG_PATTERN.match(line)
            if match:
                if current:
                    messages.append(current)
                timestamp, sender, _qq_number = match.groups()
                current = {"timestamp": timestamp, "sender": sender.strip(), "content": ""}
                continue
            if current is not None and line.strip() and not line.startswith("==="):
                current["content"] = f"{current['content']}\n{line}".strip()

    if current:
        messages.append(current)

    target_msgs = [msg for msg in messages if target_name in msg.get("sender", "")]
    return {
        "target_name": target_name,
        "total_messages": len(messages),
        "target_messages": len(target_msgs),
        "sample_messages": [msg.get("content", "") for msg in target_msgs[:50] if msg.get("content")],
    }


def parse_qq_mht(file_path: str, target_name: str) -> dict:
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    clean_text = re.sub(r"<[^>]+>", "\n", content)
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)
    return {
        "target_name": target_name,
        "format": "mht",
        "raw_text": clean_text[:20000],
        "note": "MHT 格式已提取为纯文本，建议人工复核。",
    }


def write_report(output: str, result: dict) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as file:
        file.write(f"# QQ 聊天记录分析 - {result['target_name']}\n\n")
        file.write(f"总消息数：{result.get('total_messages', 'N/A')}\n")
        file.write(f"ta 的消息数：{result.get('target_messages', 'N/A')}\n\n")
        if result.get("note"):
            file.write(f"备注：{result['note']}\n\n")

        samples = result.get("sample_messages", [])
        if samples:
            file.write("## 样本消息\n")
            for index, message in enumerate(samples, start=1):
                file.write(f"{index}. {message}\n")
        elif result.get("raw_text"):
            file.write("## 原始文本片段\n\n")
            file.write(result["raw_text"])


def main() -> None:
    parser = argparse.ArgumentParser(description="QQ 聊天记录解析器")
    parser.add_argument("--file", required=True, help="输入文件路径")
    parser.add_argument("--target", required=True, help="暗恋对象的名字或昵称")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    ext = Path(args.file).suffix.lower()
    result = parse_qq_mht(args.file, args.target) if ext in {".mht", ".mhtml"} else parse_qq_txt(args.file, args.target)
    write_report(args.output, result)
    print(f"分析完成，结果已写入 {args.output}")


if __name__ == "__main__":
    main()
