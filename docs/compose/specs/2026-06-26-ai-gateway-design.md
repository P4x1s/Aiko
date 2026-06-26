# AI Gateway - API Proxy Platform Design

## [S1] Problem

Chinese developers face three pain points when using AI APIs:

1. **Payment barriers** - Most international AI providers require overseas credit cards, which are difficult for Chinese developers to obtain
2. **Network latency** - Direct connections from mainland China to overseas AI providers suffer from high latency and instability
3. **Multi-platform management** - Each AI provider requires separate registration, API key management, and account top-ups

## [S2] Solution Overview

Build a unified AI API gateway that:

- Exposes an OpenAI-compatible API format, so existing applications can switch providers with minimal code changes
- Routes requests to multiple AI providers through a single interface
- Handles payment via Alipay, WeChat Pay, and cryptocurrency
- Deploys on Vercel for serverless scalability
- Uses Supabase for authentication and database
- Provides admin dashboard for user management and system monitoring

## [S3] Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Backend | Python (FastAPI) | Async performance, rich ecosystem, strong for API services |
| Frontend | Vue.js (Nuxt) | Modern framework, native Vercel deployment |
| Database | Supabase (PostgreSQL) | Managed PostgreSQL, built-in auth, real-time |
| Cache | In-memory + Supabase | Simple caching for rate limiting, no external service needed |
| Deployment | Vercel | Serverless, free tier, GitHub integration |
| Version Control | GitHub | Industry standard, Vercel integration |
| Architecture | Modular monolith | Clear boundaries, easy to split later if needed |

## [S4] Core Modules

### 4.1 Proxy Module

- Request routing based on model name or provider selection
- OpenAI-compatible API format (`/v1/chat/completions`, `/v1/models`, etc.)
- Load balancing across multiple API keys per provider
- Request/response transformation for non-OpenAI providers
- Streaming support (SSE)

### 4.2 Provider Adapters

Each provider implements a unified interface:

```python
class ProviderAdapter(ABC):
    @abstractmethod
    async def chat_completion(self, request: ChatRequest) -> ChatResponse: ...

    @abstractmethod
    async def chat_completion_stream(self, request: ChatRequest) -> AsyncIterator[Chunk]: ...

    @abstractmethod
    def count_tokens(self, messages: list[Message]) -> int: ...
```

**Supported Providers:**

| Provider | Models | API Format |
|----------|--------|------------|
| OpenAI | GPT-4o, GPT-4, GPT-3.5-turbo | Native |
| Anthropic | Claude 3.5 Sonnet, Claude 3 Opus | Custom |
| Google | Gemini 1.5 Pro, Gemini 1.5 Flash | Custom |
| Baidu | ERNIE 4.0, ERNIE 3.5 | Custom |
| Alibaba | Qwen-Max, Qwen-Plus | Custom |
| Zhipu | GLM-4, GLM-3-Turbo | Custom |
| DeepSeek | DeepSeek-V2, DeepSeek-Chat | OpenAI-compatible |

### 4.3 Auth Module (Supabase Auth)

- User registration and login via Supabase Auth
- Email + password authentication
- Social login (GitHub, Google) via Supabase
- JWT token verification in FastAPI
- API key management (stored in Supabase)

### 4.4 Billing Module

- Token counting per request
- Balance management (prepaid credits)
- Pricing configuration per model
- Payment integration (Alipay, WeChat Pay, Crypto)
- Usage history and invoices

### 4.5 Admin Module

- User management (list, suspend, delete)
- Provider key management
- System monitoring (request volume, error rates, latency)
- Configuration management (pricing, rate limits)

## [S5] Data Models (Supabase)

### User (Supabase Auth)
Supabase handles user authentication automatically. Custom user data stored in `profiles` table.

```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    balance DECIMAL(10,4) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### API Key
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(8) NOT NULL,
    name VARCHAR(100),
    rate_limit INTEGER DEFAULT 60,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP
);
```

### Request Log
```sql
CREATE TABLE request_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id),
    api_key_id UUID REFERENCES api_keys(id),
    provider VARCHAR(50),
    model VARCHAR(100),
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost DECIMAL(10,6),
    latency_ms INTEGER,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Transaction
```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id),
    type VARCHAR(20), -- 'payment', 'usage', 'refund'
    amount DECIMAL(10,4),
    balance_after DECIMAL(10,4),
    description TEXT,
    payment_method VARCHAR(50),
    payment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## [S6] API Design

### Proxy Endpoints (OpenAI-compatible)

