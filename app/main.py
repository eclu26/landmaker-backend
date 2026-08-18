from fastapi import FastAPI

from app.routers import projects

app = FastAPI(title="Лендмейкер", version="1.0.0")

app.include_router(projects.router)

@app.get("/")
async def root() -> dict:
    return {"message": "You think you are not simple user, eh? This is MY API. You are not allowed to use it. Please, leave."}

@app.get("/status")
async def status() -> dict:
    return {"status": "ok"}