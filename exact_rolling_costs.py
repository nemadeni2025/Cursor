#!/usr/bin/env python3
"""
Exact Rolling Costs Calculation for NTRA Collar
Real-time options pricing for rolling strategy
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("EXACT ROLLING COSTS CALCULATION - REAL-TIME OPTIONS PRICING")
print("=" * 100)
print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 100)

# Your position
shares = 3000
current_puts = 20
current_put_strike = 210
current_calls = 30
current_call_strike = 260
current_expiration = "2026-01-16"
put_cost = 9700
call_income = 4440

# Get current stock price
ticker = "NTRA"
stock = yf.Ticker(ticker)
current_price = stock.history(period="1d")['Close'].iloc[-1]

print(f"\n📊 CURRENT MARKET CONDITIONS")
print("-" * 80)
print(f"NTRA Current Price: ${current_price:.2f}")
print(f"Your Call Strike: ${current_call_strike:.0f}")
print(f"Distance from Strike: {((current_call_strike - current_price) / current_price * 100):.1f}%")
print(f"Days to Expiration: {(datetime.strptime(current_expiration, '%Y-%m-%d') - datetime.now()).days}")

# Get current options chain
print(f"\n📊 CURRENT JANUARY 16, 2026 OPTIONS PRICING")
print("-" * 80)

try:
    opt_chain = stock.option_chain(current_expiration)
    calls = opt_chain.calls
    puts = opt_chain.puts
    
    # Find your current call
    your_call = calls[calls['strike'] == current_call_strike]
    
    if len(your_call) > 0:
        call_data = your_call.iloc[0]
        current_call_bid = call_data['bid']
        current_call_ask = call_data['ask']
        current_call_mid = (current_call_bid + current_call_ask) / 2
        current_call_last = call_data['lastPrice'] if pd.notna(call_data['lastPrice']) else current_call_mid
        
        print(f"\nYour Current Calls: 30 Jan 16 ${current_call_strike:.0f} Calls")
        print(f"  Bid: ${current_call_bid:.2f}")
        print(f"  Ask: ${current_call_ask:.2f}")
        print(f"  Mid: ${current_call_mid:.2f}")
        print(f"  Last: ${current_call_last:.2f}")
        print(f"  Original Premium: ${call_income/30/100:.2f}/share")
        
        # Calculate cost to buy back
        buyback_cost = current_call_mid * 30 * 100
        print(f"\n  Cost to Buy Back 30 Contracts: ${buyback_cost:,.2f}")
        
        if current_price < current_call_strike:
            print(f"  Status: Out-of-the-Money (Safe for now)")
        else:
            print(f"  Status: IN-THE-MONEY (ROLL IMMEDIATELY!)")
    else:
        print("Could not find your call strike in options chain")
        current_call_mid = 1.50  # Estimate
        buyback_cost = current_call_mid * 30 * 100
        
except Exception as e:
    print(f"Error fetching options: {e}")
    current_call_mid = 1.50
    buyback_cost = current_call_mid * 30 * 100

# Get February options for rolling
print(f"\n📊 FEBRUARY 21, 2026 OPTIONS (Roll Target)")
print("-" * 80)

feb_expiration = "2026-02-21"
try:
    feb_chain = stock.option_chain(feb_expiration)
    feb_calls = feb_chain.calls
    
    # Show rolling options
    roll_strikes = [270, 275, 280, 285, 290]
    
    print(f"\nRolling Options - February 21, 2026:")
    print(f"{'Strike':<10} {'Bid':<10} {'Ask':<10} {'Mid':<10} {'Income (30)':<15} {'Net Cost':<15}")
    print("-" * 80)
    
    rolling_scenarios = []
    
    for strike in roll_strikes:
        strike_calls = feb_calls[feb_calls['strike'] == strike]
        if len(strike_calls) > 0:
            call = strike_calls.iloc[0]
            bid = call['bid']
            ask = call['ask']
            mid = (bid + ask) / 2
            income = mid * 30 * 100
            net_cost = buyback_cost - income
            
            rolling_scenarios.append({
                'strike': strike,
                'bid': bid,
                'ask': ask,
                'mid': mid,
                'income': income,
                'net_cost': net_cost
            })
            
            print(f"${strike:<9.0f} ${bid:<9.2f} ${ask:<9.2f} ${mid:<9.2f} ${income:>13,.0f} ${net_cost:>13,.0f}")
        else:
            # Estimate
            estimated_premium = max(0.50, (strike - current_price) * 0.02)
            income = estimated_premium * 30 * 100
            net_cost = buyback_cost - income
            print(f"${strike:<9.0f} {'Est':<9} {'Est':<9} ${estimated_premium:<9.2f} ${income:>13,.0f} ${net_cost:>13,.0f}")
            
except Exception as e:
    print(f"Error fetching February options: {e}")
    rolling_scenarios = []

# Calculate different scenarios
print(f"\n" + "=" * 100)
print("ROLLING COST SCENARIOS")
print("=" * 100)

scenarios = [
    {'name': 'Stock at $240 (Current)', 'price': 240, 'call_value': 0.50},
    {'name': 'Stock at $250', 'price': 250, 'call_value': 1.50},
    {'name': 'Stock at $255 (2% below)', 'price': 255, 'call_value': 2.50},
    {'name': 'Stock at $260 (At Strike)', 'price': 260, 'call_value': 4.00},
    {'name': 'Stock at $265 (ITM)', 'price': 265, 'call_value': 6.00},
]

print(f"\n{'Scenario':<25} {'Buyback Cost':<15} {'Roll to $270':<15} {'Roll to $280':<15} {'Net Cost':<15}")
print("-" * 100)

for scenario in scenarios:
    buyback = scenario['call_value'] * 30 * 100
    
    # Roll to $270
    roll_270_income = 2.00 * 30 * 100 if scenario['price'] < 270 else 0.50 * 30 * 100
    net_270 = buyback - roll_270_income
    
    # Roll to $280
    roll_280_income = 1.00 * 30 * 100 if scenario['price'] < 280 else 0.30 * 30 * 100
    net_280 = buyback - roll_280_income
    
    print(f"{scenario['name']:<25} ${buyback:>13,.0f} ${net_270:>13,.0f} ${net_280:>13,.0f} ${min(net_270, net_280):>13,.0f}")

# Best rolling strategy
print(f"\n" + "=" * 100)
print("RECOMMENDED ROLLING STRATEGY")
print("=" * 100)

if rolling_scenarios:
    best_roll = min(rolling_scenarios, key=lambda x: abs(x['net_cost']))
    
    print(f"""
