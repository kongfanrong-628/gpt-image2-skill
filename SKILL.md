---
name: gpt-image2-skill
description: 通过 GeekNow 聚合 API 调用 GPT-image-2 模型进行文生图与图生图。触发词：gpt-image-2、GPT-image-2、文生图、图生图、txt2img、img2img、AI生图、配图、GPT生图、生成封面。当用户要求"用 GPT 生成图片 / 做张配图 / 生成封面 / 参考图生图"时使用。该 skill 采用 BYOK（用户自带 GeekNow API Key），首次使用若未配置 key，需多轮引导用户去 GeekNow 注册、获取并配置 API Key（付费 API，约 ¥0.04/张，需充值 credits）。
version: 1.0.0
author: 孔不惑AIko
license: MIT
homepage: https://github.com/kongfanrong-628/gpt-image2-skill
agent_created: true
---

# gpt-image2-skill

用 GeekNow 提供的 **GPT-image-2** 模型做文生图 / 图生图。纯 BYOK，skill 内**不内置任何 key**。

## 调用契约（实现细节，AI 不必改）
- Base：`https://api.geeknow.ai/v1`，模型名固定 `gpt-image-2`
- 文生图：`POST /images/generations`（JSON body）
- 图生图：`POST /images/edits`（`multipart/form-data`，图片字段名 `image`）
- 鉴权：`Authorization: Bearer <key>`
- 响应：`{"data":[{"url":"..."}]}` 或 `{"data":[{"b64_json":"..."}]}`，脚本自动下载/解码写盘
- 详见 `references/api-notes.md`

## 多轮对话引导（首次 / 未配置 key 时必走）
生图前先检测 key：
```
python scripts/config_helper.py get
```
- 输出「已配置」→ 直接生图。
- 输出「未配置」→ **不要**硬编码或编造 key，进入下面引导：

1. 告诉用户：GPT-image-2 由 GeekNow 提供，是**付费 API（约 ¥0.04/张）**，需自备 key 并**充值 credits**；本 skill 不内置 key。
2. 给注册 / 控制台入口：👉 https://geeknow.ai （以官方 `docs.geeknow.top` 实时地址为准；若官网变更，以官网为准）。
3. 引导：注册 GeekNow 账号 → 控制台创建 API Key → **充值 credits** → 把 Key 复制发给我。
4. 用户回贴 key 后，执行：
   ```
   python scripts/config_helper.py set "<用户粘贴的key>"
   ```
   key 只存到本 skill 的 `config/api_key.json`（已被 `.gitignore` 排除，绝不上传仓库）。也可引导用户改设环境变量 `GEEKNOW_API_KEY`。
5. 可选：生成 1 张测试图确认对接成功，再进入正式生图。

## 生图用法（直接给可运行命令）
文生图：
```
python scripts/txt2img.py --prompt "一只赛博朋克风格的小猫, 霓虹光, 电影质感" --size 1024x1024 --output out.png
```
图生图：
```
python scripts/img2img.py --prompt "保持角色, 换成正午阳光场景" --image ref.jpg --size 1024x1024 --output out.png
```
参数：`--prompt`(必填) `--size`(1024x1024|1792x1024|1024x1792) `--n`(1-4) `--output`。

## 安全约束（红线）
- 绝不把 key 打印到聊天、写入会被提交的文件；`config/api_key.json` 已被 `.gitignore` 排除。
- 脚本内无任何硬编码 key；key 仅来自 `GEEKNOW_API_KEY` 环境变量或 `config/api_key.json`。
