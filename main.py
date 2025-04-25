from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from typing import Dict, Any, Optional

app = FastAPI()

class ProxyRequest(BaseModel):
    url: str
    headers: Optional[Dict[str, Any]] = {}
    body: Optional[Dict[str, Any]] = {}

@app.post("/proxy")
async def proxy_request(request: ProxyRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=request.url,
            headers=request.headers,
            json=request.body
        )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("content-type") == "application/json" else response.text
        }

@app.get("/")
async def read_root():
    return {"status": "Proxy server is running"}
