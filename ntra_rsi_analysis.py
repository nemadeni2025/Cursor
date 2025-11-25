#!/usr/bin/env python3
"""
NTRA RSI vs Price Analysis
Plotting RSI and stock price to identify overbought/oversold conditions
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
fig, axes = plt.subplots(3, 1, figsize=(16, 12))
fig.suptitle('NTRA: Price vs RSI Analysis - Overbought/Oversold Signals', 
             fontsize=16, fontweight='bold', y=0.995)

ticker = "NTRA"
stock = yf.Ticker(ticker)

# Get 1 year of data
print("Fetching NTRA data...")
hist_data = stock.history(period="1y")

# Calculate RSI
def calculate_rsi(data, period=14):
    """Calculate RSI indicator"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate multiple RSI periods
hist_data['RSI_14'] = calculate_rsi(hist_data['Close'], 14)
hist_data['RSI_9'] = calculate_rsi(hist_data['Close'], 9)
hist_data['RSI_21'] = calculate_rsi(hist_data['Close'], 21)

# Get current values
current_price = hist_data['Close'].iloc[-1]
current_rsi_14 = hist_data['RSI_14'].iloc[-1]
current_rsi_9 = hist_data['RSI_9'].iloc[-1]

print(f"\nCurrent Price: ${current_price:.2f}")
print(f"Current RSI (14): {current_rsi_14:.1f}")
print(f"Current RSI (9): {current_rsi_9:.1f}")

# PLOT 1: Price with RSI Overlay
ax1 = axes[0]
ax1_twin = ax1.twinx()

# Price line
price_line = ax1.plot(hist_data.index, hist_data['Close'], 
                      label='NTRA Price', linewidth=2, color='#2E86AB', zorder=3)

# RSI line on secondary axis
rsi_line = ax1_twin.plot(hist_data.index, hist_data['RSI_14'], 
                         label='RSI (14)', linewidth=2, color='#A23B72', alpha=0.7)

# RSI zones
ax1_twin.axhline(y=70, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='Overbought (70)')
ax1_twin.axhline(y=50, color='gray', linestyle='-', linewidth=1, alpha=0.3)
ax1_twin.axhline(y=30, color='green', linestyle='--', linewidth=1.5, alpha=0.5, label='Oversold (30)')

# Fill overbought/oversold zones
ax1_twin.fill_between(hist_data.index, 70, 100, alpha=0.1, color='red', label='Overbought Zone')
ax1_twin.fill_between(hist_data.index, 0, 30, alpha=0.1, color='green', label='Oversold Zone')

# Mark current point
ax1.scatter(hist_data.index[-1], current_price, color='red', s=100, zorder=5, 
           label=f'Current: ${current_price:.2f}')
ax1_twin.scatter(hist_data.index[-1], current_rsi_14, color='red', s=100, zorder=5,
                label=f'RSI: {current_rsi_14:.1f}')

# Mark significant RSI extremes
high_rsi = hist_data[hist_data['RSI_14'] > 75]
low_rsi = hist_data[hist_data['RSI_14'] < 25]

if len(high_rsi) > 0:
    ax1.scatter(high_rsi.index, high_rsi['Close'], color='red', s=50, alpha=0.6, 
               marker='v', label='Extreme Overbought', zorder=4)
if len(low_rsi) > 0:
    ax1.scatter(low_rsi.index, low_rsi['Close'], color='green', s=50, alpha=0.6,
               marker='^', label='Extreme Oversold', zorder=4)

