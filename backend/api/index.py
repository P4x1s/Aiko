from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import routes as v1_routes
from api.billing_routes import router as billing_router

app = FastAPI(
    title="艾柯 (Aiko) API 中转站",
    description="统一的 AI API 中转站，让国内开发者轻松调用多个厂商的模型",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_routes.router)
app.include_router(billing_router)


@app.get("/")
async def root():
    return {
        "name": "艾柯 (Aiko) API 中转站",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "billing": "/api/billing/*",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
