import os
from typing import List, Dict, Any
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException
from tavily import TavilyClient  # Changed from TavilyClient to Client

from app.core.config import settings
from app.schemas.news import NewsSearchParams, NewsResponse, NewsBase

logger = logging.getLogger(__name__)

# Initialize Tavily client
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)  # Changed initialization

async def search_financial_news(params: NewsSearchParams) -> NewsResponse:
  """
  Search for financial news using Tavily's Python SDK
  """
  try:
      # Prepare search query
      search_query = f"{params.query}"
      
      # Use Tavily SDK to search
      response = tavily_client.search(
          query=search_query,
          search_depth="advanced",
          max_results=params.max_results,
          include_domains=params.include_domains,
          exclude_domains=params.exclude_domains,
          include_answer=True,
          topic="news"
      )
      
      # Transform Tavily results to our schema
      articles = [
          NewsBase(
              title=result["title"],
              content=result["content"],
              url=result["url"],
              published_date=result.get("published_date"),
              relevance_score=result.get("score", 0.0),
          )
          for result in response["results"]
      ]
      
      return NewsResponse(
          answer=response.get("answer"),
          articles=articles,
          total_count=len(articles)
      )
          
  except Exception as e:
      raise HTTPException(
          status_code=502,
          detail=f"News service error: {str(e)}"
      )

class NewsService:
    def __init__(self):
        self.tavily_client = tavily_client
  
    async def fetch_news(self, session_name: str) -> List[Dict]:
        try:
            params = NewsSearchParams(
                query=f"forex gold XAU/USD market {session_name} session",
                max_results=10,
                include_domains=["reuters.com", "bloomberg.com", "forexlive.com"],
                exclude_domains=[]
            )
            
            response = await search_financial_news(params)
            logger.info(f"Fetched {len(response.articles)} news items for {session_name} session")
            return [article.dict() for article in response.articles]
                
        except Exception as e:
            logger.error(f"Error fetching news for {session_name} session: {str(e)}")
            return []
