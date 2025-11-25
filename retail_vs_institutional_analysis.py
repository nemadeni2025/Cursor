#!/usr/bin/env python3
"""
Retail vs Institutional Volume Analysis for NTRA
Analyzing trading patterns to identify who's buying/selling
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("NTRA: RETAIL vs INSTITUTIONAL VOLUME ANALYSIS")
print("=" * 100)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 100)

ticker = "NTRA"
stock = yf.Ticker(ticker)

# Get recent trading data
print("\n📊 METHOD 1: ORDER SIZE ANALYSIS")
print("-" * 80)

try:
    # Get intraday data to analyze trade sizes
    hist_1d = stock.history(period="1d", interval="1m")
    
    if len(hist_1d) > 0:
        # Calculate volume patterns
        total_volume = hist_1d['Volume'].sum()
        avg_volume_per_minute = hist_1d['Volume'].mean()
        median_volume = hist_1d['Volume'].median()
        
        # Large blocks (likely institutional)
        large_blocks = hist_1d[hist_1d['Volume'] > avg_volume_per_minute * 3]
        institutional_volume = large_blocks['Volume'].sum()
        institutional_pct = (institutional_volume / total_volume) * 100
        
        # Small trades (likely retail)
        small_trades = hist_1d[hist_1d['Volume'] < avg_volume_per_minute * 0.5]
        retail_volume = small_trades['Volume'].sum()
        retail_pct = (retail_volume / total_volume) * 100
        
        print(f"Total Volume Today: {total_volume:,.0f}")
        print(f"Average per Minute: {avg_volume_per_minute:,.0f}")
        print(f"Median per Minute: {median_volume:,.0f}")
        print(f"\nLarge Block Trades (>3x avg): {len(large_blocks)} occurrences")
        print(f"Institutional Volume: {institutional_volume:,.0f} ({institutional_pct:.1f}%)")
        print(f"\nSmall Trades (<0.5x avg): {len(small_trades)} occurrences")
        print(f"Retail Volume: {retail_volume:,.0f} ({retail_pct:.1f}%)")
        
        # Block size analysis
        if len(large_blocks) > 0:
            avg_block_size = large_blocks['Volume'].mean()
            print(f"\nAverage Block Size: {avg_block_size:,.0f} shares")
            print(f"Typical Institutional Block: 10,000+ shares")
            print(f"Typical Retail Trade: 100-1,000 shares")
            
            if avg_block_size > 10000:
                print("✅ Large blocks detected - Likely institutional")
            elif avg_block_size > 5000:
                print("⚠️ Medium blocks - Mixed retail/institutional")
            else:
                print("📱 Smaller blocks - More retail")
                
except Exception as e:
    print(f"Error in order size analysis: {e}")

# METHOD 2: Time-of-Day Analysis
print("\n📊 METHOD 2: TIME-OF-DAY PATTERN ANALYSIS")
print("-" * 80)

try:
    hist_1d = stock.history(period="1d", interval="5m", prepost=True)
    
    if len(hist_1d) > 0:
        hist_1d['Hour'] = hist_1d.index.hour
        hist_1d['Minute'] = hist_1d.index.minute
        
        # Define trading periods
        periods = {
            'Pre-Market (4:00-9:30)': (4, 9, 30),
            'Market Open (9:30-10:00)': (9, 10, 0),
            'Morning (10:00-12:00)': (10, 12, 0),
            'Midday (12:00-14:00)': (12, 14, 0),
            'Power Hour (14:00-15:00)': (14, 15, 0),
            'Close (15:00-16:00)': (15, 16, 0),
            'After-Hours (16:00-20:00)': (16, 20, 0)
        }
        
        print("Volume by Trading Period:")
        print("-" * 60)
        
        for period_name, (start_hour, end_hour, end_min) in periods.items():
            if end_min == 0:
                period_data = hist_1d[(hist_1d['Hour'] >= start_hour) & (hist_1d['Hour'] < end_hour)]
            else:
                period_data = hist_1d[((hist_1d['Hour'] == start_hour) & (hist_1d['Minute'] >= 0)) | 
                                     ((hist_1d['Hour'] < end_hour) | ((hist_1d['Hour'] == end_hour) & (hist_1d['Minute'] < end_min)))]
            
            if len(period_data) > 0:
                period_volume = period_data['Volume'].sum()
                period_pct = (period_volume / hist_1d['Volume'].sum()) * 100
                avg_trade_size = period_data['Volume'].mean()
                
                # Classify
                if period_name in ['Pre-Market', 'After-Hours']:
                    trader_type = "Institutional (Extended Hours)"
                elif period_name in ['Market Open', 'Close']:
                    trader_type = "Mixed (High Activity)"
                elif avg_trade_size > 5000:
                    trader_type = "Institutional (Large Blocks)"
                else:
                    trader_type = "Retail (Small Trades)"
                
                print(f"{period_name:25s}: {period_volume:>10,.0f} ({period_pct:>5.1f}%) - {trader_type}")
                
except Exception as e:
    print(f"Error in time analysis: {e}")

# FINAL ASSESSMENT
print("\n" + "=" * 100)
print("📊 RETAIL vs INSTITUTIONAL ASSESSMENT")
print("=" * 100)

try:
    # Get today's data
    hist_today = stock.history(period="1d", interval="1m")
    
    if len(hist_today) > 0:
        total_vol = hist_today['Volume'].sum()
        avg_trade = hist_today['Volume'].mean()
        
        # Scoring system
        retail_score = 0
        institutional_score = 0
        
        # Factor 1: Average trade size
        if avg_trade < 2000:
            retail_score += 2
        elif avg_trade > 10000:
            institutional_score += 2
        else:
            retail_score += 1
            institutional_score += 1
        
        # Factor 2: Large blocks
        large_blocks = hist_today[hist_today['Volume'] > avg_trade * 3]
        if len(large_blocks) > 10:
            institutional_score += 2
        elif len(large_blocks) > 5:
            institutional_score += 1
        
        # Factor 3: After-hours activity
        after_hours = hist_today[hist_today.index.hour >= 16]
        if len(after_hours) > 0 and after_hours['Volume'].sum() > total_vol * 0.05:
            institutional_score += 1
        
        print(f"\nRetail Score: {retail_score}/5")
        print(f"Institutional Score: {institutional_score}/5")
        
        if institutional_score > retail_score:
            print("\n🎯 ASSESSMENT: Primarily INSTITUTIONAL trading")
            print("   → Higher manipulation risk")
        elif retail_score > institutional_score:
            print("\n📱 ASSESSMENT: Primarily RETAIL trading")
            print("   → Lower manipulation risk")
        else:
            print("\n⚖️ ASSESSMENT: MIXED retail/institutional")
            
except Exception as e:
    print(f"Error in final assessment: {e}")

print("\n" + "=" * 100)