#!/usr/bin/env python3
"""
Deep Dive: Collar Strategy Implementation for Natera (NTRA)
Comprehensive analysis for protecting 3,000 shares at peak levels
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 100)
print("COLLAR STRATEGY DEEP DIVE - NATERA (NTRA)")
print("Protecting Your Position at Peak Levels")
print("=" * 100)
print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 100)

# Parameters
TICKER = "NTRA"
SHARES = 3000
CONTRACTS = 30

# Fetch current data
stock = yf.Ticker(TICKER)
try:
    info = stock.info
    current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose', 0)
    high_52w = info.get('fiftyTwoWeekHigh', 0)
    low_52w = info.get('fiftyTwoWeekLow', 0)
except:
    hist = stock.history(period="1y")
    current_price = hist['Close'].iloc[-1]
    high_52w = hist['High'].max()
    low_52w = hist['Low'].min()

position_value = current_price * SHARES

print(f"\n📊 MARKET CONTEXT - WHY COLLAR NOW?")
print("-" * 80)
print(f"Current Price: ${current_price:.2f}")
print(f"52-Week High: ${high_52w:.2f}")
print(f"52-Week Low: ${low_52w:.2f}")
print(f"Distance from High: {((high_52w - current_price)/high_52w*100):.1f}% below peak")
print(f"Distance from Low: {((current_price - low_52w)/low_52w*100):.1f}% above low")
print(f"Position Value: ${position_value:,.2f}")

# Calculate recent volatility
hist_data = stock.history(period="6mo")
hist_data['Daily_Return'] = hist_data['Close'].pct_change()
volatility_30d = hist_data['Daily_Return'].tail(30).std() * np.sqrt(252)
volatility_60d = hist_data['Daily_Return'].tail(60).std() * np.sqrt(252)

print(f"\n📈 VOLATILITY METRICS")
print(f"30-Day Volatility: {volatility_30d:.1%}")
print(f"60-Day Volatility: {volatility_60d:.1%}")

# Technical indicators
sma_20 = hist_data['Close'].tail(20).mean()
sma_50 = hist_data['Close'].tail(50).mean()
rsi = 100 - (100 / (1 + (hist_data['Daily_Return'].tail(14)[hist_data['Daily_Return'].tail(14) > 0].mean() / 
                         abs(hist_data['Daily_Return'].tail(14)[hist_data['Daily_Return'].tail(14) < 0].mean()))))

print(f"\n📊 TECHNICAL INDICATORS")
print(f"20-Day SMA: ${sma_20:.2f} ({'+' if current_price > sma_20 else ''}{((current_price/sma_20 - 1)*100):.1f}%)")
print(f"50-Day SMA: ${sma_50:.2f} ({'+' if current_price > sma_50 else ''}{((current_price/sma_50 - 1)*100):.1f}%)")
print(f"14-Day RSI: {rsi:.1f} {'(Overbought)' if rsi > 70 else '(Oversold)' if rsi < 30 else '(Neutral)'}")

print("\n" + "=" * 100)
print("COLLAR STRATEGY FUNDAMENTALS")
print("=" * 100)

print("""
🎯 WHAT IS A COLLAR?
A collar combines:
1. PROTECTIVE PUT (you buy) - Insurance against downside
2. COVERED CALL (you sell) - Generates income to offset put cost

📌 WHY COLLAR AT MARKET PEAKS?
✓ Stock near 52-week high = Higher probability of pullback
✓ High implied volatility = Expensive call premiums (good for selling)
✓ Protects gains while keeping some upside
✓ Often zero-cost or even generates credit
✓ Defined risk profile - know your max loss and gain

