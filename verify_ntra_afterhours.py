#!/usr/bin/env python3
"""
Verify NTRA after-hours price from multiple data points
Checking current price, after-hours, and recent trading
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("NTRA PRICE VERIFICATION - INCLUDING AFTER-HOURS")
print(f"Query Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} EST")
print("=" * 100)

# Get NTRA ticker
ntra = yf.Ticker("NTRA")

# Method 1: Get current info
print("\n📊 METHOD 1: Current Stock Info")
print("-" * 80)
try:
    info = ntra.info
    print(f"Regular Market Price: ${info.get('regularMarketPrice', 'N/A')}")
    print(f"Previous Close: ${info.get('previousClose', 'N/A')}")
    print(f"Day High: ${info.get('dayHigh', 'N/A')}")
    print(f"Day Low: ${info.get('dayLow', 'N/A')}")
    print(f"Current Price: ${info.get('currentPrice', 'N/A')}")
    print(f"Post Market Price: ${info.get('postMarketPrice', 'N/A')}")
    print(f"Pre Market Price: ${info.get('preMarketPrice', 'N/A')}")
    if info.get('postMarketPrice'):
        post_change = info.get('postMarketChange', 0)
        post_pct = info.get('postMarketChangePercent', 0) * 100
        print(f"Post Market Change: ${post_change:.2f} ({post_pct:.2f}%)")
except Exception as e:
    print(f"Error fetching info: {e}")

# Method 2: Get latest history
print("\n📊 METHOD 2: Latest Trading History")
print("-" * 80)
try:
    # Get 1 minute data for today
    hist_1d = ntra.history(period="1d", interval="1m")
    if len(hist_1d) > 0:
        print(f"Last Regular Trading:")
        print(f"  Time: {hist_1d.index[-1]}")
        print(f"  Close: ${hist_1d['Close'].iloc[-1]:.2f}")
        print(f"  Volume: {hist_1d['Volume'].iloc[-1]:,.0f}")
        
    # Get 5 day data
    hist_5d = ntra.history(period="5d", interval="15m", prepost=True)
    if len(hist_5d) > 0:
        latest_5 = hist_5d.tail(10)
        print(f"\nLast 10 fifteen-minute bars:")
        for idx, row in latest_5.iterrows():
            print(f"  {idx.strftime('%Y-%m-%d %H:%M')}: ${row['Close']:.2f} (Vol: {row['Volume']:,.0f})")
except Exception as e:
    print(f"Error fetching history: {e}")

# Method 3: Get most recent daily data
print("\n📊 METHOD 3: Recent Daily Closes")
print("-" * 80)
try:
    hist_daily = ntra.history(period="5d")
    for idx, row in hist_daily.iterrows():
        change = row['Close'] - row['Open']
        change_pct = (change / row['Open']) * 100
        print(f"{idx.strftime('%Y-%m-%d')}: Open ${row['Open']:.2f}, Close ${row['Close']:.2f}, Change {change:+.2f} ({change_pct:+.1f}%)")
except Exception as e:
    print(f"Error fetching daily data: {e}")

# Method 4: Check extended hours specifically
print("\n📊 METHOD 4: Extended Hours Trading")
print("-" * 80)
try:
    # Fetch with pre/post market data
    today = datetime.now()
    start = today - timedelta(days=1)
    
    hist_extended = ntra.history(start=start, end=today, interval="5m", prepost=True)
    
    if len(hist_extended) > 0:
        # Find after-hours data (after 4 PM)
        after_4pm = hist_extended[hist_extended.index.hour >= 16]
        if len(after_4pm) > 0:
            print("After-Hours Trading (Post 4 PM EST):")
            for idx, row in after_4pm.tail(5).iterrows():
                print(f"  {idx.strftime('%H:%M')}: ${row['Close']:.2f} (Volume: {row['Volume']:,.0f})")
            
            print(f"\nLatest After-Hours Price: ${after_4pm['Close'].iloc[-1]:.2f}")
            ah_change = after_4pm['Close'].iloc[-1] - hist_extended[hist_extended.index.hour < 16]['Close'].iloc[-1]
            print(f"After-Hours Change: ${ah_change:+.2f}")
        else:
            print("No after-hours data available yet")
            
    # Get the official closing price
    regular_close = hist_extended[hist_extended.index.hour < 16]['Close'].iloc[-1] if len(hist_extended[hist_extended.index.hour < 16]) > 0 else None
    if regular_close:
        print(f"\nRegular Session Close: ${regular_close:.2f}")
        
except Exception as e:
    print(f"Error fetching extended hours: {e}")

# Method 5: Calculate key levels
print("\n📊 METHOD 5: Key Price Levels")
print("-" * 80)
try:
    hist_1m = ntra.history(period="1mo")
    current = hist_1m['Close'].iloc[-1]
    high_52w = ntra.info.get('fiftyTwoWeekHigh', 0)
    
    print(f"Last Official Close: ${current:.2f}")
    print(f"52-Week High: ${high_52w:.2f}")
    print(f"Distance from 52W High: {((current - high_52w)/high_52w)*100:.1f}%")
    
    # Check if we're at new highs
    if current >= high_52w * 0.99:
        print("⚠️ AT OR NEAR 52-WEEK HIGH!")
        
    # Volume analysis
    avg_volume = hist_1m['Volume'].mean()
    last_volume = hist_1m['Volume'].iloc[-1]
    print(f"\nVolume Analysis:")
    print(f"Last Day Volume: {last_volume:,.0f}")
    print(f"Average Volume: {avg_volume:,.0f}")
    print(f"Volume Ratio: {last_volume/avg_volume:.2f}x")
    
except Exception as e:
    print(f"Error calculating levels: {e}")

# Summary
print("\n" + "=" * 100)
print("VERIFICATION SUMMARY")
print("=" * 100)

try:
    # Get the most reliable price
    current_price = info.get('regularMarketPrice', 0)
    post_price = info.get('postMarketPrice', None)
    
    print(f"Regular Market Close: ${current_price:.2f}")
    if post_price:
        print(f"After-Hours Price: ${post_price:.2f}")
        print(f"After-Hours Move: ${post_price - current_price:+.2f} ({((post_price/current_price - 1)*100):+.1f}%)")
        
        if post_price > 241:
            print("\n⚠️ BREAKOUT CONFIRMED - Trading above $241 resistance!")
        elif post_price > 239.40:
            print("\n⚠️ TESTING BREAKOUT - At key resistance!")
    else:
        print("After-Hours Price: Not available or no after-hours trading yet")
        
    print(f"\n52-Week High: ${high_52w:.2f}")
    if current_price >= high_52w * 0.99 or (post_price and post_price >= high_52w):
        print("🚨 NEW 52-WEEK HIGH TERRITORY!")
        
except:
    print("Unable to determine current prices - market may be closed")

print("\n" + "=" * 100)
print("Data from Yahoo Finance API")
print("Note: After-hours data may have 15-20 minute delay")
print("=" * 100)