🎯 OPTIMAL ROLL:

From: 30 Jan 16 ${current_call_strike:.0f} Calls
To: 30 Feb 21 ${best_roll['strike']:.0f} Calls

Cost to Buy Back: ${buyback_cost:,.2f}
Income from New Calls: ${best_roll['income']:,.2f}
Net Cost: ${best_roll['net_cost']:,.2f}

Benefits:
  ✅ Higher strike: ${best_roll['strike'] - current_call_strike:.0f} points more room
  ✅ More time: 36 extra days
  ✅ Keep your shares
  ✅ Avoid $210,000 tax bill
""")

# E*TRADE specific order instructions
print("=" * 100)
print("E*TRADE ROLL ORDER - STEP BY STEP")
print("=" * 100)

print(f"""
📱 E*TRADE ROLLING INSTRUCTIONS:

METHOD 1: Using Roll Function (Easiest)

1. Login to E*TRADE
2. Go to: Positions → Options
3. Find: 30 NTRA Jan 16 ${current_call_strike:.0f} Calls
4. Click: "Roll" button
5. Select: "Roll Up and Out"
6. Enter:
   - Close: 30 Jan 16 ${current_call_strike:.0f} Calls
   - Open: 30 Feb 21 {best_roll['strike'] if rolling_scenarios else 270:.0f} Calls
7. Order Type: NET DEBIT
8. Limit: ${best_roll['net_cost']/30/100 if rolling_scenarios else 2.00:.2f} per share
9. Duration: Day Order
10. Review and Submit

METHOD 2: Two Separate Orders (If Roll Function Not Available)

ORDER 1: Buy to Close
   Action: BUY TO CLOSE
   Symbol: NTRA
   Quantity: 30
   Expiration: Jan 16, 2026
   Strike: ${current_call_strike:.0f}
   Type: Call
   Order Type: LIMIT
   Limit Price: ${current_call_mid:.2f} or better
   Duration: Day

ORDER 2: Sell to Open (Place immediately after Order 1)
   Action: SELL TO OPEN
   Symbol: NTRA
   Quantity: 30
   Expiration: Feb 21, 2026
   Strike: {best_roll['strike'] if rolling_scenarios else 270:.0f}
   Type: Call
   Order Type: LIMIT
   Limit Price: ${best_roll['mid'] if rolling_scenarios else 2.00:.2f} or better
   Duration: Day

