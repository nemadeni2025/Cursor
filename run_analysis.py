#!/usr/bin/env python3
"""
Natera Options Hedging Analysis
Analyzing hedging strategies for 3,000 shares of NTER
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

print("=" * 80)
print("NATERA (NTER) OPTIONS HEDGING ANALYSIS")
print("=" * 80)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Position: 3,000 shares")
print("=" * 80)

# Portfolio Parameters
SHARES_OWNED = 3000
TICKER = "NTRA"  # Correct ticker for Natera

# Fetch current stock data
print("\n📊 FETCHING CURRENT MARKET DATA...")
stock = yf.Ticker(TICKER)

# Get current stock price and info
try:
    info = stock.info
    current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose', 0)
except Exception as e:
    print(f"Note: Using last available price due to market hours")
    current_price = stock.history(period="1d")['Close'].iloc[-1]

# Get stock info
stock_info = {
    'Symbol': TICKER,
    'Company Name': stock.info.get('longName', 'Natera Inc.'),
    'Current Price': current_price,
    'Shares Owned': SHARES_OWNED,
    'Position Value': current_price * SHARES_OWNED,
    '52 Week High': stock.info.get('fiftyTwoWeekHigh', 'N/A'),
    '52 Week Low': stock.info.get('fiftyTwoWeekLow', 'N/A'),
    'Beta': stock.info.get('beta', 'N/A')
}

# Display position summary
print("\n📈 POSITION SUMMARY")
print("-" * 60)
for key, value in stock_info.items():
    if key == 'Position Value' and isinstance(value, (int, float)):
        print(f"{key}: ${value:,.2f}")
    elif key in ['Current Price', '52 Week High', '52 Week Low'] and isinstance(value, (int, float)):
        print(f"{key}: ${value:.2f}")
    else:
        print(f"{key}: {value}")

# Fetch historical data for volatility analysis
print("\n📊 VOLATILITY ANALYSIS")
print("-" * 60)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
hist_data = stock.history(start=start_date, end=end_date)

# Calculate returns and volatility
hist_data['Daily_Return'] = hist_data['Close'].pct_change()
daily_volatility = hist_data['Daily_Return'].std()
annual_volatility = daily_volatility * np.sqrt(252)

# Calculate different period volatilities
volatility_30d = hist_data['Daily_Return'].tail(30).std() * np.sqrt(252)
volatility_60d = hist_data['Daily_Return'].tail(60).std() * np.sqrt(252)
volatility_90d = hist_data['Daily_Return'].tail(90).std() * np.sqrt(252)

print(f"Annual Historical Volatility: {annual_volatility:.1%}")
print(f"30-Day Volatility: {volatility_30d:.1%}")
print(f"60-Day Volatility: {volatility_60d:.1%}")
print(f"90-Day Volatility: {volatility_90d:.1%}")
print(f"\nDaily Value at Risk (95% confidence): ${current_price * 1.65 * daily_volatility * SHARES_OWNED:,.0f}")
print(f"Monthly Value at Risk (95% confidence): ${current_price * 1.65 * daily_volatility * np.sqrt(21) * SHARES_OWNED:,.0f}")

# Get available options
print("\n📅 AVAILABLE OPTIONS EXPIRATIONS")
print("-" * 60)
try:
    expirations = stock.options
    print(f"Total available expiration dates: {len(expirations)}")
    if len(expirations) > 0:
        print(f"Next 5 expirations: {expirations[:5]}")
        
        # Select expiration dates for analysis
        target_dates = []
        today = datetime.now()
        
        for exp in expirations[:8]:
            exp_date = datetime.strptime(exp, '%Y-%m-%d')
            days_to_exp = (exp_date - today).days
            if 20 <= days_to_exp <= 120:
                target_dates.append({
                    'expiration': exp,
                    'days_to_expiration': days_to_exp,
                    'exp_date': exp_date
                })
        
        if target_dates:
            print(f"\nSelected expiration dates for hedging analysis:")
            for td in target_dates[:3]:
                print(f"  • {td['expiration']}: {td['days_to_expiration']} days")
except Exception as e:
    print(f"Note: Options data may be limited during market hours")
    expirations = []

# Analyze specific strategies
print("\n" + "=" * 80)
print("HEDGING STRATEGY RECOMMENDATIONS")
print("=" * 80)

position_value = current_price * SHARES_OWNED
contracts_needed = SHARES_OWNED / 100

# Strategy 1: Protective Put
print("\n🛡️ STRATEGY 1: PROTECTIVE PUT")
print("-" * 60)
put_strike_90 = current_price * 0.90
put_strike_95 = current_price * 0.95
put_premium_estimate = current_price * 0.03  # Estimated 3% premium

print(f"Purpose: Protect against downside while maintaining upside potential")
print(f"\nRecommended Strikes:")
print(f"  • 10% OTM Put: ${put_strike_90:.2f}")
print(f"    - Estimated cost: ${put_premium_estimate * SHARES_OWNED:,.2f}")
print(f"    - Protection below: ${put_strike_90:.2f}")
print(f"    - Max loss: ${(current_price - put_strike_90 + put_premium_estimate) * SHARES_OWNED:,.2f}")
print(f"\n  • 5% OTM Put: ${put_strike_95:.2f}")
print(f"    - Estimated cost: ${put_premium_estimate * 1.5 * SHARES_OWNED:,.2f}")
print(f"    - Protection below: ${put_strike_95:.2f}")
print(f"    - Max loss: ${(current_price - put_strike_95 + put_premium_estimate * 1.5) * SHARES_OWNED:,.2f}")

# Strategy 2: Covered Call
print("\n💰 STRATEGY 2: COVERED CALL")
print("-" * 60)
call_strike_105 = current_price * 1.05
call_strike_110 = current_price * 1.10
call_premium_estimate = current_price * 0.02  # Estimated 2% premium

print(f"Purpose: Generate income while potentially selling at a profit")
print(f"\nRecommended Strikes:")
print(f"  • 5% OTM Call: ${call_strike_105:.2f}")
print(f"    - Estimated income: ${call_premium_estimate * 1.5 * SHARES_OWNED:,.2f}")
print(f"    - If called away, gain: ${(call_strike_105 - current_price + call_premium_estimate * 1.5) * SHARES_OWNED:,.2f}")
print(f"\n  • 10% OTM Call: ${call_strike_110:.2f}")
print(f"    - Estimated income: ${call_premium_estimate * SHARES_OWNED:,.2f}")
print(f"    - If called away, gain: ${(call_strike_110 - current_price + call_premium_estimate) * SHARES_OWNED:,.2f}")

# Strategy 3: Collar
print("\n🔄 STRATEGY 3: COLLAR (Put + Call)")
print("-" * 60)
print(f"Purpose: Low-cost protection with limited upside")
print(f"\nRecommended Combination:")
print(f"  • Buy Put @ ${put_strike_90:.2f} (cost: ~${put_premium_estimate * SHARES_OWNED:,.2f})")
print(f"  • Sell Call @ ${call_strike_110:.2f} (income: ~${call_premium_estimate * SHARES_OWNED:,.2f})")
print(f"  • Net cost: ~${(put_premium_estimate - call_premium_estimate) * SHARES_OWNED:,.2f}")
print(f"  • Protected range: ${put_strike_90:.2f} to ${call_strike_110:.2f}")
print(f"  • Max loss: ${(current_price - put_strike_90) * SHARES_OWNED:,.2f}")
print(f"  • Max gain: ${(call_strike_110 - current_price) * SHARES_OWNED:,.2f}")

# Risk Analysis
print("\n" + "=" * 80)
print("RISK ANALYSIS & SCENARIOS")
print("=" * 80)

# Calculate probability ranges
one_std_down = current_price * (1 - annual_volatility / np.sqrt(252/30))
two_std_down = current_price * (1 - 2 * annual_volatility / np.sqrt(252/30))
one_std_up = current_price * (1 + annual_volatility / np.sqrt(252/30))
two_std_up = current_price * (1 + 2 * annual_volatility / np.sqrt(252/30))

print(f"\n📊 PROBABILITY ANALYSIS (30-day horizon)")
print("-" * 60)
print(f"Based on {annual_volatility:.1%} annual volatility:")
print(f"  • 68% probability: Stock between ${one_std_down:.2f} and ${one_std_up:.2f}")
print(f"  • 95% probability: Stock between ${two_std_down:.2f} and ${two_std_up:.2f}")
print(f"  • Current price: ${current_price:.2f}")

# Scenario Analysis
scenarios = [
    ("20% decline", current_price * 0.80),
    ("10% decline", current_price * 0.90),
    ("Unchanged", current_price),
    ("10% gain", current_price * 1.10),
    ("20% gain", current_price * 1.20)
]

print(f"\n📈 PROFIT/LOSS SCENARIOS")
print("-" * 60)
print(f"{'Scenario':<15} {'Price':<10} {'Unhedged P&L':<15} {'w/ Put@90%':<15} {'w/ Collar':<15}")
print("-" * 80)

for scenario_name, scenario_price in scenarios:
    unhedged_pl = (scenario_price - current_price) * SHARES_OWNED
    
    # With protective put at 90%
    put_pl = unhedged_pl - put_premium_estimate * SHARES_OWNED
    if scenario_price < put_strike_90:
        put_pl = (put_strike_90 - current_price) * SHARES_OWNED - put_premium_estimate * SHARES_OWNED
    
    # With collar
    collar_pl = unhedged_pl - (put_premium_estimate - call_premium_estimate) * SHARES_OWNED
    if scenario_price < put_strike_90:
        collar_pl = (put_strike_90 - current_price) * SHARES_OWNED - (put_premium_estimate - call_premium_estimate) * SHARES_OWNED
    elif scenario_price > call_strike_110:
        collar_pl = (call_strike_110 - current_price) * SHARES_OWNED - (put_premium_estimate - call_premium_estimate) * SHARES_OWNED
    
    print(f"{scenario_name:<15} ${scenario_price:<9.2f} ${unhedged_pl:>13,.0f} ${put_pl:>13,.0f} ${collar_pl:>13,.0f}")

# Final Recommendations
print("\n" + "=" * 80)
print("RECOMMENDED ACTION PLAN")
print("=" * 80)

print(f"""
Based on your 3,000 shares (30 option contracts) of Natera:

