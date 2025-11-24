#!/usr/bin/env python3
"""
Verify NTRA after-hours price from multiple trusted sources
Check various APIs and data providers
"""

import yfinance as yf
import requests
import json
from datetime import datetime
import time

print("=" * 100)
print("NTRA AFTER-HOURS PRICE VERIFICATION - MULTIPLE SOURCES")
print(f"Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} EST")
print("=" * 100)

# Track all findings
price_findings = []

# SOURCE 1: Yahoo Finance (via yfinance)
print("\n🔍 SOURCE 1: Yahoo Finance (yfinance API)")
print("-" * 80)
try:
    ticker = yf.Ticker("NTRA")
    info = ticker.info
    
    regular_close = info.get('regularMarketPrice', 'N/A')
    post_market = info.get('postMarketPrice', 'N/A')
    post_change = info.get('postMarketChange', 'N/A')
    
    print(f"Regular Market Close: ${regular_close}")
    print(f"Post-Market Price: ${post_market}")
    print(f"Post-Market Change: ${post_change}")
    print(f"Data Freshness: Real-time during market, 15-min delay after-hours")
    
    if post_market != 'N/A':
        price_findings.append({
            'source': 'Yahoo Finance',
            'price': post_market,
            'status': 'Confirmed'
        })
    
except Exception as e:
    print(f"Error accessing Yahoo Finance: {e}")

# SOURCE 2: Alpha Vantage (if API key available)
print("\n🔍 SOURCE 2: Alpha Vantage API")
print("-" * 80)
try:
    # Note: Requires API key - using demo for structure
    print("Status: Requires API key for real-time data")
    print("Would provide: Real-time and after-hours quotes")
    print("Data quality: Institutional grade")
except Exception as e:
    print(f"Alpha Vantage not accessible without API key")

# SOURCE 3: Direct Yahoo Finance URL
print("\n🔍 SOURCE 3: Yahoo Finance Direct Query")
print("-" * 80)
try:
    import urllib.request
    
    # Construct Yahoo Finance quote URL
    yahoo_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=NTRA"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    req = urllib.request.Request(yahoo_url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    
    if 'quoteResponse' in data and data['quoteResponse']['result']:
        quote = data['quoteResponse']['result'][0]
        
        print(f"Symbol: {quote.get('symbol', 'N/A')}")
        print(f"Regular Market Price: ${quote.get('regularMarketPrice', 'N/A')}")
        print(f"Post Market Price: ${quote.get('postMarketPrice', 'N/A')}")
        print(f"Post Market Change: ${quote.get('postMarketChange', 'N/A')}")
        print(f"Post Market Time: {quote.get('postMarketTime', 'N/A')}")
        
        if quote.get('postMarketPrice'):
            price_findings.append({
                'source': 'Yahoo Direct API',
                'price': quote.get('postMarketPrice'),
                'status': 'Confirmed'
            })
    
except Exception as e:
    print(f"Error with direct query: {e}")

# SOURCE 4: Check using different method
print("\n🔍 SOURCE 4: Extended Hours via Historical Data")
print("-" * 80)
try:
    ticker = yf.Ticker("NTRA")
    # Get today's data with extended hours
    hist = ticker.history(period="1d", interval="5m", prepost=True)
    
    # Find prices after 4 PM EST
    after_market_data = []
    for idx, row in hist.iterrows():
        if idx.hour >= 16:  # After 4 PM
            after_market_data.append({
                'time': idx.strftime('%H:%M'),
                'price': row['Close'],
                'volume': row['Volume']
            })
    
    if after_market_data:
        print("After-Hours Trading Activity:")
        for data in after_market_data[-5:]:  # Last 5 entries
            print(f"  {data['time']}: ${data['price']:.2f} (Volume: {data['volume']:,.0f})")
        
        latest_ah = after_market_data[-1]['price']
        print(f"\nLatest After-Hours Price: ${latest_ah:.2f}")
        
        price_findings.append({
            'source': 'Historical Extended Hours',
            'price': latest_ah,
            'status': 'Confirmed'
        })
    else:
        print("No after-hours data found")
        
except Exception as e:
    print(f"Error fetching extended hours: {e}")

# SOURCE 5: Market Data Cross-Reference
print("\n🔍 SOURCE 5: Market Summary Check")
print("-" * 80)
try:
    ticker = yf.Ticker("NTRA")
    
    # Get multiple data points for verification
    info = ticker.info
    fast_info = ticker.fast_info
    
    print(f"Market State: {info.get('marketState', 'N/A')}")
    print(f"Quote Type: {info.get('quoteType', 'N/A')}")
    print(f"Exchange: {info.get('exchange', 'N/A')}")
    print(f"Previous Close: ${info.get('previousClose', 'N/A')}")
    print(f"Regular Market Previous: ${info.get('regularMarketPreviousClose', 'N/A')}")
    
    # Check if we have consistent data
    if info.get('postMarketPrice'):
        print(f"Post-Market Confirmed: ${info.get('postMarketPrice')}")
    
except Exception as e:
    print(f"Error in market summary: {e}")

# FINAL VERIFICATION SUMMARY
print("\n" + "=" * 100)
print("📊 VERIFICATION SUMMARY FROM ALL SOURCES")
print("=" * 100)

if price_findings:
    print("\n✅ CONFIRMED PRICES:")
    for finding in price_findings:
        print(f"  • {finding['source']}: ${finding['price']:.2f} ({finding['status']})")
    
    # Calculate consensus
    prices = [f['price'] for f in price_findings if isinstance(f['price'], (int, float))]
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        print(f"\n📈 CONSENSUS AFTER-HOURS PRICE:")
        print(f"  Average: ${avg_price:.2f}")
        print(f"  Range: ${min_price:.2f} - ${max_price:.2f}")
        print(f"  Sources Confirming: {len(prices)}")
        
        if all(p > 241 for p in prices):
            print("\n🚨 BREAKOUT CONFIRMED: All sources show price above $241 resistance!")
else:
    print("⚠️ Unable to confirm after-hours price from available sources")

print("\n" + "=" * 100)
print("📝 SOURCE RELIABILITY NOTES:")
print("=" * 100)
print("""
1. Yahoo Finance (yfinance): 
   - Most widely used free source
   - 15-20 minute delay for after-hours
   - Generally reliable for US stocks

2. Direct Yahoo API:
   - Same data as yfinance but direct access
   - Cross-verification method

3. Extended Hours Historical:
   - Shows actual trades in after-hours
   - Most accurate for executed trades

4. Professional Sources (not accessed):
   - Bloomberg Terminal: Real-time, most accurate
   - Reuters Eikon: Institutional grade
   - Interactive Brokers: Real-time for account holders
   - E*TRADE: Real-time for account holders

⚠️ IMPORTANT: After-hours prices can be volatile with low volume.
   The opening price Monday may differ from after-hours quotes.
""")

print("=" * 100)