ax1.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
ax1_twin.set_ylabel('RSI', fontsize=12, fontweight='bold')
ax1.set_title('NTRA Price vs RSI (14) - Overbought/Oversold Signals', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left', fontsize=9)
ax1_twin.legend(loc='upper right', fontsize=9)
ax1_twin.set_ylim(0, 100)

# Format x-axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))

# PLOT 2: RSI Divergence Analysis
ax2 = axes[1]

# Calculate price peaks and RSI peaks
price_peaks = []
rsi_peaks = []
price_troughs = []
rsi_troughs = []

# Find peaks and troughs
for i in range(20, len(hist_data) - 20):
    if (hist_data['Close'].iloc[i] == hist_data['Close'].iloc[i-20:i+20].max()):
        price_peaks.append((hist_data.index[i], hist_data['Close'].iloc[i]))
    if (hist_data['Close'].iloc[i] == hist_data['Close'].iloc[i-20:i+20].min()):
        price_troughs.append((hist_data.index[i], hist_data['Close'].iloc[i]))
    if (hist_data['RSI_14'].iloc[i] == hist_data['RSI_14'].iloc[i-20:i+20].max()):
        rsi_peaks.append((hist_data.index[i], hist_data['RSI_14'].iloc[i]))
    if (hist_data['RSI_14'].iloc[i] == hist_data['RSI_14'].iloc[i-20:i+20].min()):
        rsi_troughs.append((hist_data.index[i], hist_data['RSI_14'].iloc[i]))

# Plot price and RSI normalized
price_normalized = (hist_data['Close'] - hist_data['Close'].min()) / (hist_data['Close'].max() - hist_data['Close'].min()) * 100
rsi_normalized = hist_data['RSI_14']

ax2.plot(hist_data.index, price_normalized, label='Price (Normalized)', linewidth=2, color='#2E86AB')
ax2.plot(hist_data.index, rsi_normalized, label='RSI (14)', linewidth=2, color='#A23B72', alpha=0.7)

# Mark divergences
if len(price_peaks) >= 2 and len(rsi_peaks) >= 2:
    # Check for bearish divergence (price higher, RSI lower)
    last_price_peak = price_peaks[-1]
    prev_price_peak = price_peaks[-2] if len(price_peaks) >= 2 else None
    
    if prev_price_peak:
        last_rsi = hist_data.loc[last_price_peak[0], 'RSI_14']
        prev_rsi = hist_data.loc[prev_price_peak[0], 'RSI_14']
        
        if last_price_peak[1] > prev_price_peak[1] and last_rsi < prev_rsi:
            ax2.annotate('Bearish Divergence', 
                        xy=(last_price_peak[0], price_normalized.loc[last_price_peak[0]]),
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                        fontsize=10, fontweight='bold', color='red')

ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5)
ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5)
ax2.set_ylabel('Normalized Value', fontsize=12, fontweight='bold')
ax2.set_title('RSI Divergence Analysis - Price vs Momentum', fontsize=14, fontweight='bold')
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))

# PLOT 3: RSI Histogram and Distribution
ax3 = axes[2]

# Create histogram
ax3.hist(hist_data['RSI_14'].dropna(), bins=50, alpha=0.7, color='#A23B72', edgecolor='black')
ax3.axvline(x=current_rsi_14, color='red', linestyle='-', linewidth=3, 
           label=f'Current RSI: {current_rsi_14:.1f}')
