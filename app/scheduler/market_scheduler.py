from datetime import datetime, timedelta
import asyncio
import logging
from typing import Callable, Coroutine, Any

from app.config.market_schedule import MARKET_SESSIONS, NEWS_FETCH_OFFSET

logger = logging.getLogger(__name__)

class MarketScheduler:
    def __init__(self):
        self.tasks = []
        
    async def schedule_next_runs(self, callback: Callable[[str], Coroutine[Any, Any, None]]):
        while True:
            now = datetime.utcnow()
            
            for session in MARKET_SESSIONS:
                # Convert session time to today's date
                session_time = datetime.combine(now.date(), session.open_time)
                
                # If the session time has passed for today, schedule for tomorrow
                if session_time <= now:
                    session_time = session_time + timedelta(days=1)
                    
                # Calculate when to fetch news (30 minutes before session)
                fetch_time = session_time - timedelta(minutes=NEWS_FETCH_OFFSET)
                
                # Calculate seconds until next run
                seconds_until_run = (fetch_time - now).total_seconds()
                
                if seconds_until_run > 0:
                    logger.info(f"Scheduling news fetch for {session.name} session at {fetch_time}")
                    self.tasks.append(
                        asyncio.create_task(self._schedule_task(seconds_until_run, callback, session.name))
                    )
            
            # Check again in 1 hour
            await asyncio.sleep(3600)
            
    async def _schedule_task(self, delay: float, callback: Callable[[str], Coroutine[Any, Any, None]], session_name: str):
        await asyncio.sleep(delay)
        await callback(session_name)