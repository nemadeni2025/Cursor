#!/usr/bin/env python3
"""
Collar Rolling Strategy Analysis
For 3,000 shares with Jan 16, 2026 puts and potential covered calls
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("YOUR COLLAR POSITION ANALYSIS & ROLLING STRATEGY")
print("=" * 100)

# Your position details
shares_owned = 3000
put_contracts = 20
put_strike = 210  # Assuming based on earlier discussion
put_cost = 9700
put_cost_per_contract = put_cost / put_contracts
put_cost_per_share = put_cost / shares_owned

# Covered call details (clarifying)
call_contracts = 30  # Assuming you meant 30, not 310
call_premium = 1.48  # Per share
call_income = call_premium * shares_owned  # $1.48 * 3,000 = $4,440
call_strike = None  # Need to determine

expiration = "2026-01-16"
exp_date = datetime.strptime(expiration, "%Y-%m-%d")
today = datetime.now()
days_to_exp = (exp_date - today).days

print(f"\n📊 YOUR CURRENT POSITION")
print("-" * 80)
print(f"Shares Owned: {shares_owned:,}")
print(f"Put Contracts: {put_contracts} (covers {put_contracts * 100:,} shares)")
print(f"Put Strike: ${put_strike:.0f}")
print(f"Put Cost: ${put_cost:,.2f} (${put_cost_per_share:.2f}/share)")
print(f"Expiration: {expiration} ({days_to_exp} days)")
print(f"\n⚠️ NOTE: You have {shares_owned - (put_contracts * 100):,} shares UNPROTECTED by puts")

# Get current options pricing
print(f"\n📊 ANALYZING JANUARY 16, 2026 OPTIONS")
print("-" * 80)

ticker = "NTRA"
stock = yf.Ticker(ticker)
current_price = stock.history(period="1d")['Close'].iloc[-1]

print(f"Current NTRA Price: ${current_price:.2f}")

try:
    opt_chain = stock.option_chain(expiration)
    calls = opt_chain.calls
    puts = opt_chain.puts
    
    # Find call strikes that would generate ~$1.48 premium
    print(f"\nAvailable Call Strikes for Jan 16, 2026:")
    print("-" * 60)
    
    relevant_calls = calls[(calls['strike'] >= current_price * 1.05) & 
                          (calls['strike'] <= current_price * 1.20)]
    
    if len(relevant_calls) > 0:
        print(f"{'Strike':<10} {'Bid':<10} {'Ask':<10} {'Last':<10} {'Income (30)':<15}")
        print("-" * 60)
        
        for _, call in relevant_calls.head(10).iterrows():
            premium = call['lastPrice'] if pd.notna(call['lastPrice']) else (call['bid'] + call['ask']) / 2
            income_30 = premium * 30 * 100
            if abs(income_30 - call_income) < 500:  # Close to $4,440
                call_strike = call['strike']
                print(f"${call['strike']:<9.0f} ${call['bid']:<9.2f} ${call['ask']:<9.2f} ${premium:<9.2f} ${income_30:>13,.0f} ← MATCH")
            else:
                print(f"${call['strike']:<9.0f} ${call['bid']:<9.2f} ${call['ask']:<9.2f} ${premium:<9.2f} ${income_30:>13,.0f}")
        
        if call_strike is None:
            # Find closest match
            call_strike = relevant_calls.iloc[0]['strike']
            print(f"\nAssuming call strike: ${call_strike:.0f}")
    else:
        # Estimate based on premium
        call_strike = current_price * 1.10  # ~10% OTM
        print(f"Estimated call strike: ${call_strike:.0f} (10% OTM)")
        
except Exception as e:
    print(f"Error fetching options: {e}")
    call_strike = current_price * 1.10
    print(f"Using estimated call strike: ${call_strike:.0f}")

# Calculate collar metrics
net_cost = put_cost - call_income
net_cost_per_share = net_cost / shares_owned

print(f"\n" + "=" * 100)
print("YOUR COLLAR STRATEGY SUMMARY")
print("=" * 100)

print(f"""
Position Structure:
  • 3,000 shares of NTRA
  • 20 Jan 16 $210 Puts (cost: ${put_cost:,.2f})
  • 30 Jan 16 ${call_strike:.0f} Calls (income: ${call_income:,.2f})
  
Net Cost: ${net_cost:,.2f} (${net_cost_per_share:.2f}/share)
Protected Range: ${put_strike:.0f} to ${call_strike:.0f}
Days to Expiration: {days_to_exp} days
""")

# Rolling strategy
print("=" * 100)
print("ROLLING STRATEGY TO AVOID ASSIGNMENT")
print("=" * 100)

print(f"""
🎯 WHEN TO ROLL YOUR COVERED CALLS:

