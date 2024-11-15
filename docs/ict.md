# Inner Circle Trading (ICT) Strategy Documentation

## 1. Introduction

The Inner Circle Trading (ICT) strategy, developed by Michael J. Huddleston, focuses on understanding market structure, liquidity pools, order blocks, and fair value gaps (FVG). This strategy aims to identify high-probability trading opportunities by analyzing how institutional traders operate in the financial markets.

## 2. Key Concepts

### 2.1 Market Structure
- **Swing Highs and Lows**: Identify significant swing highs and lows to understand the overall market structure.
- **Market Phases**: Recognize different market phases such as accumulation, distribution, uptrend, and downtrend.

### 2.2 Liquidity Pools
- **Definition**: Areas where liquidity is likely to be concentrated, such as previous highs and lows, round numbers, and order blocks.
- **Stop Hunts**: Understand how institutional traders may target liquidity pools to trigger stop-loss orders and create trading opportunities.

### 2.3 Order Blocks
- **Definition**: Areas where institutional traders have placed large orders, causing significant price movements.
- **Identification**: Look for consolidation areas before a strong price move, which indicates the presence of an order block.

### 2.4 Fair Value Gaps (FVG)
- **Definition**: Gaps between price levels where there is an imbalance between buyers and sellers.
- **Usage**: Use FVGs to identify potential entry and exit points, as price often returns to fill these gaps.

### 2.5 Time and Price Theory
- **Optimal Trade Entry (OTE)**: Identify the optimal entry point within a price retracement, typically between the 61.8% and 79% Fibonacci retracement levels.
- **Kill Zones**: Specific times of the day when institutional traders are most active, such as the London Open, New York Open, and London Close.

### 2.6 Institutional Order Flow
- **Bias**: Determine the overall market bias (bullish or bearish) based on institutional order flow.
- **Confirmation**: Use multiple timeframes to confirm the market bias and identify high-probability trading setups.

## 3. ICT Trading Strategy Steps

### Step 1: Analyze Market Structure
- Identify the overall trend by analyzing swing highs and lows.
- Determine the current market phase (accumulation, distribution, uptrend, downtrend).

### Step 2: Identify Liquidity Pools
- Look for areas where liquidity is likely to be concentrated, such as previous highs and lows, round numbers, and order blocks.
- Anticipate potential stop hunts by institutional traders.

### Step 3: Locate Order Blocks
- Identify consolidation areas before a strong price move, indicating the presence of an order block.
- Use order blocks as potential entry and exit points.

### Step 4: Use Fair Value Gaps (FVG)
- Identify gaps between price levels where there is an imbalance between buyers and sellers.
- Use FVGs to identify potential entry and exit points, as price often returns to fill these gaps.

### Step 5: Apply Time and Price Theory
- Use the Optimal Trade Entry (OTE) method to identify the optimal entry point within a price retracement.
- Focus on specific times of the day (kill zones) when institutional traders are most active.

### Step 6: Confirm Institutional Order Flow
- Determine the overall market bias using multiple timeframes.
- Look for confluence between the identified order blocks, FVGs, and liquidity pools.

## 4. Example of ICT Trading Setup

### 1. Identify Market Structure
- Determine the overall trend by analyzing swing highs and lows on the daily chart.
- Identify the current market phase (e.g., uptrend).

### 2. Locate Liquidity Pools
- Identify previous swing highs and lows as potential liquidity pools.
- Look for round numbers and order blocks.

### 3. Find Order Blocks
- Identify consolidation areas before a strong price move on the 4-hour chart.
- Mark these areas as potential order blocks.

### 4. Use Fair Value Gaps (FVG)
- Identify FVGs on the 1-hour chart.
- Use these gaps to identify potential entry and exit points.

### 5. Apply Time and Price Theory
- Use the OTE method to identify the optimal entry point within a price retracement on the 15-minute chart.
- Focus on kill zones such as the London Open and New York Open.

### 6. Confirm Institutional Order Flow
- Confirm the market bias using multiple timeframes (daily, 4-hour, 1-hour).
- Look for confluence between the identified order blocks, FVGs, and liquidity pools.

## 5. Example Code for ICT Trading Setup

```python
import pandas as pd
import numpy as np

# Load historical price data
price_data = pd.read_csv('price_data.csv')

# Identify market structure
def identify_market_structure(data):
    data['Trend'] = np.where(data['High'] > data['High'].shift(1), 'uptrend', 'downtrend')
    data['Trend'] = np.where(data['Low'] < data['Low'].shift(1), 'downtrend', data['Trend'])
    return data

# Identify swing highs and lows (liquidity pools)
def identify_liquidity_pools(data):
    data['Liquidity_Pool_High'] = data['High'].rolling(window=5, center=True).apply(lambda x: x.max() == x[2], raw=True)
    data['Liquidity_Pool_Low'] = data['Low'].rolling(window=5, center=True).apply(lambda x: x.min() == x[2], raw=True)
    return data

# Identify order blocks
def identify_order_blocks(data):
    data['Bullish_Order_Block'] = (data['Close'].shift(1) < data['Open'].shift(1)) & (data['Close'] > data['Open'])
    data['Bearish_Order_Block'] = (data['Close'].shift(1) > data['Open'].shift(1)) & (data['Close'] < data['Open'])
    return data

# Identify fair value gaps (FVG)
def identify_fvg(data):
    data['FVG'] = (data['High'].shift(1) < data['Low']) | (data['Low'].shift(1) > data['High'])
    return data

# Generate trading signals based on ICT concepts
def generate_trading_signals(data):
    signals = []
    for i in range(len(data)):
        if data['Trend'].iloc[i] == 'uptrend' and data['Bullish_Order_Block'].iloc[i] and data['Liquidity_Pool_Low'].iloc[i] and data['FVG'].iloc[i]:
            signals.append('buy')
        elif data['Trend'].iloc[i] == 'downtrend' and data['Bearish_Order_Block'].iloc[i] and data['Liquidity_Pool_High'].iloc[i] and data['FVG'].iloc[i]:
            signals.append('sell')
        else:
            signals.append('hold')
    return signals

# Apply ICT trading strategy
price_data = identify_market_structure(price_data)
price_data = identify_liquidity_pools(price_data)
price_data = identify_order_blocks(price_data)
price_data = identify_fvg(price_data)

# Generate trading signals
price_data['Signal'] = generate_trading_signals(price_data)
print(price_data[['Date', 'Signal']])