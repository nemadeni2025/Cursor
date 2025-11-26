# Natera Options Hedging Analysis

## Overview
This repository contains a comprehensive Jupyter notebook for analyzing options hedging strategies for a position of 3,000 shares of Natera (NTER).

## Features
- Real-time stock and options data fetching
- Historical volatility analysis
- Multiple hedging strategy evaluation:
  - Protective Puts
  - Covered Calls
  - Collar Strategies
- Profit/Loss scenario modeling
- Risk metrics and probability analysis
- Personalized recommendations based on investor profile
- Implementation guide with sample trade orders

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Launch Jupyter Notebook:
```bash
jupyter notebook natera_options_hedging_analysis.ipynb
```

## Usage

1. Open the notebook in Jupyter
2. Run all cells sequentially (Cell → Run All)
3. The notebook will:
   - Fetch current Natera stock data
   - Analyze available options chains
   - Calculate optimal hedging strategies
   - Generate visualizations and recommendations

## Key Sections

1. **Current Position Analysis** - Overview of your 3,000 share position
2. **Historical Volatility** - Analysis of price movements and risk
3. **Options Analysis** - Available options chains and pricing
4. **Strategy Comparison** - Detailed analysis of each hedging approach
5. **P&L Scenarios** - Visualization of outcomes under different price movements
6. **Risk Metrics** - Statistical analysis and probability assessments
7. **Recommendations** - Tailored suggestions based on different investor profiles
8. **Implementation Guide** - Step-by-step execution instructions

## Important Notes

- Options data is fetched in real-time from Yahoo Finance
- Analysis assumes standard option contract size of 100 shares
- All calculations are for educational purposes
- Consult with a financial advisor before implementing any strategy

## Customization

To analyze a different position size or ticker:
1. Modify the `SHARES_OWNED` variable (currently set to 3000)
2. Change the `TICKER` variable if analyzing a different stock
3. Re-run all cells to update the analysis

## Disclaimer

This tool is for educational and informational purposes only. It is not financial advice. Options trading involves substantial risk and is not suitable for all investors. Always consult with a qualified financial advisor before making investment decisions.