ax3.axvline(x=70, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Overbought (70)')
ax3.axvline(x=50, color='gray', linestyle='-', linewidth=1, alpha=0.5)
ax3.axvline(x=30, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Oversold (30)')

# Calculate percentiles
rsi_percentiles = hist_data['RSI_14'].quantile([0.05, 0.25, 0.50, 0.75, 0.95])
current_percentile = (hist_data['RSI_14'] < current_rsi_14).sum() / len(hist_data['RSI_14'].dropna()) * 100

ax3.set_xlabel('RSI Value', fontsize=12, fontweight='bold')
ax3.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax3.set_title(f'RSI Distribution - Current at {current_percentile:.1f}th Percentile', 
             fontsize=14, fontweight='bold')
ax3.legend(loc='best', fontsize=9)
ax3.grid(True, alpha=0.3, axis='y')

# Add text annotations
textstr = f'RSI Statistics:\n'
textstr += f'Current: {current_rsi_14:.1f} ({current_percentile:.1f}th percentile)\n'
textstr += f'Mean: {hist_data["RSI_14"].mean():.1f}\n'
textstr += f'Max: {hist_data["RSI_14"].max():.1f}\n'
textstr += f'Min: {hist_data["RSI_14"].min():.1f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax3.text(0.02, 0.98, textstr, transform=ax3.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('/workspace/ntra_rsi_analysis.png', dpi=150, bbox_inches='tight')
print("\nChart saved to: ntra_rsi_analysis.png")

# Additional Analysis
print("\n" + "=" * 100)
print("RSI ANALYSIS SUMMARY")
print("=" * 100)

# Find RSI extremes and what happened next
print("\n📊 HISTORICAL RSI EXTREMES & SUBSEQUENT PRICE ACTION")
print("-" * 80)

# Find all times RSI was above 75
extreme_overbought = hist_data[hist_data['RSI_14'] > 75]
print(f"\nTimes RSI > 75 (Extreme Overbought): {len(extreme_overbought)} occurrences")

if len(extreme_overbought) > 0:
    print("\nWhat happened after extreme overbought readings:")
    for idx, row in extreme_overbought.head(5).iterrows():
        # Find price 5, 10, 20 days later
        future_idx = hist_data.index.get_loc(idx)
        if future_idx + 20 < len(hist_data):
            price_5d = hist_data['Close'].iloc[future_idx + 5]
            price_10d = hist_data['Close'].iloc[future_idx + 10]
            price_20d = hist_data['Close'].iloc[future_idx + 20]
            change_5d = ((price_5d - row['Close']) / row['Close']) * 100
            change_10d = ((price_10d - row['Close']) / row['Close']) * 100
            change_20d = ((price_20d - row['Close']) / row['Close']) * 100
            
            print(f"\n{idx.strftime('%Y-%m-%d')}: RSI {row['RSI_14']:.1f}, Price ${row['Close']:.2f}")
            print(f"  5 days later: {change_5d:+.1f}%")
            print(f"  10 days later: {change_10d:+.1f}%")
            print(f"  20 days later: {change_20d:+.1f}%")

# Find all times RSI was below 25
extreme_oversold = hist_data[hist_data['RSI_14'] < 25]
print(f"\n\nTimes RSI < 25 (Extreme Oversold): {len(extreme_oversold)} occurrences")

if len(extreme_oversold) > 0:
    print("\nWhat happened after extreme oversold readings:")
    for idx, row in extreme_oversold.head(5).iterrows():
        future_idx = hist_data.index.get_loc(idx)
        if future_idx + 20 < len(hist_data):
            price_5d = hist_data['Close'].iloc[future_idx + 5]
            price_10d = hist_data['Close'].iloc[future_idx + 10]
            price_20d = hist_data['Close'].iloc[future_idx + 20]
            change_5d = ((price_5d - row['Close']) / row['Close']) * 100
            change_10d = ((price_10d - row['Close']) / row['Close']) * 100
            change_20d = ((price_20d - row['Close']) / row['Close']) * 100
            
            print(f"\n{idx.strftime('%Y-%m-%d')}: RSI {row['RSI_14']:.1f}, Price ${row['Close']:.2f}")
            print(f"  5 days later: {change_5d:+.1f}%")
            print(f"  10 days later: {change_10d:+.1f}%")
            print(f"  20 days later: {change_20d:+.1f}%")

# Current RSI analysis
print("\n" + "=" * 100)
print("CURRENT RSI ANALYSIS")
print("=" * 100)

print(f"\nCurrent Price: ${current_price:.2f}")
print(f"Current RSI (14): {current_rsi_14:.1f}")
print(f"Current RSI (9): {current_rsi_9:.1f}")

# Determine RSI status
if current_rsi_14 > 70:
    status = "🔴 EXTREMELY OVERBOUGHT"
    recommendation = "High probability of pullback"
elif current_rsi_14 > 60:
    status = "🟠 OVERBOUGHT"
    recommendation = "Caution - may be topping"
elif current_rsi_14 < 30:
    status = "🟢 OVERSOLD"
    recommendation = "Potential bounce opportunity"
elif current_rsi_14 < 40:
    status = "🟡 NEAR OVERSOLD"
    recommendation = "Watch for support"
else:
    status = "⚪ NEUTRAL"
    recommendation = "No extreme signal"

print(f"\nRSI Status: {status}")
print(f"Recommendation: {recommendation}")

# Calculate how often current RSI level leads to declines
similar_rsi = hist_data[(hist_data['RSI_14'] > current_rsi_14 - 5) & 
                        (hist_data['RSI_14'] < current_rsi_14 + 5)]
if len(similar_rsi) > 10:
    future_returns = []
    for idx in similar_rsi.index[:-10]:  # Exclude last 10 to have future data
        future_idx = hist_data.index.get_loc(idx)
        if future_idx + 10 < len(hist_data):
            future_return = ((hist_data['Close'].iloc[future_idx + 10] - 
                            hist_data.loc[idx, 'Close']) / hist_data.loc[idx, 'Close']) * 100
            future_returns.append(future_return)
    
    if future_returns:
        avg_return = np.mean(future_returns)
        positive_pct = (np.array(future_returns) > 0).sum() / len(future_returns) * 100
        print(f"\nHistorical Performance at Similar RSI Levels:")
        print(f"  Average 10-day return: {avg_return:+.1f}%")
        print(f"  Positive returns: {positive_pct:.1f}% of the time")

print("\n" + "=" * 100)
print("Chart visualization complete!")
print("=" * 100)

plt.show()
