import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, List, Dict, Any, Tuple
import logging
from enum import Enum
import os
import numpy as np
import time

logger = logging.getLogger(__name__)

class Timeframe(Enum):
    M5 = "5m"      # 5 minutes
    M15 = "15m"    # 15 minutes
    M30 = "30m"    # 30 minutes
    H1 = "1h"      # 1 hour
    H4 = "4h"      # 4 hours
    D1 = "1d"      # 1 day
    W1 = "1wk"     # 1 week

class ChartService:
    def __init__(self, symbol: str = "GC=F"):
        """
        Initialize the chart service
        
        Args:
            symbol: Trading symbol (default: GC=F for Gold Futures)
        """
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        
    def get_ohlcv(self, 
                 timeframe: Timeframe,
                 start_pos: int = 0,
                 count: int = 1000) -> pd.DataFrame:
        """
        Get OHLCV data for the specified timeframe
        
        Args:
            timeframe: Timeframe enum value
            start_pos: Start position (0 means from the current bar)
            count: Number of bars to get
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Calculate start and end dates
            end_date = pd.Timestamp.now()
            
            # For intraday data, we need a shorter timespan
            if timeframe in [Timeframe.M5, Timeframe.M15, Timeframe.M30, Timeframe.H1, Timeframe.H4]:
                # For intraday, get data for last 60 days max
                start_date = end_date - pd.Timedelta(days=60)
            else:
                # Add extra periods to account for start_pos
                total_periods = start_pos + count
                
                if timeframe == Timeframe.D1:
                    start_date = end_date - pd.Timedelta(days=total_periods)
                else:  # W1
                    start_date = end_date - pd.Timedelta(weeks=total_periods)

            # Convert dates to strings for yfinance
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            logger.info(f"Fetching {timeframe.value} data from {start_str} to {end_str}")

            # Get the raw data from yfinance
            df = self.ticker.history(
                interval=timeframe.value,
                start=start_str,
                end=end_str,
                prepost=True  # Include pre/post market data
            )
            
            if df.empty:
                logger.error(f"Failed to get data for {self.symbol} {timeframe.name}")
                return pd.DataFrame()
            
            # Reset index to make datetime a column
            df = df.reset_index()
            
            # Rename columns to match previous format
            df = df.rename(columns={
                'Date': 'Datetime',
                'Datetime': 'Datetime',  # Handle both column names
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Close': 'Close',
                'Volume': 'tick_volume'
            })
            
            # Add placeholder columns for compatibility
            df['spread'] = 0
            df['real_volume'] = df['tick_volume']
            
            # For intraday data, we got more data than needed, so slice from the end
            if timeframe in [Timeframe.M5, Timeframe.M15, Timeframe.M30, Timeframe.H1, Timeframe.H4]:
                df = df.iloc[-(start_pos + count):]
            
            # If we have start_pos, skip those records
            if start_pos > 0:
                df = df.iloc[start_pos:]
            
            # Limit to requested count
            df = df.head(count)
            
            logger.info(f"Retrieved {len(df)} rows of data")
            return df
            
        except Exception as e:
            logger.error(f"Error getting OHLCV data: {str(e)}")
            return pd.DataFrame()

    def get_current_price(self) -> dict:
        """
        Get current price and market data
        
        Returns:
            Dictionary containing current price information
        """
        try:
            # Get real-time data
            ticker_info = self.ticker.info
            current_data = {
                'symbol': self.symbol,
                'datetime': pd.Timestamp.now(),
                'price': ticker_info.get('regularMarketPrice', ticker_info.get('currentPrice')),
                'open': ticker_info.get('regularMarketOpen'),
                'high': ticker_info.get('regularMarketDayHigh'),
                'low': ticker_info.get('regularMarketDayLow'),
                'volume': ticker_info.get('regularMarketVolume'),
                'bid': ticker_info.get('bid'),
                'ask': ticker_info.get('ask'),
                'volume': ticker_info.get('volume'),
                'day_high': ticker_info.get('dayHigh'),
                'day_low': ticker_info.get('dayLow'),
                'prev_close': ticker_info.get('previousClose'),
                'last_price': ticker_info.get('lastPrice'),  # Add last price for futures
                'market_state': ticker_info.get('marketState')  # Add market state
            }
            
            logger.info(f"Retrieved current price for {self.symbol}")
            return current_data
            
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            return {}

    def __del__(self):
        """Cleanup"""
        pass
