from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

app = Flask(__name__)

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

rf = yf.Ticker("^IRX").fast_info.last_price / 100

def calculate_alpha(stock_returns, market_returns, risk_free_rate=0.02):
    beta = calculate_beta(stock_returns, market_returns)

    annual_stock_return = stock_returns.mean() * 252
    annual_market_return = market_returns.mean() * 252

    alpha = annual_stock_return - (
        risk_free_rate + beta * (annual_market_return - risk_free_rate)
    )
    return alpha

def calculate_sharpe(stock_returns):
    excess_returns = stock_returns - (rf / 252)

    sharpe = (
        excess_returns.mean() / excess_returns.std()
    ) * np.sqrt(252)

    return sharpe

def get_buyer_consensus(ticker):
    trends = ticker.get_recommendations()

    if trends.any() is None:
        return "No consensus"
    
    latest_trend = trends.iloc[0]

    buys = latest_trend.get("strongBuy", 0) + latest_trend.get("buy", 0)
    holds = latest_trend.get("hold", 0)
    sells = latest_trend.get("sell", 0) + latest_trend.get("strongSell", 0)
    total = buys + holds + sells

    if buys / total > 0.7:
        return "Strong Buy"
    elif buys / total > 0.55:
        return "Buy"
    elif sells / total > 0.45:
        return "Sell"
    elif sells / total > 0.65:
        return "Strong Sell"
    else:
        return "Hold"
    



@app.route("/", methods=["GET", "POST"])
def home():
    metrics = None
    ticker = ""
    buyer_consensus = "No consensus"
    chart_html = None
    market_returns = None
    stock_returns = None
    period = "1Y"
    interval = "1M"
    chart_type = "line"
    
    period_map = {
        "1D": "1d",
        "1W": "5d",
        "1M": "1mo",
        "1Y": "1y",
        "5Y": "5y",
        "MAX": "max",
        "YTD": "ytd",
    }
    label_desc = {
        "1D": "1 Day",
        "1W": "1 Week",
        "1M": "1 Month",
        "1Y": "1 Year",
        "5Y": "5 Years",
        "MAX": "Max",
        "YTD": "Year to Date",
    }

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper()
        period = request.form.get("period", "1Y")
        interval = request.form.get("interval", "1M")
        market_returns = ticker_returns("^GSPC", period)
        stock_returns = ticker_returns(ticker ,period)
        chart_type = request.form.get("chart_type", "line")

        df = yf.download(ticker, period=period_map[period], interval=period_map[interval])
        df.reset_index(inplace=True)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        fig = go.Figure()

        if chart_type == "candle":
            fig.add_trace(
                go.Candlestick(
                    x=df["Date"],
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"]
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df["Close"],
                    mode="lines",
                    line=dict(color="#38BDF8", width=2)
                )
            )



        fig.update_layout(
            title=dict(
                text=f"<b>{ticker} -- {label_desc[interval]} over {label_desc[period]}</b>",
                x=0.5,
                xanchor="center"
            ),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Roboto, Arial, sans-serif",
                color="#E5E7EB",
                size=14
            ),

            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(148,163,184,0.15)",
                zeroline=False,
                showline=False,
                ticks=""
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(148,163,184,0.15)",
                zeroline=False,
                showline=False,
                ticklabelstandoff=12,
                ticks=""
            ),

            margin=dict(l=40, r=60, t=60, b=40),
            xaxis_rangeslider_visible=False,
            autosize=True,
            showlegend=False
        )

        chart_html = fig.to_html(
            full_html=False,
            config={"responsive": True}
        )

        ticker_obj = yf.Ticker(ticker)
        ticker_fast_info = ticker_obj.fast_info
        ticker_info = ticker_obj.info

        metrics={
            "Current Price": f" {ticker_fast_info.last_price:.2f}",
            "Market Cap": f" {format_large_number(ticker_info.get('marketCap'))}",
            "Beta": f" {ticker_info["beta"]}",
        }

        buyer_consensus = get_buyer_consensus(ticker_obj)

    return render_template("index.html",period=period, 
                                        interval=interval, 
                                        ticker=ticker, 
                                        chart_html=chart_html, 
                                        metrics=metrics,
                                        buyer_consensus=buyer_consensus,
                                        chart_type=chart_type,)

if __name__ == "__main__":
    app.run(debug=True)
