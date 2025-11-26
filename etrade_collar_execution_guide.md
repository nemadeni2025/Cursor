# 📱 E*TRADE Collar Strategy Execution Guide
## For Your 3,000 Shares of Natera (NTRA)

---

## 🎯 Quick Reference - Your Collar Trade
**Symbol**: NTRA  
**Current Price**: $236.71  
**Position**: 3,000 shares (30 option contracts)  
**Strategy**: Collar (Protective Put + Covered Call)  
**Net Result**: RECEIVE $390 credit

---

## 📋 Step-by-Step E*TRADE Instructions

### Step 1: Login and Navigate to Options Trading

1. **Log into E*TRADE**
2. Click **"Trading"** tab at the top
3. Select **"Options"** from dropdown menu
4. Choose **"Trade Options"** 

### Step 2: Set Up the Collar Order

#### Option A: Using E*TRADE's Spread Trading Tool (RECOMMENDED)

1. **Select "Spreads" or "Multi-Leg"** option
2. **Choose "Collar"** from strategy list (may be under "Stock/Option Strategies")
3. **Enter Details:**
   ```
   Underlying Symbol: NTRA
   Shares to Cover: 3000
   ```

4. **Select Expiration:**
   ```
   Expiration: DEC 19 2025
   ```

5. **Select Strikes:**
   ```
   Put Strike (Buy): $210
   Call Strike (Sell): $260
   ```

6. **Verify Order Preview Shows:**
   - BUY +30 NTRA DEC 19 '25 $210 PUT
   - SELL -30 NTRA DEC 19 '25 $260 CALL

#### Option B: Manual Entry Using Order Ticket

If collar template not available, use **"Complex Options"** order:

1. **Click "Complex Order" or "Create Spread"**
2. **Add First Leg:**
   ```
   Action: Buy to Open
   Quantity: 30
   Symbol: NTRA
   Expiration: 12/19/2025
   Strike: $210
   Type: Put
   ```

3. **Add Second Leg** (click "+ Add Leg"):
   ```
   Action: Sell to Open
   Quantity: 30
   Symbol: NTRA
   Expiration: 12/19/2025
   Strike: $260
   Type: Call
   ```

### Step 3: Set Order Parameters

**CRITICAL SETTINGS:**

```
Order Type: NET CREDIT (or "Limit")
Limit Price: $0.13 CREDIT (or better)
Duration: Day (or Good Till Cancelled)
Account: [Your account with NTRA shares]
```

**Important**: The order should show as a NET CREDIT, meaning you receive money. If it shows as a debit, adjust the limit price.

### Step 4: Review Order Before Submitting

**Verify ALL Details:**
- [ ] Shows as "Collar" or "Buy Put/Sell Call Spread"
- [ ] 30 contracts each leg (covers 3,000 shares)
- [ ] Net Credit of ~$390 (or $0.13 per share minimum)
- [ ] December 19, 2025 expiration
- [ ] $210 Put (buying) / $260 Call (selling)

**Order Preview Should Look Like:**
```
Collar on NTRA
BUY  +30 NTRA 12/19/25 $210 P
SELL -30 NTRA 12/19/25 $260 C
Net Credit: $390.00 ($0.13 per share)
```

### Step 5: Submit and Monitor

1. **Click "Preview Order"**
2. **Review one final time**
3. **Click "Submit Order"**
4. **Save order confirmation number**

---

## 📊 E*TRADE Collar Using Power E*TRADE (Advanced Platform)

If you have Power E*TRADE access:

1. **Open Power E*TRADE**
2. **Click "Options" then "Strategy Builder"**
3. **Select "Collar" from strategies**
4. **Input:**
   - Symbol: NTRA
   - Shares: 3000
   - Expiry: DEC 19
5. **Auto-populate will suggest strikes**
6. **Adjust to $210P/$260C**
7. **Set limit for credit of $0.13**

---

## 🔧 E*TRADE Mobile App Instructions

1. **Open E*TRADE Mobile App**
2. **Tap "Trade" button**
3. **Select "Options"**
4. **Choose "Spread Order"**
5. **Select "Collar" strategy**
6. **Enter:**
   ```
   NTRA
   30 contracts
   DEC 19 expiration
   $210 Put / $260 Call
   ```
7. **Set as LIMIT order for $0.13 credit**
8. **Swipe to submit**

---

## ⚠️ E*TRADE-Specific Alerts to Set

### In E*TRADE Alerts Section:

1. **Go to "Alerts" under "Trading" menu**
2. **Create New Alerts:**

