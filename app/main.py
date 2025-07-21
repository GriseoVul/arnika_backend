from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.scheduler import (
    lifespan, 
    cached_data, 
    update_cache, 
    get_cache_info
)
from config import settings
import uvicorn


app = FastAPI(lifespan=lifespan)
app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], #tilda host
    allow_methods=["GET"],
    allow_headers=['*']
)

@app.get("/api/data/{slug}")
async def get_data_by_slug(slug: str):
    if not cached_data:
        await update_cache()
    
    for record in cached_data:
        if record.get("slug") == slug:
            return record
    
    raise HTTPException(404, detail="{slug} not found!")

@app.get("/api/cache-info")
async def cache_info():
    return get_cache_info()

def main():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=443,
        ssl_certfile=f"/etc/letsencrypt/live/{settings.host_name}/fullchain.pem",
        ssl_keyfile=f"/etc/letsencrypt/live/{settings.host_name}/privkey.pem"
    )

if __name__ == "__main__":
    main()
