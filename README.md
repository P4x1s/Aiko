# AI Gateway

Unified AI API proxy for Chinese developers. Access OpenAI, Anthropic, Google, and more through a single OpenAI-compatible endpoint.

## Features

- OpenAI-compatible API format
- Support for multiple AI providers
- User authentication via Supabase
- Deployed on Vercel

## Quick Start

1. Clone the repository
2. Copy `backend/.env.example` to `backend/.env` and add your keys
3. Deploy to Vercel with the **Root Directory** set to `backend`

## API Usage

```bash
curl https://your-app.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```