**Alert 1 - Downside Warning:**
```
Symbol: NTRA
Condition: Last Price <= $215
Alert Type: Email + Text
Name: "NTRA Near Put Strike"
```

**Alert 2 - Upside Warning:**
```
Symbol: NTRA
Condition: Last Price >= $255
Alert Type: Email + Text
Name: "NTRA Near Call Strike"
```

**Alert 3 - Expiration Reminder:**
```
Date Alert: December 5, 2025
Message: "Review NTRA Collar - 2 weeks to expiry"
```

---

## 📱 E*TRADE Position Management

### Where to Monitor Your Collar:

1. **Positions Page**: Will show options separately
2. **Options Positions**: Shows P&L for each leg
3. **Risk Analyzer**: Shows combined position Greeks
4. **Options Chain**: Monitor bid/ask spreads

### How It Will Display:
```
Stock Position:
NTRA: 3,000 shares @ [your cost basis]

Options Positions:
Long 30 NTRA DEC 210 P
Short 30 NTRA DEC 260 C
```

---

## 🚫 Common E*TRADE Issues & Solutions

### Issue 1: "Insufficient Buying Power"
**Solution**: The collar should be a credit. Check that you're selling the call, not buying it.

### Issue 2: "Options Level Required"
**Solution**: Collar requires Level 2 options approval. Call E*TRADE if needed: **1-800-387-2331**

### Issue 3: Order Won't Fill
**Solution**: 
1. Widen the spread slightly (accept $0.10 credit instead of $0.13)
2. Try "legging in" - execute call and put separately
3. Use "Mid Price" selection if available

### Issue 4: "Shares Not Available"
**Solution**: Ensure shares aren't already committed to another covered call. Check "Positions" page.

---

## 📞 E*TRADE Support for Options Help

**Options Trading Desk**: 1-800-387-2331 (say "Options Trading")
**Hours**: Monday-Friday, 8 AM - 6 PM ET

**What to Tell Them:**
*"I want to place a collar on my 3,000 shares of NTRA. Buy 30 December $210 puts and sell 30 December $260 calls as a spread order for a net credit."*

---

## ✅ E*TRADE Execution Checklist

**Before Market Open:**
- [ ] Log into E*TRADE
- [ ] Verify 3,000 NTRA shares available
- [ ] Check current NTRA price
- [ ] Review options chain for current bid/ask

**At Market Open (9:30 AM ET):**
- [ ] Navigate to Options Trading
- [ ] Select Collar/Spread strategy
- [ ] Enter trade details
- [ ] Set as NET CREDIT limit order
- [ ] Submit order

**After Execution:**
- [ ] Save confirmation number
- [ ] Set price alerts
- [ ] Add calendar reminder for Dec 5
- [ ] Screenshot positions page

---

## 📊 How to Track Your Collar in E*TRADE

### Daily Monitoring:
1. **Check "Positions"** tab
2. Look for combined P&L
3. Monitor "Days to Expiration"

### Weekly Review:
1. Go to **"Performance"** tab
2. Select **"Options Analysis"**
3. Review collar effectiveness

### Near Expiration:
1. Use **"Options Roll"** feature
2. Or close positions individually
3. E*TRADE will alert about expiring options

---

## 🔄 Rolling Your Collar in E*TRADE

**Two Weeks Before Expiry (Dec 5):**

1. Go to **"Options Positions"**
2. Select both collar positions
3. Click **"Roll"** button
4. Choose new expiration (January)
5. Adjust strikes if needed
6. Submit as spread order

---

## 💡 E*TRADE Pro Tips

1. **Use "Snap Ticket"** for faster order entry
2. **Save as "Template"** for future collars
3. **Enable "Real-Time Quotes"** for options
4. **Use "Strategy Scanner"** to compare alternatives
5. **Set "Auto-Exercise" settings appropriately

---

## 📝 Final E*TRADE Notes

- E*TRADE commissions: $0.65 per option contract (30 × 2 × $0.65 = $39 total)
- Assignment fees: $38 if exercised
- No fee for closing positions before expiration
- E*TRADE will handle exercise/assignment automatically

**Remember**: Place order as a SPREAD for better fill. If you can't get filled at $0.13 credit, try $0.10 or even break-even rather than paying a debit.

---

**Need Help?** 
- E*TRADE Options Desk: 1-800-387-2331
- Live Chat: Available in platform
- Visit: E*TRADE branch location

---

*Save this guide for reference when executing your collar strategy on E*TRADE.*