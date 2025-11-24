#!/usr/bin/env python3
"""
Detailed Options Chain Analysis for Natera (NTRA)
Shows actual available options with current bid/ask spreads
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

print("=" * 100)
print("DETAILED OPTIONS CHAIN ANALYSIS FOR NATERA (NTRA)")
print("=" * 100)
print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Position: 3,000 shares (30 option contracts)")
print("=" * 100)

# Fetch current stock data
TICKER = "NTRA"
SHARES = 3000
stock = yf.Ticker(TICKER)

# Get current price
try:
    info = stock.info
    current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose', 0)
except:
    current_price = stock.history(period="1d")['Close'].iloc[-1]

print(f"\n📊 CURRENT STOCK PRICE: ${current_price:.2f}")
print(f"📊 POSITION VALUE: ${current_price * SHARES:,.2f}")

# Get available expirations
expirations = stock.options
print(f"\n📅 AVAILABLE EXPIRATION DATES: {len(expirations)} total")

# Analyze next 2-3 expirations for practical hedging
today = datetime.now()
expirations_to_analyze = []

for exp_str in expirations[:5]:
    exp_date = datetime.strptime(exp_str, '%Y-%m-%d')
    days_to_exp = (exp_date - today).days
    if days_to_exp > 0 and days_to_exp <= 90:
        expirations_to_analyze.append((exp_str, days_to_exp))

print("\nAnalyzing options for the following expirations:")
for exp, days in expirations_to_analyze[:3]:
    print(f"  • {exp} ({days} days)")

# Analyze each expiration
for exp_str, days_to_exp in expirations_to_analyze[:2]:  # Focus on next 2 expirations
    print(f"\n{'='*100}")
    print(f"OPTIONS CHAIN FOR {exp_str} (Expires in {days_to_exp} days)")
    print(f"{'='*100}")
    
    # Get options chain
    opt_chain = stock.option_chain(exp_str)
    
    # PUTS FOR HEDGING
    print(f"\n🛡️ PROTECTIVE PUT OPTIONS")
    print("-" * 80)
    puts = opt_chain.puts
    
    # Filter for relevant strikes (85% to 100% of current price)
    relevant_puts = puts[(puts['strike'] >= current_price * 0.85) & 
                         (puts['strike'] <= current_price * 1.00)]
    
    if len(relevant_puts) > 0:
        # Select columns to display
        put_display = relevant_puts[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']].copy()
        put_display['% OTM'] = ((current_price - put_display['strike']) / current_price * 100).round(1)
        put_display['Total Cost (30 contracts)'] = (put_display['lastPrice'] * 30 * 100).round(0)
        
        # Sort by strike descending (ATM to OTM)
        put_display = put_display.sort_values('strike', ascending=False).head(5)
        
        print("\nMost Relevant Put Options for Hedging:")
        print(put_display.to_string(index=False))
        
        # Highlight recommended put
        recommended_put = put_display.iloc[len(put_display)//2]  # Middle strike
        print(f"\n✅ Recommended Put: Strike ${recommended_put['strike']:.2f}")
        print(f"   • Premium: ${recommended_put['lastPrice']:.2f} per share")
        print(f"   • Total Cost for 3,000 shares: ${recommended_put['Total Cost (30 contracts)']:,.0f}")
        print(f"   • Protection below: ${recommended_put['strike']:.2f}")
        print(f"   • Max Loss if stock drops to zero: ${(current_price - recommended_put['strike'] + recommended_put['lastPrice']) * SHARES:,.0f}")
    
    # CALLS FOR COVERED CALL
    print(f"\n💰 COVERED CALL OPTIONS")
    print("-" * 80)
    calls = opt_chain.calls
    
    # Filter for relevant strikes (100% to 115% of current price)
    relevant_calls = calls[(calls['strike'] >= current_price * 1.00) & 
                          (calls['strike'] <= current_price * 1.15)]
    
    if len(relevant_calls) > 0:
        # Select columns to display
        call_display = relevant_calls[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']].copy()
        call_display['% OTM'] = ((call_display['strike'] - current_price) / current_price * 100).round(1)
        call_display['Total Income (30 contracts)'] = (call_display['lastPrice'] * 30 * 100).round(0)
        
        # Sort by strike ascending (ATM to OTM)
        call_display = call_display.sort_values('strike').head(5)
        
        print("\nMost Relevant Call Options for Income:")
        print(call_display.to_string(index=False))
        
        # Highlight recommended call
        recommended_call = call_display.iloc[2] if len(call_display) > 2 else call_display.iloc[-1]
        print(f"\n✅ Recommended Call: Strike ${recommended_call['strike']:.2f}")
        print(f"   • Premium: ${recommended_call['lastPrice']:.2f} per share")
        print(f"   • Total Income for 3,000 shares: ${recommended_call['Total Income (30 contracts)']:,.0f}")
        print(f"   • Called away at: ${recommended_call['strike']:.2f}")
        print(f"   • Max Gain if called: ${(recommended_call['strike'] - current_price + recommended_call['lastPrice']) * SHARES:,.0f}")
    
    # COLLAR STRATEGY
    print(f"\n🔄 COLLAR STRATEGY (Protective Put + Covered Call)")
    print("-" * 80)
    
    if len(relevant_puts) > 0 and len(relevant_calls) > 0:
        # Select a balanced collar
        collar_put = relevant_puts[relevant_puts['strike'] <= current_price * 0.95].iloc[0] if len(relevant_puts[relevant_puts['strike'] <= current_price * 0.95]) > 0 else relevant_puts.iloc[-1]
        collar_call = relevant_calls[relevant_calls['strike'] >= current_price * 1.05].iloc[0] if len(relevant_calls[relevant_calls['strike'] >= current_price * 1.05]) > 0 else relevant_calls.iloc[0]
        
        net_cost = (collar_put['lastPrice'] - collar_call['lastPrice']) * SHARES
        
        print(f"Recommended Collar:")
        print(f"  • Buy Put @ ${collar_put['strike']:.2f} (cost: ${collar_put['lastPrice']:.2f}/share)")
        print(f"  • Sell Call @ ${collar_call['strike']:.2f} (income: ${collar_call['lastPrice']:.2f}/share)")
        print(f"  • Net Cost: ${net_cost:,.2f} ({net_cost/SHARES:.2f}/share)")
        print(f"  • Protection Range: ${collar_put['strike']:.2f} to ${collar_call['strike']:.2f}")
        print(f"  • Max Loss: ${(current_price - collar_put['strike']) * SHARES + net_cost:,.0f}")
        print(f"  • Max Gain: ${(collar_call['strike'] - current_price) * SHARES - net_cost:,.0f}")

# Summary recommendations
print(f"\n{'='*100}")
print("EXECUTIVE SUMMARY & ACTION ITEMS")
print(f"{'='*100}")

print(f"""
📊 POSITION OVERVIEW:
   • Current Stock Price: ${current_price:.2f}
   • Position: 3,000 shares
   • Position Value: ${current_price * SHARES:,.2f}
   • Options Contracts Needed: 30

