from datetime import datetime, timedelta
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from typing import Dict, List, Optional
from fastapi import FastAPI
from app.sheetRequest import get_google_sheet
from app.cerbot import renew_cert

class CacheManager:
    CAHCE_TTL = timedelta(minutes=30)
    last_update_time: Optional[datetime] = None
    cached_data: List[Dict[str, str]] = []

    async def update_cache(self):
        try:
            sheet = get_google_sheet().get_worksheet(0)
            self.cached_data = sheet.get_all_records()
            self.last_update_time = datetime.now()
            print(f"Cache updated at {self.last_update_time}")
        except Exception as e:
            print(f"Failed to update cache: {str(e)}")

    def get_cache_info(self):
        return {
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "items_count": len(self.cached_data),
            "next_update_in": (self.last_update_time + self.CAHCE_TTL - datetime.now() ).total_seconds() if self.last_update_time else None
        }

cache_manager = CacheManager()

scheduler = AsyncIOScheduler(timezone=utc)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(cache_manager.update_cache, 'interval', days=1)
    scheduler.add_job(renew_cert, 'interval', days=1)
    scheduler.start()
    yield
    scheduler.shutdown()


