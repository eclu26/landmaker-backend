from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pages
from app.routers.api_v1 import projects, users

app = FastAPI(title="Лендмейкер Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages.router)

app.include_router(projects.router)
app.include_router(users.router)

@app.get("/status")
async def status() -> dict:
    return {"status": "ok"}