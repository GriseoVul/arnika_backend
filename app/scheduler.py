from datetime import datetime, timedelta
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from typing import Dict, List, Optional
from fastapi import FastAPI
from app.sheetRequest import get_google_sheet


CAHCE_TTL = timedelta(minutes=30)
last_update_time: Optional[datetime] = None
cached_data: List[Dict[str, str]] = []

scheduler = AsyncIOScheduler(timezone=utc)

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

def get_cache_info():
    return {
        "last_update": last_update_time.isoformat() if last_update_time else None,
        "items_count": len(cached_data),
        "next_update_in": (last_update_time + CAHCE_TTL - datetime.now() ).total_seconds() if last_update_time else None
    }
