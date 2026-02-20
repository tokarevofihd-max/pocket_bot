from fastapi import FastAPI, Request
from database import add_registration
from config import WEBHOOK_SECRET

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if data.get("token") != WEBHOOK_SECRET:
        return {"status": "forbidden"}

    pocket_id = data.get("user_id")

    add_registration(pocket_id)

    return {"status": "ok"}
