from fastapi import FastAPI

app = FastAPI(title="Лендмейкер", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "You think you are not simple user, eh? This is MY API. You are not allowed to use it. Please, leave."}

@app.get("/status")
async def status():
    return {"status": "ok"}