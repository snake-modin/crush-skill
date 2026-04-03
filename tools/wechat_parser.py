#!/usr/bin/env python3
"""WeChat chat export parser for crush-skill.

Supports plain text, simple JSON exports, and manual paste logs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


TIMESTAMP_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)$")
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001FAFF\u2600-\u27BF]+",
    re.UNICODE,
)


def detect_format(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".json":
        return "json"
    if ext in {".txt", ".md"}:
        sample = Path(file_path).read_text(encoding="utf-8", errors="ignore")[:2000]
        if TIMESTAMP_PATTERN.search(sample):
            return "wechatmsg_txt"
        return "plaintext"
    return "plaintext"


def parse_wechatmsg_txt(file_path: str, target_name: str) -> dict:
    messages = []
    current = None

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")
            match = TIMESTAMP_PATTERN.match(line)
            if match:
                if current:
                    messages.append(current)
                timestamp, sender = match.groups()
                current = {"timestamp": timestamp, "sender": sender.strip(), "content": ""}
                continue
            if current is not None and line.strip():
                current["content"] = f"{current['content']}\n{line}".strip()

    if current:
        messages.append(current)

    return analyze_messages(messages, target_name)


def parse_json(file_path: str, target_name: str) -> dict:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        data = json.load(file)

    raw_messages = data if isinstance(data, list) else data.get("messages", data.get("data", []))
    messages = []
    for item in raw_messages:
        messages.append(
            {
                "timestamp": item.get("time", item.get("timestamp", "")),
                "sender": item.get("sender", item.get("nickname", item.get("from", ""))),
                "content": item.get("content", item.get("message", item.get("text", ""))),
            }
        )

    return analyze_messages(messages, target_name)


def parse_plaintext(file_path: str, target_name: str) -> dict:
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    return {
        "target_name": target_name,
        "total_messages": 0,
        "target_messages": 0,
        "analysis": {"note": "纯文本材料，建议结合人工判断。"},
        "sample_messages": [],
        "raw_text": content[:10000],
    }


def analyze_messages(messages: list[dict], target_name: str) -> dict:
    target_msgs = [msg for msg in messages if target_name in msg.get("sender", "")]
    all_target_text = " ".join(msg.get("content", "") for msg in target_msgs)
    emojis = EMOJI_PATTERN.findall(all_target_text)
    emoji_freq = _top_counts(emojis)

    particles = re.findall(r"[哈啊呢吧嘛呀啦哦嗯哼]+", all_target_text)
    particle_freq = _top_counts(particles)
    msg_lengths = [len(msg.get("content", "")) for msg in target_msgs if msg.get("content")]
    avg_length = round(sum(msg_lengths) / len(msg_lengths), 1) if msg_lengths else 0

    return {
        "target_name": target_name,
        "total_messages": len(messages),
        "target_messages": len(target_msgs),
        "analysis": {
            "top_particles": particle_freq,
            "top_emojis": emoji_freq,
            "avg_message_length": avg_length,
            "message_style": "short_burst" if avg_length and avg_length < 20 else "long_form",
        },
        "sample_messages": [msg.get("content", "") for msg in target_msgs[:50] if msg.get("content")],
    }


def _top_counts(items: list[str], limit: int = 10) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:limit]


def write_report(output: str, source_file: str, fmt: str, result: dict) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as file:
        file.write(f"# 微信聊天记录分析 - {result['target_name']}\n\n")
        file.write(f"来源文件：{source_file}\n")
        file.write(f"检测格式：{fmt}\n")
        file.write(f"总消息数：{result.get('total_messages', 0)}\n")
        file.write(f"ta 的消息数：{result.get('target_messages', 0)}\n\n")

        analysis = result.get("analysis", {})
        if analysis.get("note"):
            file.write(f"备注：{analysis['note']}\n\n")
        if analysis.get("top_particles"):
            file.write("## 高频语气词\n")
            for word, count in analysis["top_particles"]:
                file.write(f"- {word}: {count} 次\n")
            file.write("\n")
        if analysis.get("top_emojis"):
            file.write("## 高频 Emoji\n")
            for emoji, count in analysis["top_emojis"]:
                file.write(f"- {emoji}: {count} 次\n")
            file.write("\n")
        if analysis.get("avg_message_length") is not None:
            style = "短句连发型" if analysis.get("message_style") == "short_burst" else "长段落型"
            file.write("## 消息风格\n")
            file.write(f"- 平均消息长度：{analysis.get('avg_message_length', 0)} 字\n")
            file.write(f"- 风格：{style}\n\n")

        samples = result.get("sample_messages", [])
        if samples:
            file.write("## 样本消息\n")
            for index, message in enumerate(samples, start=1):
                file.write(f"{index}. {message}\n")
        elif result.get("raw_text"):
            file.write("## 原始文本片段\n\n")
            file.write(result["raw_text"])


def main() -> None:
    parser = argparse.ArgumentParser(description="微信聊天记录解析器")
    parser.add_argument("--file", required=True, help="输入文件路径")
    parser.add_argument("--target", required=True, help="暗恋对象的名字或昵称")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--format", default="auto", help="文件格式：auto / wechatmsg_txt / json / plaintext")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    fmt = detect_format(args.file) if args.format == "auto" else args.format
    if fmt == "wechatmsg_txt":
        result = parse_wechatmsg_txt(args.file, args.target)
    elif fmt == "json":
        result = parse_json(args.file, args.target)
    else:
        result = parse_plaintext(args.file, args.target)

    write_report(args.output, args.file, fmt, result)
    print(f"分析完成，结果已写入 {args.output}")


if __name__ == "__main__":
    main()
