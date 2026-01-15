import yfinance as yf
import numpy as np
from utils.cache import cache

@cache.memoize(timeout=300)
def ticker_returns(ticker, period):
    prices = yf.download(ticker, period=period, interval="1d")["Close"]
    return prices.pct_change().dropna()

def calculate_volatility(returns):
    return (returns.std() * np.sqrt(252)).iloc[0]

def get_max_drawdown(df):
    return (df["Close"] / df["Close"].cummax() - 1).min()

def get_buyer_consensus(ticker_obj):
    trends = ticker_obj.get_recommendations()
    if trends is None or trends.empty:
        return "No consensus"

    latest = trends.iloc[0]
    buys = latest.get("strongBuy", 0) + latest.get("buy", 0)
    holds = latest.get("hold", 0)
    sells = latest.get("sell", 0) + latest.get("strongSell", 0)
    total = buys + holds + sells

    if total == 0:
        return "No consensus"

    if buys / total > 0.7:
        return "Strong Buy"
    if buys / total > 0.55:
        return "Buy"
    if sells / total > 0.65:
        return "Strong Sell"
    if sells / total > 0.45:
        return "Sell"
    return "Hold"
