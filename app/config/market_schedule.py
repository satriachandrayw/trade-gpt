
from datetime import time
from typing import NamedTuple

class MarketSession(NamedTuple):
    name: str
    open_time: time  # UTC times
    close_time: time

MARKET_SESSIONS = [
    MarketSession("Asia", time(hour=0, minute=0), time(hour=9, minute=0)),
    MarketSession("London", time(hour=7, minute=0), time(hour=16, minute=0)),
    MarketSession("New York", time(hour=12, minute=0), time(hour=21, minute=0))
]

# Time before session open to fetch news (in minutes)
NEWS_FETCH_OFFSET = 30