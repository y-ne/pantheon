from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import Dict, Any, Optional, Literal

app = FastAPI()

class ProxyRequest(BaseModel):
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE",
                    "PATCH", "HEAD", "OPTIONS"] = "GET"
    headers: Optional[Dict[str, Any]] = {}
    body: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None
    timeout: Optional[float] = 30.0


@app.post("/proxy")
async def proxy_request(request: ProxyRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                json=request.body if request.method not in [
                    "GET", "HEAD"] else None,
                params=request.params,
                timeout=request.timeout
            )

            try:
                body = response.json()
            except:
                body = response.text

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": body
            }
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Request error: {str(e)}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Request timed out")


@app.get("/")
async def read_root():
    return {"status": "Proxy server is running"}