🎯 TOP 3 RECOMMENDED STRATEGIES:

1. PROTECTIVE PUT (Conservative)
   • Purpose: Maximum downside protection
   • Target Strike: 5-10% OTM
   • Expiration: 30-60 days
   • Estimated Cost: 2-4% of position value
   • Best for: Bearish outlook or high uncertainty

2. COVERED CALL (Income Generation)
   • Purpose: Generate premium income
   • Target Strike: 5-10% OTM  
   • Expiration: 30-45 days
   • Estimated Income: 1-3% of position value
   • Best for: Neutral to slightly bullish outlook

3. COLLAR (Balanced Protection)
   • Purpose: Low-cost hedging
   • Put Strike: 5-10% OTM, Call Strike: 5-10% OTM
   • Expiration: 45-60 days
   • Net Cost: Near zero or small debit
   • Best for: Seeking protection without large premium outlay

⚡ IMMEDIATE NEXT STEPS:
   1. Review the specific strikes and premiums above
   2. Check current bid-ask spreads during market hours
   3. Place limit orders (not market orders)
   4. Start with partial position if uncertain
   5. Set calendar reminders for expiration management

⚠️ RISK DISCLAIMER:
   Options involve risk and are not suitable for all investors.
   Prices shown are indicative and will vary during market hours.
   Consult with your financial advisor before trading options.
""")

print("=" * 100)
print("Analysis Complete")
print("=" * 100)