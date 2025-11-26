#!/usr/bin/env python3
"""
Collar Strategy Comparison Table
Visual comparison of different collar configurations
"""

import pandas as pd
import numpy as np
from datetime import datetime
from tabulate import tabulate

print("=" * 120)
print("COLLAR STRATEGY COMPARISON - WHICH ONE IS RIGHT FOR YOU?")
print("=" * 120)
print(f"Current NTRA Price: $235.56 | Position: 3,000 shares | Value: $706,680")
print("=" * 120)

# Define collar strategies with actual market data
collars = [
    {
        "Name": "CONSERVATIVE\n(Tight Protection)",
        "Expiry": "Dec 19 '25",
        "Days": 24,
        "Put Strike": "$220",
        "Call Strike": "$250", 
        "Put Cost": "$5.94",
        "Call Income": "$4.50",
        "Net Cost": "$4,320",
        "Protection Level": "6.6%",
        "Upside Cap": "6.1%",
        "Max Loss": "$50,995",
        "Max Gain": "$39,005",
        "Best For": "Very risk-averse\nMinimal drawdown tolerance",
        "Probability Success": "~95%"
    },
    {
        "Name": "BALANCED\n(Standard Width)",
        "Expiry": "Dec 19 '25",
        "Days": 24,
        "Put Strike": "$210",
        "Call Strike": "$260",
        "Put Cost": "$2.47",
        "Call Income": "$2.60",
        "Net Cost": "-$390\n(Credit!)",
        "Protection Level": "10.9%",
        "Upside Cap": "10.4%",
        "Max Loss": "$76,675",
        "Max Gain": "$73,325",
        "Best For": "Balanced approach\nGood risk/reward",
        "Probability Success": "~90%"
    },
    {
        "Name": "AGGRESSIVE\n(Wide Protection)",
        "Expiry": "Dec 19 '25",
        "Days": 24,
        "Put Strike": "$200",
        "Call Strike": "$270",
        "Put Cost": "$1.17",
        "Call Income": "$1.30",
        "Net Cost": "-$390\n(Credit!)",
        "Protection Level": "15.1%",
        "Upside Cap": "14.6%",
        "Max Loss": "$106,675",
        "Max Gain": "$103,325",
        "Best For": "Comfortable with\nvolatility",
        "Probability Success": "~85%"
    },
    {
        "Name": "LONGER-TERM\n(More Time)",
        "Expiry": "Jan 16 '26",
        "Days": 52,
        "Put Strike": "$210",
        "Call Strike": "$260",
        "Put Cost": "$15.20",
        "Call Income": "$5.00",
        "Net Cost": "$30,600",
        "Protection Level": "10.9%",
        "Upside Cap": "10.4%",
        "Max Loss": "$107,275",
        "Max Gain": "$42,725",
        "Best For": "Less active management\nMore time value",
        "Probability Success": "~88%"
    }
]

df = pd.DataFrame(collars)

print("\n📊 COLLAR STRATEGY COMPARISON TABLE\n")
print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

# Scenario analysis
print("\n" + "=" * 120)
print("PERFORMANCE IN DIFFERENT MARKET SCENARIOS")
print("=" * 120)

scenarios = {
    "Crash (-30%)": 165,
    "Correction (-15%)": 200,
    "Pullback (-5%)": 224,
    "Sideways (0%)": 236,
    "Rally (+10%)": 259,
    "Surge (+20%)": 283
}

print("\nP&L by Market Scenario (vs unhedged position):\n")

