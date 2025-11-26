# 🖥️ E*TRADE Visual Walkthrough - Collar Execution

## 📍 Navigation Path in E*TRADE

```
E*TRADE Homepage
    ↓
[Trading] Menu
    ↓
[Options]
    ↓
[Trade Options] or [Strategy Builder]
```

---

## 🎯 METHOD 1: Using E*TRADE Strategy Builder (RECOMMENDED)

### Screen 1: Strategy Selection
```
┌─────────────────────────────────────┐
│  Select a Strategy:                 │
│  ○ Covered Call                    │
│  ○ Protective Put                  │
│  ● COLLAR ← SELECT THIS            │
│  ○ Spread                          │
│  ○ Straddle                        │
│  [Next →]                           │
└─────────────────────────────────────┘
```

### Screen 2: Enter Symbol and Shares
```
┌─────────────────────────────────────┐
│  Symbol: [NTRA        ]             │
│  Shares to Protect: [3000    ]      │
│  [Get Options →]                    │
└─────────────────────────────────────┘
```

### Screen 3: Select Expiration
```
┌─────────────────────────────────────┐
│  Select Expiration Date:            │
│  ○ NOV 29 2025 (4 days)           │
│  ● DEC 19 2025 (24 days) ← SELECT  │
│  ○ JAN 16 2026 (52 days)          │
│  [Continue →]                       │
└─────────────────────────────────────┘
```

### Screen 4: Select Strikes
```
┌─────────────────────────────────────┐
│  Select PUT Strike (Protection):    │
│  ○ $200                            │
│  ● $210 ← SELECT                   │
│  ○ $220                            │
│                                     │
│  Select CALL Strike (Cap):          │
│  ○ $250                            │
│  ● $260 ← SELECT                   │
│  ○ $270                            │
│  [Preview Order →]                  │
└─────────────────────────────────────┘
```

### Screen 5: Order Type and Price
```
┌─────────────────────────────────────┐
│  Order Type:                        │
│  ● Limit (Net Credit) ← SELECT      │
│  ○ Market                           │
│                                     │
│  Limit Price: [$0.13  ] Credit      │
│                or better             │
│                                     │
│  Duration:                          │
│  ● Day                              │
│  ○ GTC (Good Till Cancelled)       │
│  [Review Order →]                   │
└─────────────────────────────────────────┘
```

### Screen 6: Order Confirmation
```
┌─────────────────────────────────────┐
│  CONFIRM YOUR COLLAR ORDER          │
│  ════════════════════════════       │
│  Symbol: NTRA                       │
│  Strategy: Collar                   │
│                                     │
│  BUY  +30 DEC 19 $210 PUT          │
│  SELL -30 DEC 19 $260 CALL         │
│                                     │
│  Net Credit: $390.00                │
│  Per Share: $0.13                   │
│                                     │
│  Commission: $39.00                 │
│  Total Credit: $351.00              │
│                                     │
│  [✓ Place Order]  [✗ Cancel]       │
└─────────────────────────────────────┘
```

---

## 🎯 METHOD 2: Manual Spread Entry

### If Strategy Builder Not Available:

#### Step 1: Complex Option Order
```
┌─────────────────────────────────────┐
│  Order Type: [Spread ▼]             │
│  Symbol: [NTRA        ]             │
│  [Add Legs]                         │
└─────────────────────────────────────┘
```

#### Step 2: First Leg (Put)
```
┌─────────────────────────────────────┐
│  LEG 1:                             │
│  Action: [Buy to Open ▼]           │
│  Quantity: [30        ]             │
│  Expiration: [12/19/2025 ▼]        │
│  Strike: [210 ▼]                    │
│  Type: [Put ▼]                      │
│  [+ Add Another Leg]                │
└─────────────────────────────────────┘
```

#### Step 3: Second Leg (Call)
```
┌─────────────────────────────────────┐
│  LEG 2:                             │
│  Action: [Sell to Open ▼]          │
│  Quantity: [30        ]             │
│  Expiration: [12/19/2025 ▼]        │
│  Strike: [260 ▼]                    │
│  Type: [Call ▼]                     │
│  [Continue →]                       │
└─────────────────────────────────────┘
```

---

## 📱 E*TRADE Mobile App Screens

### Mobile Step-by-Step:
```
┌──────────────┐
│    NTRA      │
│   $236.71    │
│              │
│ [Trade]      │
└──────────────┘
      ↓
┌──────────────┐
│Trade Options │
│              │
│ ○ Buy/Sell  │
│ ● Spread     │
│              │
│ [Next]       │
└──────────────┘
      ↓
┌──────────────┐
│Strategy:     │
│ [Collar ▼]   │
│              │
│Shares: 3000  │
│Exp: DEC 19   │
│              │
│Put: $210     │
│Call: $260    │
│              │
│Limit: $0.13C │
│              │
│[Review]      │
└──────────────┘
```

---

## ✅ What Success Looks Like

### After Execution - Positions Screen:
```
┌─────────────────────────────────────────────┐
│  POSITIONS                                  │
│  ═════════════════════════════════          │
│                                             │
│  Stocks:                                    │
│  NTRA    3,000 shares   $710,130.00       │
│                                             │
│  Options:                                   │
│  NTRA DEC 210 P  +30   Long    $7,410     │
│  NTRA DEC 260 C  -30   Short  ($7,800)    │
│                                             │
│  Net Options Position: +$390 Credit         │
│  ═════════════════════════════════          │
│  Strategy: COLLAR (Protected)               │
└─────────────────────────────────────────────┘
```

---

## 🚨 E*TRADE Error Messages & Fixes

### "Order Rejected: Insufficient Buying Power"
```
FIX: Change order to ensure CALL is "Sell to Open" not "Buy"
```

### "Invalid Spread: Legs Don't Match"
```
FIX: Ensure both legs have same expiration (DEC 19)
     and same quantity (30 contracts)
```

### "Options Approval Required"
```
FIX: Call 1-800-387-2331 for Level 2 approval
     (Takes 1-2 business days)
```

### "Shares Unavailable for Covered Call"
```
FIX: Check if shares are:
     - In another open order
     - Already covering other calls
     - On margin/loan
```

---

## 📞 Live Support Script

**When calling E*TRADE (1-800-387-2331):**

"Hi, I need help placing a collar strategy on my position. I own 3,000 shares of NTRA and want to:
1. Buy 30 contracts of December 19th, $210 puts
2. Sell 30 contracts of December 19th, $260 calls
3. As a single spread order for a net credit

Can you help me enter this, or should I use the strategy builder?"

---

## 🎯 Final Verification Checklist

Before clicking SUBMIT, verify:

□ **Strategy Type**: Shows as "Collar" or "Buy Put/Sell Call"  
□ **Symbol**: NTRA (not NTER or other)  
□ **Contracts**: 30 (not 3000 or 3)  
□ **Expiration**: December 19, 2025  
□ **Put Strike**: $210 (buying/long)  
□ **Call Strike**: $260 (selling/short)  
□ **Net Price**: CREDIT of $0.13 or better  
□ **Account**: Your account with 3000 NTRA shares  

---

**IMPORTANT**: Take a screenshot of your order confirmation for records!