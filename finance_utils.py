import yfinance as yf
import pandas as pd
import numpy as np

# Risk-free rate (3-month US Treasury yield)
rf = yf.Ticker("^IRX").fast_info.last_price / 100

def format_large_number(value):
    if value is None:
        return "N/A"
    abs_value = abs(value)
    if abs_value >= 1e12:
        return f"{value / 1e12:.2f}T"
    elif abs_value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif abs_value >= 1e6:
        return f"{value / 1e6:.2f}M"
    elif abs_value >= 1e3:
        return f"{value / 1e3:.2f}K"
    else:
        return f"{value:.2f}"

def ticker_returns(ticker, period):
    df = yf.download(ticker, period=period, interval="1d")["Close"]
    returns = df.pct_change().dropna()
    return returns            

def calculate_volatility(stock_returns):
    return stock_returns.std().iloc[0] * (252 ** 0.5)

def get_buyer_consensus(ticker_obj):
    trends = ticker_obj.get_recommendations()
    if trends.empty:
        return "No consensus"

    latest_trend = trends.iloc[0]

    buys = latest_trend.get("strongBuy", 0) + latest_trend.get("buy", 0)
    holds = latest_trend.get("hold", 0)
    sells = latest_trend.get("sell", 0) + latest_trend.get("strongSell", 0)
    total = buys + holds + sells

    if total == 0:
        return "No consensus"

    if buys / total > 0.7:
        return "Strong Buy"
    elif buys / total > 0.55:
        return "Buy"
    elif sells / total > 0.65:
        return "Strong Sell"
    elif sells / total > 0.45:
        return "Sell"
    else:
        return "Hold"
def get_max_drawdown(df):
    return (df["Close"]/df["Close"].cummax() - 1).min()
