import os
import httpx
from fastapi import FastAPI, Request

app = FastAPI()

# --- METTEZ VOS CLÉS ICI ---
TELEGRAM_TOKEN = "VOTRE_TOKEN_BOTFATHER"
DIFY_API_KEY = "VOTRE_API_KEY_DIFY"
DIFY_API_URL = "https://dify.ai"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    if "message" not in payload or "text" not in payload["message"]:
        return {"status": "ignored"}
    chat_id = payload["message"]["chat"]["id"]
    user_text = payload["message"]["text"]
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    dify_data = {
        "inputs": {},
        "query": user_text,
        "response_mode": "blocking",
        "user": f"telegram_{chat_id}",
        "conversation_id": ""
    }
    async with httpx.AsyncClient() as client:
        dify_response = await client.post(DIFY_API_URL, json=dify_data, headers=headers, timeout=30.0)
        dify_result = dify_response.json()
        bot_answer = dify_result.get("answer", "Désolé, je n'ai pas pu traiter votre demande.")
        telegram_url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
        await client.post(telegram_url, json={"chat_id": chat_id, "text": bot_answer})
    return {"status": "success"}
