from fastapi import FastAPI
from auth import routes as auth_routes
app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}



app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])