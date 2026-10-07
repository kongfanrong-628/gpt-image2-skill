# CROSSPLATFORM.md — 多主流 Agent 适配说明

> 目标：把「GeekNow GPT-image-2 生图方案」做成**多个主流 Agent 都能用**，而不是只活在 WorkBuddy 里。
>
> ⚠️ 诚实前提：一个 `SKILL.md` 是 WorkBuddy 私有格式，豆包 / 百度搭子等云平台**读不懂**。
> 真正可移植的是「通用分母」——**OpenAPI 规范 + BYOK 引导逻辑**——各平台再用自己的方式包一层。

## 通用分母（三件套，本仓库已提供）

| 文件 | 作用 | 谁吃 |
|---|---|---|
| `openapi.yaml` | GeekNow GPT-image-2 的 OpenAPI 3.0.3 规范（含两个接口 + bearerAuth） | 豆包 / Coze / 百度搭子 / Dify / 任何支持 OpenAPI 导入的插件系统 |
| `BYOK_PROMPT.md` | 平台无关的多轮引导 prompt（注册→拿Key→配置） | 任何 Agent 的系统提示词 / 插件描述 |
| `SKILL.md` + `scripts/` | WorkBuddy 原生实现（Python 脚本生图） | 仅 WorkBuddy |

## 各平台适配方式

### 1. WorkBuddy（已完整实现 ✅）
- 直接 `git clone` 到 `~/.workbuddy/skills/gpt-image2-skill`，重启即生效。
- Python 脚本本地运行，key 存 `GEEKNOW_API_KEY` 或 `config/api_key.json`。

### 2. 豆包 / Coze（字节系）
- 在「插件 / 工具」里选 **从 OpenAPI 导入**，上传 `openapi.yaml`。
- 鉴权选 `Bearer`，把用户的 Key 填进插件的 API Key 配置位（平台托管）。
- 把 `BYOK_PROMPT.md` 的引导逻辑写进 Bot 的「人设与回复逻辑」或插件描述。
- 生图结果（url 或 b64）由 Bot 回传 / 渲染。

### 3. 百度搭子（文心 / 千帆）
- 在「自定义 API / 工具」里粘贴 `openapi.yaml` 内容或手动填两个接口。
- 图生图注意 `multipart/form-data` 的 `image` 字段——部分平台需显式声明文件上传组件。
- BYOK 引导逻辑写进智能体提示词。

### 4. Dify
- 「工具 → 自定义工具」支持 OpenAPI / 直接填 URL + 鉴权头。
- 导入 `openapi.yaml` 后，在工具参数里把 `Authorization: Bearer {{key}}` 绑定到用户变量。
- 把 `BYOK_PROMPT.md` 作为工具的前置说明。

### 5. 其他支持 OpenAPI 的 Agent
- 通用做法：导入 `openapi.yaml` + 在鉴权配置填用户 Key + 嵌入 `BYOK_PROMPT.md`。

## 硬约束（跨平台都必须守）

1. **绝不硬编码 Key**：任何平台的实现里都不出现 `sk-` 开头字符串。Key 只来自用户粘贴 / 平台安全配置位。
2. **必须 BYOK**：这是付费 API（约 ¥0.04/张），无 Key 不能生图；引导用户自备并充值。
3. **图片字段名固定 `image`**：图生图接口 multipart 字段名是 `image`，少写平台会报 400。
4. **尺寸只用标准三档**：1024x1024 / 1792x1024 / 1024x1792；非标准会被按比例缩放。
5. **注册网址（邀请链接）**：本仓库统一使用 `https://hk.geeknow.ai/register?aff=mD63`（带推广码 `mD63`，用户从此注册你拿返佣），API 文档见 `docs.geeknow.top`。

## 我（Claw）已验证 / 未验证

- ✅ 已验证：WorkBuddy 原生 skill 可推送、可安装、无个人 key 泄漏、Python 脚本独立可跑。
- ⚠️ 未验证（红队提醒）：豆包 / 百度搭子 / Coze / Dify 的后台我**无法实测**，上述是「按平台公开文档的适配路径」，不是「跑通截图」。你在这些平台导入后，第一次生图务必用 1 张测试图确认对接成功。
- ✅ 注册网址已核实：`https://hk.geeknow.ai/register?aff=mD63`（导演下发的最新邀请链接，含推广码 `mD63`）。

## 仓库结构

```
gpt-image2-skill/
├── SKILL.md            # WorkBuddy 原生定义
├── openapi.yaml        # 通用分母：API 规范（跨平台）
├── BYOK_PROMPT.md      # 通用分母：多轮引导 prompt（跨平台）
├── CROSSPLATFORM.md    # 本文件
├── README.md           # 安装 + 用法
├── manifest.yaml
├── LICENSE             # MIT © 孔不惑AIko
├── scripts/            # WorkBuddy 用 Python 脚本（txt2img / img2img / config_helper）
├── references/
└── .gitignore          # 排除 config/（key 永不上传）
```

落款：孔不惑AIko