📌 CONSERVATIVE APPROACH:
   → Implement Protective Puts on full position
   → Strike: ${put_strike_95:.2f} (5% OTM)
   → Expiration: 30-60 days
   → Roll monthly to maintain protection

📌 INCOME GENERATION:
   → Sell Covered Calls on 1/3 to 1/2 position
   → Strike: ${call_strike_110:.2f} (10% OTM)
   → Expiration: 30-45 days
   → Collect premium monthly

📌 BALANCED APPROACH:
   → Implement Collar on full position
   → Put Strike: ${put_strike_90:.2f} / Call Strike: ${call_strike_110:.2f}
   → Near zero-cost protection
   → Defined risk/reward profile

📌 MARKET OUTLOOK CONSIDERATIONS:
   • Bullish: Focus on covered calls for income
   • Bearish: Prioritize protective puts
   • Neutral: Collar strategy optimal
   • High Volatility: Options premiums favorable for selling

⚠️ IMPORTANT NOTES:
   • Options involve risk and are not suitable for all investors
   • Actual premiums will vary based on market conditions
   • Consider tax implications of options strategies
   • Monitor positions regularly and adjust as needed
""")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"Position Value: ${position_value:,.2f}")
print(f"Options Contracts Needed: {contracts_needed:.0f}")
print(f"Volatility Risk Level: {'High' if annual_volatility > 0.4 else 'Moderate' if annual_volatility > 0.25 else 'Low'}")
print("\n✅ Ready to implement hedging strategy based on your risk tolerance and market outlook")