```
POST /v1/chat/completions
GET  /v1/models
```

### Auth Endpoints (via Supabase)

```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### API Key Endpoints

```
GET    /api/keys
POST   /api/keys
DELETE /api/keys/{key_id}
```

### Billing Endpoints

```
GET  /api/billing/balance
GET  /api/billing/history
POST /api/billing/recharge
```

### Admin Endpoints

```
GET    /api/admin/users
GET    /api/admin/requests
GET    /api/admin/stats
PUT    /api/admin/config
```

## [S7] Project Structure

```
ai-gateway/
├── backend/
│   ├── api/                    # Vercel serverless functions
│   │   ├── index.py           # Main FastAPI app
│   │   ├── auth/
│   │   │   └── [...slug].py   # Auth endpoints
│   │   ├── keys/
│   │   │   └── [...slug].py   # API key endpoints
│   │   ├── billing/
│   │   │   └── [...slug].py   # Billing endpoints
│   │   ├── admin/
│   │   │   └── [...slug].py   # Admin endpoints
│   │   └── v1/
│   │       └── [...slug].py   # Proxy endpoints (/v1/*)
│   ├── services/
│   │   ├── providers/
│   │   │   ├── base.py        # Abstract provider interface
│   │   │   ├── openai.py      # OpenAI adapter
│   │   │   ├── anthropic.py   # Anthropic adapter
│   │   │   ├── google.py      # Google adapter
│   │   │   ├── baidu.py       # Baidu adapter
│   │   │   ├── alibaba.py     # Alibaba adapter
│   │   │   ├── zhipu.py       # Zhipu adapter
│   │   │   └── deepseek.py    # DeepSeek adapter
│   │   ├── auth.py            # Supabase auth service
│   │   ├── database.py        # Supabase client
│   │   └── token_counter.py   # Token counting
│   ├── tests/
│   │   ├── test_proxy.py
│   │   └── test_providers/
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env.example
├── frontend/
│   ├── pages/
│   │   ├── index.vue
│   │   ├── login.vue
│   │   ├── register.vue
│   │   ├── dashboard/
│   │   │   ├── index.vue
│   │   │   ├── keys.vue
│   │   │   └── billing.vue
│   │   └── admin/
│   │       ├── index.vue
│   │       ├── users.vue
│   │       └── settings.vue
│   ├── components/
│   ├── composables/
│   ├── layouts/
│   ├── nuxt.config.ts
│   ├── package.json
│   └── .env.example
├── supabase/
│   ├── migrations/
│   │   └── 001_initial.sql
│   └── seed.sql
├── .gitignore
├── README.md
└── docs/
    └── compose/specs/
```

## [S8] Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GitHub                               │
│                   (Source Control)                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        Vercel                                │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │   Frontend (Nuxt)    │  │   Backend (FastAPI)  │        │
│  │   Static + SSR       │  │   Serverless Functions│        │
│  └──────────────────────┘  └──────────────────────┘        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Supabase                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL   │  │  Auth        │  │  Realtime    │      │
│  │  Database     │  │  (JWT)       │  │  (optional)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI Providers                               │
│  OpenAI | Anthropic | Google | Baidu | Alibaba | Zhipu     │
└─────────────────────────────────────────────────────────────┘
```

**Deployment Flow:**
1. Code pushed to GitHub
2. Vercel auto-deploys frontend and backend
3. Supabase handles database and authentication
4. Backend routes requests to AI providers

## [S9] Phased Implementation

### Phase 1: Core Proxy + Provider Adapters
- OpenAI-compatible API endpoints
- Provider adapters for OpenAI, Anthropic, Google
- Basic API key authentication
- Vercel deployment setup

### Phase 2: Supabase Integration
- Supabase project setup
- User registration and login
- API key management
- Profile data storage

### Phase 3: Billing System
- Token counting and cost calculation
- Balance management
- Payment integration (Alipay, WeChat Pay, Crypto)

### Phase 4: Chinese Providers
- Baidu ERNIE adapter
- Alibaba Tongyi adapter
- Zhipu GLM adapter
- DeepSeek adapter

### Phase 5: Admin Dashboard
- User management UI
- System monitoring
- Configuration management

## [S10] Success Criteria

1. Single API endpoint can route to any supported provider
2. OpenAI-compatible format allows drop-in replacement
3. Chinese developers can pay via Alipay/WeChat Pay
4. API latency from China < 500ms (p95)
5. Admin can manage users, keys, and billing
6. Deployed on Vercel with GitHub integration
7. User data stored in Supabase
