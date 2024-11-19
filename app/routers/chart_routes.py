from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.services.chart_service import ChartService, Timeframe

router = APIRouter(prefix="/chart", tags=["chart"])
chart_service = ChartService()

@router.get("/market-structure/{timeframe}")
async def get_market_structure(timeframe: str) -> Dict[str, Any]:
    """Get market structure analysis for XAU/USD"""
    try:
        tf = Timeframe[timeframe.upper()]
        return chart_service.get_market_structure(tf)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order-blocks/{timeframe}")
async def get_order_blocks(timeframe: str) -> List[Dict[str, Any]]:
    """Get potential order blocks for XAU/USD"""
    try:
        tf = Timeframe[timeframe.upper()]
        return chart_service.find_order_blocks(tf)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fvg/{timeframe}")
async def get_fair_value_gaps(timeframe: str) -> List[Dict[str, Any]]:
    """Get Fair Value Gaps (FVG) for XAU/USD"""
    try:
        tf = Timeframe[timeframe.upper()]
        return chart_service.find_fair_value_gaps(tf)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ohlcv/{timeframe}")
async def get_ohlcv_data(timeframe: str, count: int = 1000) -> Dict[str, Any]:
    """Get OHLCV data for XAU/USD"""
    try:
        tf = Timeframe[timeframe.upper()]
        df = chart_service.get_ohlcv(tf, 0, count)
        if df.empty:
            raise HTTPException(status_code=500, detail="Failed to get OHLCV data")
        
        return {
            "data": df.to_dict(orient="records"),
            "count": len(df),
            "timeframe": timeframe,
            "symbol": "XAUUSD"
        }
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
