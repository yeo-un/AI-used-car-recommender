from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.recommend import router as recommend_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Used Car Recommender",
        description="AI-powered used car recommendation service",
        version="0.1.0",
    )

    # CORS 설정 (Streamlit 연동 대비)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # MVP 단계에서는 전체 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(recommend_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "AI Used Car Recommender API is running"}

    return app


app = create_app()
