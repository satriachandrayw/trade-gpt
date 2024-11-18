import asyncio
from app.core.logger import get_logger
from app.services.news_service import NewsService
from app.scheduler.market_scheduler import MarketScheduler

logger = get_logger(__name__)

async def run_scheduler():
    news_service = NewsService()
    scheduler = MarketScheduler()
    
    async def fetch_news_callback(session_name: str):
        news = await news_service.fetch_news(session_name)
        logger.info(f"Fetched {len(news)} news items for {session_name} session")
    
    try:
        await scheduler.schedule_next_runs(fetch_news_callback)
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")

def start_scheduler():
    asyncio.run(run_scheduler())