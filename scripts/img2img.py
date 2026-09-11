#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gpt-image2-skill · GPT-image-2 图生图 CLI（GeekNow API）
BYOK：key 仅从 GEEKNOW_API_KEY 环境变量或 config/api_key.json 读取，无硬编码。
调用：POST {API_BASE}/images/edits  (multipart/form-data，图片字段名 image)
"""
import argparse
import base64
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config_helper import get_key

API_BASE = "https://api.geeknow.ai/v1"
MODEL = "gpt-image-2"
VALID_SIZES = {"1024x1024", "1792x1024", "1024x1792"}
MIME = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}


def save_results(data: dict, output: str, n: int) -> None:
    items = data.get("data", [])
    if not items:
        print("[警告] 响应中无图片数据", file=sys.stderr)
        return
    base, ext = os.path.splitext(output)
    if not ext:
        ext = ".png"
    for i, it in enumerate(items):
        img = None
        if it.get("b64_json"):
            img = base64.b64decode(it["b64_json"])
        elif it.get("url"):
            try:
                r = requests.get(it["url"], timeout=60)
                if r.ok:
                    img = r.content
            except Exception as e:
                print(f"[警告] 下载 url 失败: {e}", file=sys.stderr)
        if img:
            fn = output if n == 1 else f"{base}-{i+1}{ext}"
            with open(fn, "wb") as f:
                f.write(img)
            print(f"[保存] {fn} ({len(img) / 1024:.0f} KB)")


def main() -> None:
    ap = argparse.ArgumentParser(description="GPT-image-2 图生图")
    ap.add_argument("--prompt", required=True, help="图生图提示词")
    ap.add_argument("--image", required=True, help="参考图路径")
    ap.add_argument("--size", default="1024x1024", help="尺寸: 1024x1024 | 1792x1024 | 1024x1792")
    ap.add_argument("--n", type=int, default=1, help="生成数量 (1-4)")
    ap.add_argument("--output", default="gpt2_img2img.png", help="输出路径")
    args = ap.parse_args()

    key = get_key()
    if not key:
        print(
            "ERROR: 未配置 GeekNow API Key。请按 SKILL.md 引导注册并配置 key：\n"
            "  python scripts/config_helper.py set <key>\n"
            "或设置环境变量 GEEKNOW_API_KEY。",
            file=sys.stderr,
        )
        sys.exit(2)

    if not os.path.exists(args.image):
        print(f"[错误] 参考图不存在: {args.image}", file=sys.stderr)
        sys.exit(1)

    if args.size not in VALID_SIZES:
        print(f"[提示] size={args.size} 非标准尺寸，GeekNow 会按比例缩放；标准值: {', '.join(sorted(VALID_SIZES))}")

    ext = os.path.splitext(args.image)[1].lower().lstrip(".")
    mime = MIME.get(ext, "image/png")
    with open(args.image, "rb") as f:
        img_bytes = f.read()
    fields = {"prompt": args.prompt, "model": MODEL, "n": str(args.n), "size": args.size}
    files = {"image": (os.path.basename(args.image), img_bytes, mime)}
    headers = {"Authorization": f"Bearer {key}"}

    print(f"[提交] 图生图（{args.size}，{args.n}张）...")
    t = time.time()
    try:
        resp = requests.post(f"{API_BASE}/images/edits", data=fields, files=files, headers=headers, timeout=300)
    except Exception as e:
        print(f"[错误] 请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    if not resp.ok:
        print(f"[错误] HTTP {resp.status_code}: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)
    save_results(resp.json(), args.output, args.n)
    print(f"[完成] 用时 {time.time() - t:.0f}s")


if __name__ == "__main__":
    main()
