#!/usr/bin/env bash
# gpt-image2-skill 安装依赖（可选，仅首次需要）
# 生图脚本依赖 requests；本脚本帮你装好。
set -e
echo "[gpt-image2-skill] 安装依赖 requests ..."
python -m pip install --quiet requests 2>/dev/null || pip install requests
echo "[gpt-image2-skill] 依赖就绪。"
echo "首次生图前请按 SKILL.md 引导配置 GeekNow API Key（付费，约 ¥0.04/张）。"