⚖️ COLLAR TRADE-OFFS:
• Upside is capped at call strike
• Downside protected at put strike
• Time decay works in your favor (selling call)
• Best for 30-90 day timeframes
""")

# Get options chains for analysis
print("\n" + "=" * 100)
print("ANALYZING OPTIMAL COLLAR COMBINATIONS")
print("=" * 100)

expirations = stock.options[:5]  # Get next 5 expirations
collar_analysis = []

for exp_str in expirations[:3]:  # Analyze 3 expirations
    exp_date = datetime.strptime(exp_str, '%Y-%m-%d')
    days_to_exp = (exp_date - datetime.now()).days
    
    if days_to_exp < 20 or days_to_exp > 90:
        continue
    
    print(f"\n📅 Expiration: {exp_str} ({days_to_exp} days)")
    print("-" * 80)
    
    opt_chain = stock.option_chain(exp_str)
    puts = opt_chain.puts
    calls = opt_chain.calls
    
    # Analyze different collar widths
    collar_configs = [
        {"name": "Tight Collar", "put_pct": 0.95, "call_pct": 1.05},
        {"name": "Standard Collar", "put_pct": 0.90, "call_pct": 1.10},
        {"name": "Wide Collar", "put_pct": 0.85, "call_pct": 1.15},
    ]
    
    for config in collar_configs:
        # Find closest strikes
        put_target = current_price * config["put_pct"]
        call_target = current_price * config["call_pct"]
        
        put_row = puts.iloc[(puts['strike'] - put_target).abs().argsort()[:1]]
        call_row = calls.iloc[(calls['strike'] - call_target).abs().argsort()[:1]]
        
        if len(put_row) > 0 and len(call_row) > 0:
            put = put_row.iloc[0]
            call = call_row.iloc[0]
            
            if pd.notna(put['lastPrice']) and pd.notna(call['lastPrice']):
                net_cost = (put['lastPrice'] - call['lastPrice']) * 100 * CONTRACTS
                
                # Calculate key metrics
                max_loss = (current_price - put['strike']) * SHARES + max(0, net_cost)
                max_gain = (call['strike'] - current_price) * SHARES - max(0, net_cost)
                breakeven_down = current_price - (net_cost / SHARES) if net_cost > 0 else current_price
                
                collar_data = {
                    'Expiration': exp_str,
                    'Days': days_to_exp,
                    'Type': config['name'],
                    'Put Strike': put['strike'],
                    'Put Premium': put['lastPrice'],
                    'Call Strike': call['strike'],
                    'Call Premium': call['lastPrice'],
                    'Net Cost/Credit': net_cost,
                    'Per Share': net_cost / SHARES,
                    'Max Loss': max_loss,
                    'Max Gain': max_gain,
                    'Breakeven': breakeven_down,
                    'Put IV': put['impliedVolatility'],
                    'Call IV': call['impliedVolatility'],
                    'Protection %': (current_price - put['strike']) / current_price * 100,
                    'Cap %': (call['strike'] - current_price) / current_price * 100
                }
                collar_analysis.append(collar_data)
                
                print(f"\n{config['name']}:")
                print(f"  Put: ${put['strike']:.0f} @ ${put['lastPrice']:.2f} | Call: ${call['strike']:.0f} @ ${call['lastPrice']:.2f}")
                print(f"  Net {'Cost' if net_cost > 0 else 'Credit'}: ${abs(net_cost):,.0f} (${abs(net_cost/SHARES):.2f}/share)")
                print(f"  Max Loss: ${max_loss:,.0f} ({max_loss/position_value*100:.1f}%)")
                print(f"  Max Gain: ${max_gain:,.0f} ({max_gain/position_value*100:.1f}%)")

# Convert to DataFrame for analysis
if collar_analysis:
    collar_df = pd.DataFrame(collar_analysis)
    
    print("\n" + "=" * 100)
    print("TOP 5 RECOMMENDED COLLARS")
    print("=" * 100)
    
    # Score collars based on multiple factors
    collar_df['Score'] = (
        (collar_df['Net Cost/Credit'] <= 0).astype(int) * 30 +  # Prefer credits
        (collar_df['Protection %'] * 2) +  # Weight protection
        (collar_df['Cap %'] * 1) +  # Some upside weight
        (100 - collar_df['Days']) / 100 * 10  # Prefer 30-60 days
    )
    
    top_collars = collar_df.nlargest(5, 'Score')
    
    for idx, row in top_collars.iterrows():
        print(f"\n🏆 Option {idx+1}: {row['Type']} - {row['Expiration']} ({row['Days']} days)")
        print(f"   Structure: Buy ${row['Put Strike']:.0f} Put / Sell ${row['Call Strike']:.0f} Call")
        print(f"   Net {'Cost' if row['Net Cost/Credit'] > 0 else 'Credit'}: ${abs(row['Net Cost/Credit']):,.0f}")
        print(f"   Protection: {row['Protection %']:.1f}% downside")
        print(f"   Cap: {row['Cap %']:.1f}% upside")
        print(f"   Risk/Reward: Max Loss ${row['Max Loss']:,.0f} / Max Gain ${row['Max Gain']:,.0f}")

# Create detailed P&L visualization
print("\n" + "=" * 100)
print("PROFIT/LOSS ANALYSIS")
print("=" * 100)

# Select best collar for detailed analysis
if collar_analysis:
    best_collar = top_collars.iloc[0]
    
    # Generate P&L scenarios
    price_range = np.linspace(current_price * 0.7, current_price * 1.3, 100)
    
    pl_unhedged = []
    pl_collar = []
    
    for price in price_range:
        # Unhedged P&L
        unhedged = (price - current_price) * SHARES
        pl_unhedged.append(unhedged)
        
        # Collar P&L
        stock_pl = (price - current_price) * SHARES
        put_value = max(best_collar['Put Strike'] - price, 0) * SHARES
        call_obligation = -max(price - best_collar['Call Strike'], 0) * SHARES
        collar_pl = stock_pl + put_value + call_obligation - best_collar['Net Cost/Credit']
        pl_collar.append(collar_pl)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: P&L Comparison
    axes[0, 0].plot(price_range, pl_unhedged, label='Unhedged', linewidth=2, linestyle='--', color='gray')
    axes[0, 0].plot(price_range, pl_collar, label=f"Collar ({best_collar['Type']})", linewidth=3, color='blue')
    axes[0, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[0, 0].axvline(x=current_price, color='red', linestyle='--', alpha=0.5, label='Current Price')
    axes[0, 0].axvline(x=best_collar['Put Strike'], color='green', linestyle='--', alpha=0.5, label='Put Strike')
    axes[0, 0].axvline(x=best_collar['Call Strike'], color='orange', linestyle='--', alpha=0.5, label='Call Strike')
    axes[0, 0].fill_between(price_range, pl_collar, 0, where=(np.array(pl_collar) > 0), alpha=0.3, color='green')
    axes[0, 0].fill_between(price_range, pl_collar, 0, where=(np.array(pl_collar) <= 0), alpha=0.3, color='red')
    axes[0, 0].set_xlabel('Stock Price at Expiration')
    axes[0, 0].set_ylabel('Profit/Loss ($)')
    axes[0, 0].set_title('Collar P&L vs Unhedged Position', fontsize=14, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Protection Zones
    zones = ['Major Loss\n(<-20%)', 'Moderate Loss\n(-20% to -10%)', 'Small Move\n(-10% to +10%)', 
             'Moderate Gain\n(+10% to +20%)', 'Major Gain\n(>+20%)']
    zone_prices = [
        current_price * 0.75,
        current_price * 0.85,
        current_price,
        current_price * 1.15,
        current_price * 1.25
    ]
    
    zone_pl_unhedged = [(p - current_price) * SHARES for p in zone_prices]
    zone_pl_collar = []
    for p in zone_prices:
        stock_pl = (p - current_price) * SHARES
        put_value = max(best_collar['Put Strike'] - p, 0) * SHARES
        call_obligation = -max(p - best_collar['Call Strike'], 0) * SHARES
        collar_pl = stock_pl + put_value + call_obligation - best_collar['Net Cost/Credit']
        zone_pl_collar.append(collar_pl)
    
    x = np.arange(len(zones))
    width = 0.35
    axes[0, 1].bar(x - width/2, zone_pl_unhedged, width, label='Unhedged', alpha=0.7)
    axes[0, 1].bar(x + width/2, zone_pl_collar, width, label='With Collar', alpha=0.7)
    axes[0, 1].set_xlabel('Market Scenario')
    axes[0, 1].set_ylabel('Profit/Loss ($)')
    axes[0, 1].set_title('Scenario Analysis', fontsize=14, fontweight='bold')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(zones, rotation=45, ha='right')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    # Plot 3: Time Decay Analysis
    days_remaining = np.arange(best_collar['Days'], 0, -1)
    theta_put = -best_collar['Put Premium'] / best_collar['Days'] * 100 * CONTRACTS
    theta_call = best_collar['Call Premium'] / best_collar['Days'] * 100 * CONTRACTS
    theta_net = theta_call + theta_put
    
    cumulative_decay = [theta_net * (best_collar['Days'] - d) for d in days_remaining]
    
    axes[1, 0].plot(days_remaining, cumulative_decay, linewidth=2, color='purple')
    axes[1, 0].fill_between(days_remaining, cumulative_decay, 0, alpha=0.3, color='purple')
    axes[1, 0].set_xlabel('Days to Expiration')
    axes[1, 0].set_ylabel('Cumulative Time Decay Benefit ($)')
    axes[1, 0].set_title('Time Decay Working in Your Favor', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].invert_xaxis()
    
    # Plot 4: Probability Distribution
    from scipy import stats
    
    # Calculate probability of different outcomes
    annual_vol = volatility_30d
    time_to_exp = best_collar['Days'] / 365
    
    # Log-normal distribution parameters
    drift = 0  # Assuming no drift
    sigma = annual_vol * np.sqrt(time_to_exp)
    
    # Calculate probabilities
    prob_below_put = stats.norm.cdf(np.log(best_collar['Put Strike'] / current_price) / sigma)
    prob_above_call = 1 - stats.norm.cdf(np.log(best_collar['Call Strike'] / current_price) / sigma)
    prob_between = 1 - prob_below_put - prob_above_call
    
    labels = [f"Below Put\n(${best_collar['Put Strike']:.0f})", 
              f"Between Strikes\n(${best_collar['Put Strike']:.0f}-${best_collar['Call Strike']:.0f})",
              f"Above Call\n(${best_collar['Call Strike']:.0f})"]
    sizes = [prob_below_put * 100, prob_between * 100, prob_above_call * 100]
    colors = ['red', 'green', 'orange']
    explode = (0.1, 0, 0.1)
    
    axes[1, 1].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90)
    axes[1, 1].set_title('Probability of Outcomes at Expiration', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/workspace/collar_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Probability Analysis for Recommended Collar:")
    print(f"   • {prob_below_put*100:.1f}% chance stock falls below put strike (max loss scenario)")
    print(f"   • {prob_between*100:.1f}% chance stock stays between strikes (optimal scenario)")
    print(f"   • {prob_above_call*100:.1f}% chance stock rises above call strike (capped gain)")

# Implementation guide
print("\n" + "=" * 100)
print("IMPLEMENTATION GUIDE")
print("=" * 100)

if collar_analysis and len(top_collars) > 0:
    recommended = top_collars.iloc[0]
    
    print(f"""