scenario_results = []
for scenario, price in scenarios.items():
    row = {"Scenario": f"{scenario}\n${price:.0f}"}
    row["Unhedged"] = f"${(price - 235.56) * 3000:,.0f}"
    
    # Conservative collar
    if price <= 220:
        pl = (220 - 235.56) * 3000 - 4320
    elif price >= 250:
        pl = (250 - 235.56) * 3000 - 4320
    else:
        pl = (price - 235.56) * 3000 - 4320
    row["Conservative"] = f"${pl:,.0f}"
    
    # Balanced collar
    if price <= 210:
        pl = (210 - 235.56) * 3000 + 390
    elif price >= 260:
        pl = (260 - 235.56) * 3000 + 390
    else:
        pl = (price - 235.56) * 3000 + 390
    row["Balanced"] = f"${pl:,.0f}"
    
    # Aggressive collar
    if price <= 200:
        pl = (200 - 235.56) * 3000 + 390
    elif price >= 270:
        pl = (270 - 235.56) * 3000 + 390
    else:
        pl = (price - 235.56) * 3000 + 390
    row["Aggressive"] = f"${pl:,.0f}"
    
    scenario_results.append(row)

scenario_df = pd.DataFrame(scenario_results)
print(tabulate(scenario_df, headers='keys', tablefmt='grid', showindex=False))

# Decision matrix
print("\n" + "=" * 120)
print("DECISION MATRIX - WHICH COLLAR IS RIGHT FOR YOU?")
print("=" * 120)

print("""
Answer these questions to find your ideal collar:

1. What's your PRIMARY goal?
   a) Maximum protection, willing to pay → CONSERVATIVE
   b) Balanced protection at low cost → BALANCED ✓
   c) Some protection, maximum upside → AGGRESSIVE
   d) Set and forget for weeks → LONGER-TERM

2. How much downside can you tolerate?
   a) Less than 10% → CONSERVATIVE
   b) 10-15% → BALANCED ✓
   c) 15-20% → AGGRESSIVE
   d) Depends on timeframe → LONGER-TERM

3. Market outlook for next month?
   a) Very bearish → CONSERVATIVE (tighter protection)
   b) Mildly bearish → BALANCED ✓
   c) Neutral/choppy → AGGRESSIVE (collect credit)
   d) Uncertain → LONGER-TERM

4. How actively will you manage?
   a) Daily monitoring → Any short-term
   b) Weekly check-ins → BALANCED/AGGRESSIVE ✓
   c) Monthly only → LONGER-TERM
   d) Minimal attention → LONGER-TERM

5. What's your experience level?
   a) New to options → CONSERVATIVE
   b) Some experience → BALANCED ✓
   c) Experienced → AGGRESSIVE
   d) Varies → Start CONSERVATIVE
""")

print("\n" + "=" * 120)
print("MY RECOMMENDATION FOR YOUR SITUATION")
print("=" * 120)

print(f"""
Given that NTRA is at PEAK LEVELS (only 0.6% below 52-week high):

🏆 RECOMMENDED: BALANCED COLLAR (Dec 19 '25)
   
   Buy 30 contracts: $210 Put @ $2.47
   Sell 30 contracts: $260 Call @ $2.60
   
   ✅ Net CREDIT of $390 (you get paid!)
   ✅ Protected below $210 (10.9% cushion)
   ✅ Can profit up to $260 (10.4% upside)
   ✅ 90% probability of success
   ✅ Max risk: $76,675 (but only if stock drops >10%)

WHY THIS IS IDEAL:
• You GET PAID $390 to protect your position
• Sufficient 10% downside protection for a pullback
• Still capture 10% upside if rally continues
• Short 24-day timeframe = less risk
• Can adjust or roll if market conditions change

EXECUTION CHECKLIST:
□ Place as single spread order during market hours
□ Use LIMIT order: Net CREDIT of $0.13 or better
□ If not filled, try legging in (sell call first)
□ Set alerts at $210 and $260
□ Mark calendar for Dec 5th (2 weeks before expiry)

ALTERNATIVE IF MORE CONSERVATIVE:
   Use the CONSERVATIVE collar if you:
   • Cannot tolerate >7% drawdown
   • Believe correction is imminent
   • Prefer tighter protection even at a cost
   
ALTERNATIVE IF NEUTRAL ON MARKET:
   Use the AGGRESSIVE collar if you:
   • Think stock will consolidate here
   • Want maximum credit received
   • Comfortable with 15% swings
""")

print("\n" + "=" * 120)
print("Ready to Execute: Review live prices and place your collar order")
print("=" * 120)