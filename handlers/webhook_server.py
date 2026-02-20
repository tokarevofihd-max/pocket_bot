from fastapi import FastAPI, Request
import sqlite3
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    pocket_id = data.get("pocket_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET is_verified=1 WHERE pocket_id=?", (pocket_id,))
    conn.commit()
    conn.close()

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("webhook_server:app", host="127.0.0.1", port=8000, reload=True)
