# GPT-image-2 API 调用说明（GeekNow）

本 skill 调用的生图能力由 GeekNow 聚合 API 提供，**不是** DeepSeek 文本 LLM，鉴权与计费完全独立。

## 基础信息
- Base URL：`https://api.geeknow.ai/v1`
- 模型名：`gpt-image-2`（固定）
- 鉴权：`Authorization: Bearer <你的GeekNowKey>`
- 计费：**付费，约 ¥0.04/张**（以 GeekNow 官网实时政策为准），需充值 credits

## 文生图（Text-to-Image）
`POST {base}/images/generations`，`Content-Type: application/json`

请求体：
```json
{
  "model": "gpt-image-2",
  "prompt": "描述",
  "n": 1,
  "size": "1024x1024"
}
```
响应：
```json
{ "data": [ { "url": "https://..." } ] }
```
或 `b64_json` 形式（脚本都会自动处理）。

## 图生图（Image-to-Image）
`POST {base}/images/edits`，`multipart/form-data`

| 字段 | 说明 |
|---|---|
| `image` | 参考图文件（字段名固定为 `image`） |
| `prompt` | 提示词 |
| `model` | `gpt-image-2` |
| `n` | 数量 |
| `size` | 尺寸 |

同步模式（不加 `?async=true`）。

## 尺寸说明（怪癖）
标准尺寸：`1024x1024` / `1792x1024`(16:9) / `1024x1792`(9:16)。
实测中 **gpt-image-2 不完全支持自定义尺寸**，传入非标准尺寸会被**按比例缩放**，属正常现象。

## Key 配置（BYOK）
优先级：`GEEKNOW_API_KEY` 环境变量 > `config/api_key.json`（gitignore 排除）。
无任何硬编码 key 进入仓库。

## 注册 / 控制台
- 官网 / 注册：https://geeknow.ai （以 `docs.geeknow.top` 实时地址为准）
- API 文档：https://docs.geeknow.top/api-reference/images/gpt-image-2/generation
