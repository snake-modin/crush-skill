#!/usr/bin/env python3
"""Social media directory scanner for crush-skill."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
TEXT_EXTS = {".txt", ".md", ".json", ".csv"}


def scan_directory(dir_path: str) -> dict:
    files = {"images": [], "texts": [], "other": []}
    for root, _dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            path = str(Path(root) / filename)
            ext = Path(filename).suffix.lower()
            if ext in IMAGE_EXTS:
                files["images"].append(path)
            elif ext in TEXT_EXTS:
                files["texts"].append(path)
            else:
                files["other"].append(path)
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description="社交媒体内容扫描器")
    parser.add_argument("--dir", required=True, help="截图或导出文件目录")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"错误：目录不存在 {args.dir}", file=sys.stderr)
        sys.exit(1)

    files = scan_directory(args.dir)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as file:
        file.write("# 社交媒体内容扫描结果\n\n")
        file.write(f"扫描目录：{args.dir}\n\n")
        file.write("## 文件统计\n")
        file.write(f"- 图片文件：{len(files['images'])} 个\n")
        file.write(f"- 文本文件：{len(files['texts'])} 个\n")
        file.write(f"- 其他文件：{len(files['other'])} 个\n\n")

        if files["images"]:
            file.write("## 图片列表\n")
            for image in sorted(files["images"]):
                file.write(f"- {image}\n")
            file.write("\n")

        if files["texts"]:
            file.write("## 文本内容\n")
            for text_file in sorted(files["texts"]):
                file.write(f"\n### {Path(text_file).name}\n")
                try:
                    content = Path(text_file).read_text(encoding="utf-8", errors="ignore")[:5000]
                    file.write(f"```\n{content}\n```\n")
                except OSError as error:
                    file.write(f"读取失败：{error}\n")

    print(f"扫描完成，结果已写入 {args.output}")
    print("提示：图片本身仍需由上层工具进一步查看。")


if __name__ == "__main__":
    main()
