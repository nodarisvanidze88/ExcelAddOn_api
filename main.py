from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])