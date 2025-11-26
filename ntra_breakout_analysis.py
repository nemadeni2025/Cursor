#!/usr/bin/env python3
"""
NTRA Breakout Analysis - Technical Assessment
Determining if Natera is breaking out or facing resistance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("NATERA (NTRA) - BREAKOUT OR RESISTANCE ANALYSIS")
print("=" * 100)
print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 100)

# Fetch data
ticker = "NTRA"
stock = yf.Ticker(ticker)

# Get different timeframes
hist_1y = stock.history(period="1y")
hist_6m = stock.history(period="6mo")
hist_3m = stock.history(period="3mo")
hist_1m = stock.history(period="1mo")
hist_5d = stock.history(period="5d")

current_price = hist_1y['Close'].iloc[-1]
current_volume = hist_1y['Volume'].iloc[-1]

print(f"\n📊 CURRENT PRICE ACTION")
print("-" * 80)
print(f"Current Price: ${current_price:.2f}")
print(f"Today's Volume: {current_volume:,.0f}")

# Key price levels
high_52w = hist_1y['High'].max()
low_52w = hist_1y['Low'].min()
high_6m = hist_6m['High'].max()
high_3m = hist_3m['High'].max()
high_1m = hist_1m['High'].max()

print(f"\n📈 KEY RESISTANCE & SUPPORT LEVELS")
print("-" * 80)
print(f"52-Week High: ${high_52w:.2f} ({((high_52w - current_price)/current_price*100):+.1f}% away)")
print(f"6-Month High: ${high_6m:.2f} ({((high_6m - current_price)/current_price*100):+.1f}% away)")
print(f"3-Month High: ${high_3m:.2f} ({((high_3m - current_price)/current_price*100):+.1f}% away)")
print(f"1-Month High: ${high_1m:.2f} ({((high_1m - current_price)/current_price*100):+.1f}% away)")
print(f"52-Week Low: ${low_52w:.2f} ({((current_price - low_52w)/low_52w*100):+.1f}% above)")

# Moving averages
sma_10 = hist_1y['Close'].rolling(10).mean().iloc[-1]
sma_20 = hist_1y['Close'].rolling(20).mean().iloc[-1]
sma_50 = hist_1y['Close'].rolling(50).mean().iloc[-1]
sma_200 = hist_1y['Close'].rolling(200).mean().iloc[-1]

print(f"\n📊 MOVING AVERAGE ANALYSIS")
print("-" * 80)
print(f"10-day SMA: ${sma_10:.2f} ({'+' if current_price > sma_10 else '-'}{abs((current_price/sma_10 - 1)*100):.1f}%)")
print(f"20-day SMA: ${sma_20:.2f} ({'+' if current_price > sma_20 else '-'}{abs((current_price/sma_20 - 1)*100):.1f}%)")
print(f"50-day SMA: ${sma_50:.2f} ({'+' if current_price > sma_50 else '-'}{abs((current_price/sma_50 - 1)*100):.1f}%)")
print(f"200-day SMA: ${sma_200:.2f} ({'+' if current_price > sma_200 else '-'}{abs((current_price/sma_200 - 1)*100):.1f}%)")

# Volume analysis
avg_volume_20 = hist_1y['Volume'].rolling(20).mean().iloc[-1]
avg_volume_50 = hist_1y['Volume'].rolling(50).mean().iloc[-1]
volume_ratio = current_volume / avg_volume_20

print(f"\n📊 VOLUME ANALYSIS")
print("-" * 80)
print(f"Current Volume: {current_volume:,.0f}")
print(f"20-Day Avg Volume: {avg_volume_20:,.0f}")
print(f"Volume Ratio: {volume_ratio:.2f}x average")
print(f"Volume Trend: {'Above Average ⬆️' if volume_ratio > 1.2 else 'Average' if volume_ratio > 0.8 else 'Below Average ⬇️'}")

# RSI Calculation
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

rsi_14 = calculate_rsi(hist_1y['Close'])
rsi_9 = calculate_rsi(hist_1y['Close'], 9)

print(f"\n📊 MOMENTUM INDICATORS")
print("-" * 80)
print(f"RSI (14): {rsi_14:.1f} {'🔴 Overbought' if rsi_14 > 70 else '🟢 Oversold' if rsi_14 < 30 else '⚪ Neutral'}")
print(f"RSI (9): {rsi_9:.1f} {'🔴 Overbought' if rsi_9 > 70 else '🟢 Oversold' if rsi_9 < 30 else '⚪ Neutral'}")

# MACD
exp1 = hist_1y['Close'].ewm(span=12, adjust=False).mean()
exp2 = hist_1y['Close'].ewm(span=26, adjust=False).mean()
macd = exp1 - exp2
signal = macd.ewm(span=9, adjust=False).mean()
macd_histogram = macd - signal

print(f"MACD Line: {macd.iloc[-1]:.2f}")
print(f"Signal Line: {signal.iloc[-1]:.2f}")
print(f"MACD Histogram: {macd_histogram.iloc[-1]:.2f} {'🟢 Bullish' if macd_histogram.iloc[-1] > 0 else '🔴 Bearish'}")

# Recent price action
last_5_days = hist_5d['Close'].values
price_trend = "Uptrend" if last_5_days[-1] > last_5_days[0] else "Downtrend"
consecutive_up = 0
consecutive_down = 0

for i in range(1, len(last_5_days)):
    if last_5_days[i] > last_5_days[i-1]:
        consecutive_up += 1
        consecutive_down = 0
    else:
        consecutive_down += 1
        consecutive_up = 0

print(f"\n📊 RECENT PRICE ACTION (Last 5 Days)")
print("-" * 80)
for i, price in enumerate(last_5_days):
    change = ((price / last_5_days[i-1] - 1) * 100) if i > 0 else 0
    print(f"Day {i-4 if i < 4 else 'Today'}: ${price:.2f} ({change:+.1f}%)")

# Bollinger Bands
sma_20_bb = hist_1y['Close'].rolling(20).mean()
std_20 = hist_1y['Close'].rolling(20).std()
upper_band = sma_20_bb + (std_20 * 2)
lower_band = sma_20_bb - (std_20 * 2)

bb_position = (current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])

print(f"\n📊 BOLLINGER BANDS ANALYSIS")
print("-" * 80)
print(f"Upper Band: ${upper_band.iloc[-1]:.2f}")
print(f"Middle (20 SMA): ${sma_20_bb.iloc[-1]:.2f}")
print(f"Lower Band: ${lower_band.iloc[-1]:.2f}")
print(f"Current Position: {bb_position:.1%} {'📍 Near Upper Band' if bb_position > 0.8 else '📍 Near Lower Band' if bb_position < 0.2 else '📍 Middle Range'}")

# Breakout Detection
is_at_resistance = (high_52w - current_price) / high_52w < 0.02  # Within 2% of high
is_above_mas = current_price > sma_20 and current_price > sma_50
volume_surge = volume_ratio > 1.5
momentum_positive = macd_histogram.iloc[-1] > 0 and rsi_14 > 50

# Calculate breakout score
breakout_score = 0
breakout_factors = []

if is_at_resistance:
    breakout_score += 20
    breakout_factors.append("✓ At 52-week high resistance")
else:
    breakout_factors.append("✗ Not at resistance level")

if current_price > high_1m:
    breakout_score += 20
    breakout_factors.append("✓ Above 1-month high")
else:
    breakout_factors.append("✗ Below recent highs")

if is_above_mas:
    breakout_score += 20
    breakout_factors.append("✓ Above key moving averages")
else:
    breakout_factors.append("✗ Mixed MA positioning")

if volume_surge:
    breakout_score += 25
    breakout_factors.append("✓ Volume surge detected")
else:
    breakout_factors.append("✗ Normal/Low volume")

if momentum_positive:
    breakout_score += 15
    breakout_factors.append("✓ Positive momentum")
else:
    breakout_factors.append("✗ Weak momentum")

# Extended analysis
extended_from_50ma = ((current_price - sma_50) / sma_50) * 100
extended_from_200ma = ((current_price - sma_200) / sma_200) * 100

print("\n" + "=" * 100)
print("🎯 BREAKOUT ANALYSIS SUMMARY")
print("=" * 100)

print(f"\nBreakout Score: {breakout_score}/100")
print("\nBreakout Checklist:")
for factor in breakout_factors:
    print(f"  {factor}")

print(f"\n📊 EXTENSION ANALYSIS")
print("-" * 80)
print(f"Extended from 50-day MA: {extended_from_50ma:+.1f}%")
print(f"Extended from 200-day MA: {extended_from_200ma:+.1f}%")
print(f"Days since 52-week high: {(hist_1y.index[-1] - hist_1y['High'].idxmax()).days}")

# Pattern Recognition
print(f"\n📊 PATTERN RECOGNITION")
print("-" * 80)

# Check for double top
recent_highs = hist_3m['High'].nlargest(5)
if len(recent_highs) >= 2:
    if abs(recent_highs.iloc[0] - recent_highs.iloc[1]) / recent_highs.iloc[0] < 0.02:
        print("⚠️ DOUBLE TOP PATTERN detected at ${:.2f}".format(recent_highs.iloc[0]))
    else:
        print("No double top pattern detected")

# Check for ascending triangle
lows_trend = np.polyfit(range(len(hist_1m['Low'])), hist_1m['Low'].values, 1)[0]
highs_trend = np.polyfit(range(len(hist_1m['High'])), hist_1m['High'].values, 1)[0]

if lows_trend > 0 and abs(highs_trend) < abs(lows_trend) * 0.3:
    print("📈 ASCENDING TRIANGLE pattern possible")
elif highs_trend < 0 and lows_trend < 0:
    print("📉 DESCENDING CHANNEL detected")
else:
    print("No clear pattern detected")

# Risk Assessment
print("\n" + "=" * 100)
print("⚠️ RISK ASSESSMENT FOR BREAKOUT TRADING")
print("=" * 100)

risks = []
opportunities = []

if extended_from_50ma > 20:
    risks.append(f"🔴 Overextended {extended_from_50ma:.1f}% above 50-day MA")
else:
    opportunities.append(f"🟢 Reasonable extension from 50-day MA")

if rsi_14 > 65:
    risks.append(f"🔴 RSI showing overbought conditions ({rsi_14:.1f})")
else:
    opportunities.append(f"🟢 RSI not overbought ({rsi_14:.1f})")

if bb_position > 0.9:
    risks.append("🔴 At upper Bollinger Band - potential reversal zone")
else:
    opportunities.append("🟢 Room to upper Bollinger Band")

if not volume_surge:
    risks.append("🔴 Lack of volume confirmation for breakout")
else:
    opportunities.append("🟢 Strong volume supporting move")

if is_at_resistance:
    risks.append("🔴 At major resistance (52-week high)")
else:
    opportunities.append("🟢 Not at major resistance")

print("\n📊 RISKS:")
for risk in risks:
    print(f"  {risk}")

print("\n📊 OPPORTUNITIES:")
for opp in opportunities:
    print(f"  {opp}")

# Final Verdict
print("\n" + "=" * 100)
print("🎯 FINAL VERDICT")
print("=" * 100)

if breakout_score >= 70:
    verdict = "STRONG BREAKOUT"
    recommendation = "Consider waiting for breakout confirmation before collar"
    emoji = "🚀"
elif breakout_score >= 50:
    verdict = "POSSIBLE BREAKOUT"
    recommendation = "Monitor closely, consider wider collar strikes"
    emoji = "⚡"
elif breakout_score >= 30:
    verdict = "NO CLEAR BREAKOUT"
    recommendation = "Good time for collar - stock at resistance"
    emoji = "⚠️"
else:
    verdict = "RESISTANCE/REVERSAL LIKELY"
    recommendation = "IDEAL time for collar strategy - protect gains"
    emoji = "🛡️"

print(f"\n{emoji} {verdict} (Score: {breakout_score}/100)")
print(f"\n💡 RECOMMENDATION: {recommendation}")

print(f"\n📋 SPECIFIC GUIDANCE FOR YOUR POSITION:")
print("-" * 80)
if breakout_score < 50:
    print("""
1. Stock is at 52-week HIGH RESISTANCE - not breaking out
2. Extended significantly from moving averages
3. Perfect timing for COLLAR implementation
4. High probability of consolidation or pullback
5. Protect your $700k+ position NOW

ACTION: Proceed with collar strategy as planned
""")
elif breakout_score >= 50 and breakout_score < 70:
    print("""
1. Mixed signals - could go either way
2. Consider implementing collar with WIDER strikes
3. Maybe use $200P/$270C instead of $210P/$260C
4. Give more room for potential breakout

ACTION: Implement collar but adjust strikes wider
""")
else:
    print("""
1. Breakout appears imminent
2. Consider WAITING 2-3 days for confirmation
3. If breaks above $240 with volume, new uptrend
4. Could then collar at higher levels

ACTION: Wait for breakout confirmation first
""")

print("=" * 100)
print("Analysis Complete")
print("=" * 100)