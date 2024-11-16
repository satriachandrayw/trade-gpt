### **When Does a High-Probability Trade Appear in ICT?**

High-probability trade setups in ICT occur when multiple ICT concepts align, creating a strong confluence of factors. These setups are based on observing price behavior that reflects institutional order flow and liquidity hunts.

#### **Key Conditions for High-Probability Positions**

1. **Liquidity Sweep Followed by a Break of Structure (BOS):**
   - **Setup**: Price sweeps liquidity (above a recent high or below a recent low) and then reverses direction with a BOS.
   - **High Probability**: This setup signals that smart money has grabbed liquidity and is likely driving price in the opposite direction.
   - **Bot’s Role**: Detect liquidity sweeps (large wicks above/below key levels) and confirm BOS (price closing beyond the last swing point).

2. **Order Block (OB) Retests:**
   - **Setup**: Price retraces to an identified order block after a strong move away.
   - **High Probability**: Order blocks are areas where institutional orders have been placed, so a retest often triggers significant reactions.
   - **Bot’s Role**: Identify the OB and monitor for price rejections (e.g., wicks, small-bodied candles) when price returns to it.

3. **Fair Value Gap (FVG) Fills:**
   - **Setup**: Price retraces into a fair value gap (inefficiency) and shows rejection or continuation signals.
   - **High Probability**: FVG fills indicate a rebalancing of price and are often used as entry points for smart money.
   - **Bot’s Role**: Identify gaps between candles and monitor for retracement into these zones.

4. **Optimal Trade Entry (OTE) within Discount or Premium Zones:**
   - **Setup**: Price retraces to the 61.8%–79% Fibonacci zone, ideally aligned with an OB or FVG.
   - **High Probability**: This combines retracement logic with institutional price behavior, increasing entry precision.
   - **Bot’s Role**: Calculate the OTE zone and check for confluence with OBs or liquidity zones.

5. **Time-of-Day Confluence (Killzones):**
   - **Setup**: Signals occur during key trading sessions (e.g., London or New York killzones).
   - **High Probability**: Institutions are most active during these times, increasing the likelihood of sustained moves.
   - **Bot’s Role**: Filter signals to execute only during killzones.

---

### **Bot’s Workflow for Identifying High-Probability Trades**

#### **1. Data Collection and Preprocessing**
- **Input Data**: Real-time candlestick data (OHLCV) and historical price action.
- **Chart Information**:
  - Identify swing highs/lows (zigzag indicator or price action analysis).
  - Calculate Fibonacci levels.
  - Highlight OBs and FVGs from historical price moves.
  
#### **2. High-Probability Detection Logic**
Here’s how the bot identifies high-probability setups:

---

#### **Liquidity Sweep Detection**
- **Condition**: 
  - Recent high/low is breached by a large wick.
  - Price closes back inside the range.
- **Bot Implementation**:
  ```python
  if price.high > recent_high and close < recent_high:
      liquidity_sweep = True
  elif price.low < recent_low and close > recent_low:
      liquidity_sweep = True
  else:
      liquidity_sweep = False
  ```

---

#### **Break of Structure (BOS)**
- **Condition**: 
  - After a liquidity sweep, price breaks the previous swing high (for a bullish signal) or swing low (for a bearish signal).
- **Bot Implementation**:
  ```python
  if liquidity_sweep and price.close > swing_high:
      BOS = "Bullish"
  elif liquidity_sweep and price.close < swing_low:
      BOS = "Bearish"
  ```

---

#### **Order Block Identification**
- **Condition**:
  - Last down candle before a strong bullish move (bullish OB).
  - Last up candle before a strong bearish move (bearish OB).
- **Bot Implementation**:
  ```python
  # Detect significant candles
  if strong_bullish_move:
      bullish_OB = last_bearish_candle
  elif strong_bearish_move:
      bearish_OB = last_bullish_candle
  ```

---

#### **Fair Value Gap (FVG) Detection**
- **Condition**:
  - Gap between the high of one candle and the low of the next (inefficiency).
  - Price retraces to this gap.
- **Bot Implementation**:
  ```python
  if previous_candle.high < current_candle.low:
      FVG = (previous_candle.high, current_candle.low)
  if price retraces to FVG:
      FVG_filled = True
  ```

---

#### **Optimal Trade Entry (OTE)**
- **Condition**:
  - Price retraces into the 61.8%–79% Fibonacci retracement zone.
  - Confluence with OBs or FVGs.
- **Bot Implementation**:
  ```python
  fib_zone = calculate_fib(high, low)  # Calculate 61.8%–79% retracement
  if fib_zone.contains(price) and OB_zone.contains(price):
      OTE = True
  ```

---

#### **Time Filtering**
- **Condition**:
  - Signal aligns with the London or New York killzone (e.g., 2 AM–5 AM EST or 7 AM–10 AM EST).
- **Bot Implementation**:
  ```python
  if current_time in killzone and signal_detected:
      high_probability_signal = True
  ```

---

### **End-to-End Workflow for the Bot**

1. **Real-Time Monitoring**:
   - Continuously collect candlestick data.
   - Monitor for liquidity sweeps, OBs, FVGs, and BOS in real-time.

2. **Signal Detection**:
   - Evaluate if all conditions for a high-probability trade are met.
   - Combine confluence factors: liquidity sweep → BOS → FVG → OB retest.

3. **Signal Scoring**:
   - Assign weights to each condition (e.g., OB confluence = 40%, FVG = 30%).
   - Only execute trades when signal score exceeds a predefined threshold.

4. **Trade Recommendation**:
   - If all conditions align:
     - **Entry**: At the OB or FVG.
     - **Stop Loss**: Below/above liquidity sweep level.
     - **Take Profit**: At a predetermined risk/reward ratio (e.g., 1:2).

5. **Execution**:
   - For manual trading: Display trade details.
   - For automated trading: Integrate with an API to execute orders.

---

### **Visual Representation**
To make the bot "read" chart data:
- Use libraries like **Matplotlib** or **Plotly** in Python to visualize price levels.
- Mark liquidity sweeps, OB zones, FVGs, and retracement zones on the chart.
- Example Chart Markup:
  - Green Zones: Bullish OBs.
  - Red Zones: Bearish OBs.
  - Blue Lines: FVG.
  - Arrows: Signal directions based on BOS and liquidity sweeps.

---

### **Next Steps**
1. **Backtest ICT Conditions**:
   - Test the bot’s logic on historical XAU/USD or BTC/USD data to validate.
2. **Optimize Parameters**:
   - Fine-tune thresholds for liquidity sweeps, FVGs, and OBs.
3. **Integrate APIs**:
   - Use brokers like MetaTrader or TradingView for live execution.

Would you like to explore the coding aspect of this workflow or focus on implementing specific ICT concepts?