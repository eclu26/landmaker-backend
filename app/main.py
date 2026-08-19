from fastapi import FastAPI

from app.routers import pages
from app.routers.api_v1 import projects

app = FastAPI(title="Лендмейкер Backend", version="1.0.0")

app.include_router(pages.router)

app.include_router(projects.router)

@app.get("/status")
async def status() -> dict:
    return {"status": "ok"}