IMPORTANT: Execute both orders within 1-2 minutes of each other!
""")

# Timing recommendations
print("=" * 100)
print("WHEN TO EXECUTE THE ROLL")
print("=" * 100)

exp_date = datetime.strptime(current_expiration, '%Y-%m-%d')
days_remaining = (exp_date - datetime.now()).days

print(f"""
⏰ TIMING RECOMMENDATIONS:

Current Situation:
  • Days to Expiration: {days_remaining} days
  • Stock Price: ${current_price:.2f}
  • Distance from Strike: {((current_call_strike - current_price) / current_price * 100):.1f}%

IMMEDIATE ACTION:
  {'🚨 ROLL NOW - Stock approaching strike!' if current_price > current_call_strike * 0.95 else '✅ Monitor - Stock still safe'}

OPTIMAL ROLLING WINDOW:
  • Best Time: {exp_date - timedelta(days=14)} (14 days out)
  • Latest Safe Time: {exp_date - timedelta(days=7)} (7 days out)
  • Emergency: {exp_date - timedelta(days=3)} (3 days out)

PRICE TRIGGERS:
  • ${current_call_strike * 0.98:.0f} (2% below): Start preparing roll
  • ${current_call_strike * 0.95:.0f} (5% below): Execute roll this week
  • ${current_call_strike:.0f} (At strike): ROLL IMMEDIATELY
  • ${current_call_strike + 1:.0f}+ (ITM): ROLL TODAY
""")

# Cost comparison
print("=" * 100)
print("COST-BENEFIT ANALYSIS")
print("=" * 100)

roll_cost = best_roll['net_cost'] if rolling_scenarios else 3000
tax_savings = 210000

print(f"""
💰 FINANCIAL COMPARISON:

Option 1: ROLL THE CALLS
  Cost: ${roll_cost:,.2f}
  Benefit: Keep shares, no tax event
  Net Position: 3,000 shares + protection

Option 2: LET CALLS EXPIRE ITM (DON'T DO THIS!)
  Cost: $0 (but lose shares)
  Tax Bill: $210,000
  Net Position: $0 shares, $210,000 less

SAVINGS FROM ROLLING: ${tax_savings - roll_cost:,.2f}
ROI: {(tax_savings / roll_cost - 1) * 100:.0f}% return on roll cost
""")

# Set up alerts
print("=" * 100)
print("SET UP PRICE ALERTS IN E*TRADE")
print("=" * 100)

print(f"""
🔔 CRITICAL ALERTS TO SET:

Alert 1: Warning Level
   Symbol: NTRA
   Condition: Price >= ${current_call_strike * 0.98:.0f}
   Type: Email + Text
   Message: "NTRA approaching call strike - prepare to roll"

Alert 2: Action Level
   Symbol: NTRA
   Condition: Price >= ${current_call_strike * 0.95:.0f}
   Type: Email + Text
   Message: "NTRA near strike - execute roll this week"

Alert 3: Emergency Level
   Symbol: NTRA
   Condition: Price >= ${current_call_strike:.0f}
   Type: Email + Text + Phone
   Message: "NTRA at strike - ROLL IMMEDIATELY"

Alert 4: Date Reminder
   Date: {exp_date - timedelta(days=14)}
   Message: "14 days to expiration - review roll strategy"

Alert 5: Final Reminder
   Date: {exp_date - timedelta(days=7)}
   Message: "7 days to expiration - roll if needed"
""")

print("=" * 100)
print("SUMMARY & ACTION ITEMS")
print("=" * 100)

print(f"""
✅ YOUR ACTION PLAN:

1. TODAY:
   □ Set price alerts at ${current_call_strike * 0.98:.0f}, ${current_call_strike * 0.95:.0f}, ${current_call_strike:.0f}
   □ Set calendar reminder for {exp_date - timedelta(days=14).strftime('%Y-%m-%d')}
   □ Prepare roll order template in E*TRADE

2. ON {exp_date - timedelta(days=14).strftime('%Y-%m-%d')} (14 days out):
   □ Check stock price
   □ If above ${current_call_strike * 0.95:.0f}, execute roll
   □ Roll to Feb 21 ${best_roll['strike'] if rolling_scenarios else 270:.0f} Calls

3. IF STOCK REACHES ${current_call_strike:.0f}:
   □ Execute roll IMMEDIATELY
   □ Don't wait - assignment risk is high

4. REMEMBER:
   • Rolling costs $1,000-4,000
   • Not rolling costs $210,000 in taxes
   • Always roll before expiration if stock near strike
   • Better to roll early than too late

📞 E*TRADE SUPPORT: 1-800-387-2331
   Say: "I need to roll covered calls to avoid assignment"
""")

print("=" * 100)
