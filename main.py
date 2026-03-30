from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI()

GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "http://127.0.0.1:18789/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GATEWAY_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openclaw/default",
                    "messages": [
                        {"role": "user", "content": req.message}
                    ],
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "raw": data,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
