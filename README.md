# gpt-image2-skill

通过 [GeekNow](https://geeknow.ai) 聚合 API 调用 **GPT-image-2** 模型做文生图 / 图生图的 WorkBuddy skill。
纯 BYOK（Bring Your Own Key），skill 内**不含任何密钥**，任何人安装后自备 GeekNow Key 即可用。

> ⚠️ GPT-image-2 是**付费 API（约 ¥0.04/张）**，需注册 GeekNow 账号、创建 API Key 并**充值 credits** 后才能生图。

## 安装（一条命令）

```bash
git clone https://github.com/<owner>/gpt-image2-skill.git ~/.workbuddy/skills/gpt-image2-skill
```

装完重启 / 刷新 WorkBuddy，首次对话会引导你注册并配置 key。

> 依赖 Python + `requests`：`pip install requests`

## 首次使用（多轮对话引导）

1. 直接说"用 gpt-image-2 给我生张图"，AI 检测到你没配 key，会给你注册网址。
2. 去 https://geeknow.ai 注册 → 控制台创建 API Key → **充值 credits** → 把 Key 发回给 AI。
3. AI 把 Key 存到本 skill 的 `config/api_key.json`（已被 `.gitignore` 排除，绝不上传）。
4. 之后正常生图即可。

也可手动配置环境变量 `GEEKNOW_API_KEY`（把你的 GeekNow Key 赋值给它即可，优先级最高）。

## 用法

文生图：
```bash
python ~/.workbuddy/skills/gpt-image2-skill/scripts/txt2img.py \
  --prompt "一只赛博朋克风格的小猫, 霓虹光, 电影质感" \
  --size 1024x1024 --output out.png
```

图生图：
```bash
python ~/.workbuddy/skills/gpt-image2-skill/scripts/img2img.py \
  --prompt "保持角色, 换成正午阳光场景" \
  --image ref.jpg --size 1024x1024 --output out.png
```

参数：`--prompt`(必填) `--size`(1024x1024|1792x1024|1024x1792) `--n`(1-4) `--output`

## 安全说明
- 密钥只存在本地 `config/api_key.json`（gitignore 排除）或环境变量，**不会**进入仓库。
- 脚本内无任何硬编码密钥。

## License
MIT © 孔不惑AIko
