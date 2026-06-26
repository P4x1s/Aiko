# 艾柯 (Aiko) API 中转站

统一的 AI API 中转站，让国内开发者轻松调用 OpenAI、Anthropic、Google 等多个厂商的模型。

## 解决的痛点

- **支付门槛** - 无需海外信用卡，支持支付宝、微信支付
- **网络延迟** - 海外服务器部署，国内直连稳定快速
- **多平台管理** - 一个接口调用所有模型，统一管理

## 功能特性

- OpenAI 兼容 API 格式
- 支持 OpenAI、Anthropic、Google 等多个 AI 厂商
- 流式响应 (SSE) 支持
- Supabase 用户认证
- Vercel 部署

## 快速开始

1. 克隆仓库
2. 复制 `backend/.env.example` 到 `backend/.env` 并填入你的 API Key
3. 部署到 Vercel，Root Directory 设置为 `backend`

## API 使用

```bash
curl https://your-app.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "你好!"}]
  }'
```

## 支持的模型

| 厂商 | 模型 |
|------|------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku |
| Google | gemini-pro, gemini-1.5-pro, gemini-1.5-flash |

## 项目结构

```
ai-gateway/
├── backend/
│   ├── api/              # FastAPI 路由
│   ├── services/         # 业务逻辑
│   │   ├── providers/    # AI 厂商适配器
│   │   ├── auth.py       # 认证服务
│   │   └── database.py   # 数据库配置
│   └── vercel.json       # Vercel 部署配置
├── supabase/
│   └── migrations/       # 数据库迁移
└── README.md
```

## 部署

1. 在 [Vercel](https://vercel.com) 导入 GitHub 仓库
2. Root Directory 设置为 `backend`
3. 添加环境变量（参考 `.env.example`）
4. 在 [Supabase](https://supabase.com) 创建项目并运行迁移

## License

MIT
