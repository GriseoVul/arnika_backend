from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from typing import Dict, List, Optional


CAHCE_TTL = timedelta(minutes=30)
last_update_time: Optional[datetime] = None
cached_data: List[Dict[str, str]] = []

scheduler = AsyncIOScheduler(timezone=utc)

def get_google_sheet():
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(credentials=creds)
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1OpkcVMwqZmsR1nTVEjvj92pPUm-Wn4BvMbIj5NjRvck")
    return sheet

@scheduler.scheduled_job('cron', minute=30)
async def update_cache():
    global cached_data, last_update_time
    try:
        sheet = get_google_sheet().get_worksheet(0)
        cached_data = sheet.get_all_records(
            expected_headers=["Статус", "Номер аптеки по лицензии", "Название", "Город", "Район", "Адрес", "Номер телефона", "Акция", "Ориентир", "Номер аптеки (бот)","Карта всех аптек", "ПН","ВТ", "СР", "ЧТ","ПТ", "СБ", "ВС","slug"]
        )
        last_update_time = datetime.now()
        print(f"Cache updated at {last_update_time}")
    except Exception as e:
        print(f"Failed to update cache: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

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
    return {
        "last_update": last_update_time.isoformat() if last_update_time else None,
        "items_count": len(cached_data),
        "next_update_in": (last_update_time + CAHCE_TTL - datetime.now() ).total_seconds() if last_update_time else None
    }