📋 RECOMMENDED COLLAR IMPLEMENTATION

Selected Strategy: {recommended['Type']}
Expiration: {recommended['Expiration']} ({recommended['Days']} days)

1️⃣ TRADE SETUP - PLACE AS A SPREAD ORDER
   
   ORDER TYPE: Buy Put Spread / Sell Call Spread (Collar)
   
   Leg 1: BUY 30 NTRA {recommended['Expiration']} ${recommended['Put Strike']:.0f} PUT
          Limit: ${recommended['Put Premium']:.2f} or better
   
   Leg 2: SELL 30 NTRA {recommended['Expiration']} ${recommended['Call Strike']:.0f} CALL
          Limit: ${recommended['Call Premium']:.2f} or better
   
   NET DEBIT/CREDIT: ${recommended['Per Share']:.2f} per share
   
   IMPORTANT: Enter as a single spread order for better fill

2️⃣ ALTERNATIVE: LEGGING INTO POSITION
   
   If spread order doesn't fill:
   
   Step 1: During morning volatility (9:30-10:30 AM ET)
           SELL the calls first (when stock is strong)
           Order: SELL 30 NTRA {recommended['Call Strike']:.0f} CALL @ ${recommended['Call Premium']:.2f}
   
   Step 2: During afternoon or on a dip
           BUY the puts (when stock weakens)
           Order: BUY 30 NTRA {recommended['Put Strike']:.0f} PUT @ ${recommended['Put Premium']:.2f}

