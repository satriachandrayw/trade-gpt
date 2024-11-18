from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field

class NewsBase(BaseModel):
    title: str
    content: str
    url: HttpUrl
    published_date: Optional[str]
    relevance_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)

class NewsSearchParams(BaseModel):
    query: str
    max_results: int = 10
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None

class NewsResponse(BaseModel):
    answer: str
    articles: List[NewsBase]
    total_count: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)