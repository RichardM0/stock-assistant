# MeRich — Stock Analysis Dashboard

MeRich is a **Flask-based stock analysis web application** that allows users to explore, visualize, and analyze stocks in real-time. It provides interactive charts, key financial metrics, consensus ratings, and Monte Carlo projections for future stock performance.

---

## Features

### 1. Stock Search & Visualization
- Search for any stock ticker symbol (e.g., AAPL, TSLA).
- Select the time period: 1 Day, 1 Week, 1 Month, 1 Year, 5 Years, Max, or Year-to-Date.
- Choose chart type: **Line** or **Candlestick**.
- Interactive Plotly charts display historical stock prices.

### 2. Financial Metrics
- **Current Price**
- **Market Capitalization**
- **Beta**
- **Volatility** (annualized)
- **52-Week High / Low**
- **Dividend Yield**
- **Maximum Drawdown**

### 3. Buyer Consensus
- Shows analyst ratings including **Buy, Strong Buy, Hold, Sell, Strong Sell**.
- Derived from the latest analyst recommendations.

### 4. Monte Carlo Projection (90 Days)
- Simulates 90-day future stock prices using a Monte Carlo model.
- Provides:
  - **Expected price**
  - **90% confidence range**
  - **Probability of increase**
  - **Probability of increasing by over 5%**
 
## Comparing Two Stocks

MeRich allows you to compare **two stock tickers side by side**, providing insights into their historical performance, volatility, and key metrics.

### How to Use

1. Enter the **first ticker** in the search bar.
2. Enter the **second ticker** in the comparison field
3. Click **Refresh Chart**.

### Features

- Side-by-side **cumulative returns comparison** on the interactive Plotly chart.
- Compare similarity between each ticker
  - Correlation
  - Covariance
- Quickly identify stronger or weaker performers over the selected period.

### Benefits

- Analyze relative performance before making investment decisions.
- Make informed comparisons using both historical and projected data.

### 6. Performance Optimizations
- **Server-side caching** reduces redundant Monte-Carlo simulations
- Reduced yFinance API calls by caching data

### 7. Clean Architecture
- `app.py`: Routing and orchestration.
- `services/`: Data retrieval, chart generation, market benchmarks.
- `utils/`: Financial calculations and formatting.
- Modular design makes the app maintainable and easy to extend.

---

## Technologies
- **Backend:** Python, Flask, Flask-Caching  
- **Data:** yfinance, pandas, numpy  
- **Visualization:** Plotly  
- **Frontend:** HTML, CSS, JavaScript (Bootstrap-inspired styling)

---

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/merich.git
   cd merich
   Setup & Installation

2. Create and activate a virtual environment

Linux / macOS
```
python -m venv venv
source venv/bin/activate
```

Windows (Command Prompt)
```
python -m venv venv
venv\Scripts\activate
```

Windows (PowerShell)
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies
```
pip install -r requirements.txt
```

3. Run the application
```
python app.py
```

## You should see:
```
Running on http://127.0.0.1:5000/
 (Press CTRL+C to quit)
```

## Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

## You can now:

Enter a stock ticker

Select the period, interval, and chart type

View charts, metrics, and Monte Carlo projections```