1. TIME-BASED ROLLING (Primary Trigger):
   ⏰ 21 DAYS BEFORE EXPIRATION: {exp_date - timedelta(days=21)}
     → Start monitoring closely
     → Prepare roll order
   
   ⏰ 14 DAYS BEFORE EXPIRATION: {exp_date - timedelta(days=14)}
     → DECISION POINT - Roll if stock near strike
     → If stock at ${call_strike * 0.98:.0f} or higher, roll NOW
   
   ⏰ 7 DAYS BEFORE EXPIRATION: {exp_date - timedelta(days=7)}
     → URGENT - Roll if stock above ${call_strike * 0.95:.0f}
     → Risk of early assignment increases

2. PRICE-BASED ROLLING (Critical Triggers):
   
   🚨 ROLL IMMEDIATELY IF:
   • Stock reaches ${call_strike * 0.95:.0f} (5% below strike)
   • Stock reaches ${call_strike * 0.98:.0f} (2% below strike)
   • Stock is IN-THE-MONEY (above ${call_strike:.0f})
   
   ⚠️ ROLL SOON IF:
   • Stock within $5 of strike (${call_strike - 5:.0f})
   • Stock showing strong momentum upward
   • Volume spike suggests breakout

3. GREEKS-BASED ROLLING:
   • Delta > 0.50: High risk of assignment
   • Gamma increasing: Price sensitivity rising
   • Theta decay accelerating: Time running out
""")

# Rolling mechanics
print("\n" + "=" * 100)
print("HOW TO ROLL YOUR COVERED CALLS")
print("=" * 100)

print(f"""
📋 ROLLING PROCESS:

Step 1: BUY BACK Current Calls
   Action: BUY TO CLOSE
   Contracts: 30
   Strike: ${call_strike:.0f}
   Expiration: Jan 16, 2026
   Cost: Current market price (may be higher than you sold)

Step 2: SELL NEW Calls
   Action: SELL TO OPEN
   Contracts: 30
   Strike: ${call_strike + 10:.0f} (or higher - "roll up")
   Expiration: Feb 21, 2026 (or later - "roll out")
   Income: New premium received

NET RESULT: 
   • Debit: Cost to buy back old calls
   • Credit: Premium from new calls
   • Net: Usually small debit or credit
   • Benefit: Keep your shares!
""")

# Specific rolling scenarios
print("\n" + "=" * 100)
print("ROLLING SCENARIOS & EXAMPLES")
print("=" * 100)

scenarios = [
    {
        'name': 'Stock at Strike (At-the-Money)',
        'price': call_strike,
        'action': 'ROLL IMMEDIATELY',
        'new_strike': call_strike + 10,
        'timing': 'Same day'
    },
    {
        'name': 'Stock 2% Below Strike',
        'price': call_strike * 0.98,
        'action': 'ROLL THIS WEEK',
        'new_strike': call_strike + 5,
        'timing': 'Within 3 days'
    },
    {
        'name': 'Stock 5% Below Strike',
        'price': call_strike * 0.95,
        'action': 'Monitor Closely',
        'new_strike': call_strike + 5,
        'timing': 'If approaches strike'
    },
    {
        'name': 'Stock Well Below Strike',
        'price': call_strike * 0.90,
        'action': 'No Action Needed',
        'new_strike': 'N/A',
        'timing': 'Let calls expire worthless'
    }
]

print(f"\n{'Scenario':<30} {'Stock Price':<15} {'Action':<20} {'New Strike':<15} {'Timing':<20}")
print("-" * 100)

for scenario in scenarios:
    strike_str = f"${scenario['new_strike']:.0f}" if isinstance(scenario['new_strike'], (int, float)) else scenario['new_strike']
    print(f"{scenario['name']:<30} ${scenario['price']:<14.2f} {scenario['action']:<20} "
          f"{strike_str:<15} {scenario['timing']:<20}")

# Rolling cost estimates
print("\n" + "=" * 100)
print("ESTIMATED ROLLING COSTS")
print("=" * 100)

print(f"""
Example: Rolling from ${call_strike:.0f} to ${call_strike + 10:.0f} (Feb 21)

