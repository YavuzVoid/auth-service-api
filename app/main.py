from fastapi import FastAPI
from app.database import engine, Base
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service API",
    description="JWT tabanlı kimlik doğrulama ve yetkilendirme servisi",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
