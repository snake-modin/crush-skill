#!/usr/bin/env python3
"""Photo EXIF analyzer for crush-skill."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import GPSTAGS, TAGS
    HAS_PIL = True
except ImportError:  # pragma: no cover
    HAS_PIL = False


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}


def get_exif_data(image_path: str) -> dict:
    if not HAS_PIL:
        return {"file": Path(image_path).name, "error": "Pillow 未安装，无法读取 EXIF。"}

    try:
        image = Image.open(image_path)
        raw_exif = image._getexif()
        if not raw_exif:
            return {"file": Path(image_path).name}

        exif = {TAGS.get(tag_id, tag_id): value for tag_id, value in raw_exif.items()}
        result = {"file": Path(image_path).name, "path": image_path}

        date_taken = exif.get("DateTimeOriginal") or exif.get("DateTime")
        if date_taken:
            result["date_taken"] = str(date_taken)

        gps_info = exif.get("GPSInfo")
        if gps_info:
            gps_data = {GPSTAGS.get(key, key): value for key, value in gps_info.items()}
            if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                lat = _convert_to_degrees(gps_data["GPSLatitude"])
                lon = _convert_to_degrees(gps_data["GPSLongitude"])
                if gps_data.get("GPSLatitudeRef") == "S":
                    lat = -lat
                if gps_data.get("GPSLongitudeRef") == "W":
                    lon = -lon
                result["gps"] = {"lat": lat, "lon": lon}
        return result
    except Exception as error:  # pragma: no cover
        return {"file": Path(image_path).name, "error": str(error)}


def _convert_to_degrees(value) -> float:
    degrees, minutes, seconds = value
    return float(degrees) + float(minutes) / 60 + float(seconds) / 3600


def main() -> None:
    parser = argparse.ArgumentParser(description="照片元信息分析器")
    parser.add_argument("--dir", required=True, help="照片目录")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"错误：目录不存在 {args.dir}", file=sys.stderr)
        sys.exit(1)

    photos = []
    for root, _dirs, files in os.walk(args.dir):
        for filename in sorted(files):
            if Path(filename).suffix.lower() in IMAGE_EXTS:
                photos.append(get_exif_data(str(Path(root) / filename)))

    dated = sorted((photo for photo in photos if photo.get("date_taken")), key=lambda item: item["date_taken"])
    undated = [photo for photo in photos if not photo.get("date_taken")]

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as file:
        file.write("# 照片时间线分析\n\n")
        file.write(f"扫描目录：{args.dir}\n")
        file.write(f"总照片数：{len(photos)}\n")
        file.write(f"有时间信息：{len(dated)}\n")
        file.write(f"有 GPS 信息：{len([photo for photo in photos if photo.get('gps')])}\n\n")

        if dated:
            file.write("## 时间线\n")
            for photo in dated:
                line = f"- {photo['date_taken'][:10]} · {photo['file']}"
                if photo.get("gps"):
                    line += f" (GPS: {photo['gps']['lat']:.4f}, {photo['gps']['lon']:.4f})"
                file.write(line + "\n")
            file.write("\n")

        if undated:
            file.write("## 无时间信息的照片\n")
            for photo in undated:
                file.write(f"- {photo['file']}\n")
            file.write("\n")

        if not HAS_PIL:
            file.write("提示：未安装 Pillow，因此无法读取 EXIF。可执行 `pip3 install Pillow`。\n")

    print(f"分析完成，结果已写入 {args.output}")


if __name__ == "__main__":
    main()