3️⃣ POSITION MANAGEMENT RULES

   ✓ If stock drops to put strike:
     - Collar is working as intended
     - Consider rolling put down and out
     - Or let put protect your position
   
   ✓ If stock rises to call strike:
     - Decide if you want to keep shares
     - Can buy back call and sell higher strike
     - Or let shares be called away for profit
   
   ✓ Time-based management:
     - 21 days before expiration: Start planning roll
     - 14 days before: Execute roll if keeping position
     - 7 days before: Close or prepare for assignment

4️⃣ ADJUSTMENT SCENARIOS

   Scenario A: Stock drops 10% quickly
   → Buy back the call for profit
   → Keep put for protection
   → Sell new call at lower strike when stock stabilizes
   
   Scenario B: Stock rallies 10% quickly  
   → Consider closing entire collar for profit
   → Or roll up both strikes to lock in gains
   
   Scenario C: Stock goes sideways
   → Perfect! Let time decay work
   → Prepare to roll at 14-21 days to expiration

5️⃣ EXIT STRATEGIES

   A. Full Exit:
      - Close both legs simultaneously as spread
      - Best during high volatility periods
   
   B. Partial Exit:
      - Close profitable leg (usually the call if stock drops)
      - Manage remaining leg separately
   
   C. Rolling:
      - Roll entire collar to next expiration
      - Adjust strikes based on new stock price
      - Try to maintain credit or small debit

