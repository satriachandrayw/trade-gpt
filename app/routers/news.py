from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.news import NewsSearchParams, NewsResponse
from app.services.news_service import search_financial_news

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

async def validate_news_params(
    query: Annotated[str, Query(min_length=3)],
    max_results: Annotated[int, Query(ge=1, le=50)] = 10,
    include_domains: str | None = None,
    exclude_domains: str | None = None,
) -> NewsSearchParams:
    """
    Validate and transform query parameters into NewsSearchParams
    """
    # Transform comma-separated domains into lists
    include_domains_list = (
        [domain.strip() for domain in include_domains.split(",")]
        if include_domains
        else None
    )
    exclude_domains_list = (
        [domain.strip() for domain in exclude_domains.split(",")]
        if exclude_domains
        else None
    )
    
    return NewsSearchParams(
        query=query,
        max_results=max_results,
        include_domains=include_domains_list,
        exclude_domains=exclude_domains_list
    )

@router.get("/search", response_model=NewsResponse)
async def search_news(
    params: Annotated[NewsSearchParams, Depends(validate_news_params)]
) -> NewsResponse:
    """
    Search for financial news related to XAU/USD trading
    
    Parameters:
    - query: Search query string (min 3 characters)
    - max_results: Maximum number of results to return (1-50)
    - include_domains: Comma-separated list of domains to include
    - exclude_domains: Comma-separated list of domains to exclude
    
    Returns:
    - NewsResponse containing matching articles
    """
    try:
        return await search_financial_news(params)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search news: {str(e)}"
        )