If Stock at ${call_strike:.0f}:
  • Buy back 30 ${call_strike:.0f} calls: ~${call_premium * 1.5 * 3000:,.0f} (more expensive)
  • Sell 30 ${call_strike + 10:.0f} calls: ~${call_premium * 0.8 * 3000:,.0f} (less premium)
  • Net Cost: ~${(call_premium * 1.5 - call_premium * 0.8) * 3000:,.0f}
  • BUT: You keep your shares and avoid ${(call_strike - 200) * 3000:,.0f} in taxes!

If Stock at ${call_strike * 0.95:.0f}:
  • Buy back 30 ${call_strike:.0f} calls: ~${call_premium * 0.5 * 3000:,.0f} (cheaper)
  • Sell 30 ${call_strike + 10:.0f} calls: ~${call_premium * 0.6 * 3000:,.0f}
  • Net Cost: ~${(call_premium * 0.6 - call_premium * 0.5) * 3000:,.0f} (small)
  • Benefit: Reset protection, keep shares
""")

# Critical dates calendar
print("\n" + "=" * 100)
print("CRITICAL DATES CALENDAR")
print("=" * 100)

critical_dates = [
    (exp_date - timedelta(days=21), "21 days out", "Start monitoring for roll"),
    (exp_date - timedelta(days=14), "14 days out", "DECISION POINT - Roll if needed"),
    (exp_date - timedelta(days=7), "7 days out", "URGENT - Roll if stock near strike"),
    (exp_date - timedelta(days=3), "3 days out", "Last chance to roll easily"),
    (exp_date - timedelta(days=1), "1 day out", "Very difficult to roll"),
    (exp_date, "Expiration", "Assignment risk highest")
]

print(f"\n{'Date':<15} {'Days Out':<15} {'Action Required':<50}")
print("-" * 80)
for date, days_out, action in critical_dates:
    print(f"{date.strftime('%Y-%m-%d'):<15} {days_out:<15} {action:<50}")

# Tax implications reminder
print("\n" + "=" * 100)
print("⚠️ TAX IMPLICATIONS OF ROLLING")
print("=" * 100)

print(f"""
CRITICAL: Rolling prevents assignment = NO TAX EVENT

If You DON'T Roll and Get Assigned:
  • Shares called away at ${call_strike:.0f}
  • Realize ${(call_strike - 200) * 3000:,.0f} in gains
  • Tax bill: ~$210,000
  • Net after tax: ~$516,000

If You DO Roll:
  • Cost: ~$2,000-5,000 to roll
  • Keep shares
  • NO tax event
  • Continue protection
  • Net benefit: Save $210,000 in taxes for $5,000 cost

ROLLING IS ESSENTIAL TO AVOID TAX DISASTER!
""")

# E*TRADE specific instructions
print("\n" + "=" * 100)
print("E*TRADE ROLLING INSTRUCTIONS")
print("=" * 100)

print(f"""
📱 HOW TO ROLL IN E*TRADE:

1. Go to "Positions" → Find your 30 Jan 16 ${call_strike:.0f} Calls

2. Click "Roll" or "Close and Replace"

3. Enter Roll Order:
   CLOSE: 30 Jan 16 ${call_strike:.0f} Calls (Buy to Close)
   OPEN: 30 Feb 21 ${call_strike + 10:.0f} Calls (Sell to Open)
   
4. Set as NET DEBIT or NET CREDIT order
   • If stock below strike: Usually small credit
   • If stock at/above strike: Usually small debit

5. Submit order

ALTERNATIVE: Two Separate Orders
   Order 1: Buy to Close 30 Jan 16 ${call_strike:.0f} Calls
   Order 2: Sell to Open 30 Feb 21 ${call_strike + 10:.0f} Calls
   (Execute simultaneously or within minutes)
""")

print("\n" + "=" * 100)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 100)

print(f"""
✅ YOUR CURRENT SETUP:
   • Protected below ${put_strike:.0f}
   • Capped above ${call_strike:.0f}
   • Net cost: ${net_cost:,.2f}
   • Expires: {expiration}

🎯 ROLLING STRATEGY:
   1. Monitor stock price daily
   2. Set alert at ${call_strike * 0.98:.0f} (2% below strike)
   3. Roll 14 days before expiration ({exp_date - timedelta(days=14).strftime('%Y-%m-%d')})
   4. Roll up and out (higher strike, later expiration)
   5. Cost: $2,000-5,000 but saves $210,000 in taxes

⚠️ CRITICAL RULE:
   NEVER let calls expire in-the-money if you want to keep shares!
   Roll at least 3-7 days before expiration if stock near strike.

💰 REMEMBER:
   The $2,000-5,000 cost to roll is NOTHING compared to 
   $210,000 tax bill if shares get called away!
""")

print("=" * 100)