6️⃣ TAX CONSIDERATIONS

   ⚠️ IMPORTANT: Consult your tax advisor about:
   - Qualified covered call rules
   - Impact on holding period
   - Short-term vs long-term gains
   - Straddle rules for tax purposes

7️⃣ RISK MONITORING

   Set Alerts:
   • Stock at ${recommended['Put Strike']:.0f} (put strike)
   • Stock at ${recommended['Call Strike']:.0f} (call strike)
   • Stock at ${current_price * 0.95:.0f} (5% down)
   • Stock at ${current_price * 1.05:.0f} (5% up)
   • 21 days before expiration
""")

# Final summary
print("\n" + "=" * 100)
print("EXECUTIVE SUMMARY - ACTION PLAN")
print("=" * 100)

print(f"""
🎯 YOUR SITUATION:
• Position: 3,000 shares of NTRA worth ${position_value:,.2f}
• Stock near 52-week high (${current_price:.2f} vs ${high_52w:.2f})
• High volatility environment ({volatility_30d:.1%})
• Perfect setup for collar strategy

✅ RECOMMENDED ACTION:
Implement a {recommended['Days']}-day collar with:
• Downside protection at ${recommended['Put Strike']:.0f} ({recommended['Protection %']:.1f}% below current)
• Upside cap at ${recommended['Call Strike']:.0f} ({recommended['Cap %']:.1f}% above current)
• Net cost: ${recommended['Net Cost/Credit']:,.2f} ({recommended['Per Share']:.2f}/share)

📊 EXPECTED OUTCOMES:
• Maximum Loss: ${recommended['Max Loss']:,.2f} ({recommended['Max Loss']/position_value*100:.1f}% of position)
• Maximum Gain: ${recommended['Max Gain']:,.2f} ({recommended['Max Gain']/position_value*100:.1f}% of position)
• Breakeven: ${recommended['Breakeven']:.2f}
• High probability ({prob_between*100:.0f}%) of optimal outcome

🚀 NEXT STEPS:
1. Review this analysis
2. Check live options prices during market hours
3. Place collar as single spread order
4. Set monitoring alerts
5. Plan for position management

⏰ BEST EXECUTION TIMES:
• Open (9:30-10:00 AM): Often best for selling calls
• Mid-day (11:30-1:30 PM): Lower volatility, tighter spreads
• Close (3:00-4:00 PM): Can be good for puts

Remember: The collar limits both losses AND gains. You're trading unlimited upside 
for downside protection - perfect when stock is at peak levels.
""")

print("=" * 100)
print("Analysis Complete - Collar Strategy Ready for Implementation")
print("=" * 100)