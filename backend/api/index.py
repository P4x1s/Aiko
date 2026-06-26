from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import routes as v1_routes

app = FastAPI(
    title="AI Gateway",
    description="Unified AI API proxy for Chinese developers",
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


@app.get("/health")
async def health():
    return {"status": "ok"}
