#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gpt-image2-skill · 本地密钥安全存取（BYOK）
- 密钥只存到本 skill 的 config/api_key.json（已被 .gitignore 排除，绝不上传仓库）
- 读取优先级：环境变量 GEEKNOW_API_KEY > config/api_key.json
- 本文件不含任何硬编码 key
"""
import os
import sys
import json

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "api_key.json")


def save_key(key: str) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"api_key": key}, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass
    print(f"已保存 API Key 到 {CONFIG_FILE}")
    print("该文件已被 .gitignore 排除，不会随仓库上传。")


def get_key() -> str:
    # 1) 环境变量优先
    k = (os.environ.get("GEEKNOW_API_KEY") or "").strip()
    if k:
        return k
    # 2) 本地 config/api_key.json
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return (json.load(f).get("api_key") or "").strip()
    except Exception:
        return ""


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "set":
        save_key(sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == "get":
        print("已配置" if get_key() else "未配置")
    else:
        print("用法: python config_helper.py set <key> | get")
