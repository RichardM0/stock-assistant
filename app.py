from flask import Flask, render_template, request
import yfinance as yf
from finance_utils import (
    format_large_number,
    ticker_returns,
    calculate_volatility,
    get_buyer_consensus,
    get_max_drawdown,
    rf
)
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def home():
    metrics = None
    ticker = ""
    buyer_consensus = "No consensus"
    chart_html = None
    period = "1Y"
    interval = "1M"
    chart_type = "line"
    stock_data = None

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper()
        period = request.form.get("period", "1Y")
        interval = request.form.get("interval", "1M")
        chart_type = request.form.get("chart_type", "line")
        stock_data = yf.download(ticker, period="1y", interval="1d")

        market_returns = ticker_returns("^GSPC", period_map[period])
        stock_returns = ticker_returns(ticker, period_map[period])

        df = yf.download(ticker, period=period_map[period], interval=period_map[interval])
        df.reset_index(inplace=True)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Create chart
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
            font=dict(family="Roboto, Arial, sans-serif", color="#E5E7EB", size=14),
            xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False, showline=False, ticks=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", zeroline=False, showline=False, ticklabelstandoff=12, ticks=""),
            margin=dict(l=40, r=60, t=60, b=40),
            xaxis_rangeslider_visible=False,
            autosize=True,
            showlegend=False
        )

        chart_html = fig.to_html(full_html=False, config={"responsive": True})

        ticker_obj = yf.Ticker(ticker)
        ticker_fast_info = ticker_obj.fast_info
        ticker_info = ticker_obj.info

        div_yield = ticker_info.get("dividendYield")
        if div_yield is not None:
            div_yield_str = f"{div_yield:.2f}"
        else:
            div_yield_str = "N/A"

        metrics = {
            "Current Price": f"{ticker_fast_info.last_price:.2f}",
            "Market Cap": f"{format_large_number(ticker_info.get('marketCap'))}",
            "Beta": f"{ticker_info.get('beta'):.3f}",
            "Volatility": f"{calculate_volatility(stock_returns):.3f}",
            "52W High": f"{stock_data["Close"].max().iloc[0]:.2f}",
            "52W Low": f"{stock_data["Close"].min().iloc[0]:.2f}",
            "Dividend Yield": div_yield_str,
            "Max Drawdown": f"{get_max_drawdown(stock_data).iloc[0]:.2f}",
        }

        buyer_consensus = get_buyer_consensus(ticker_obj)

    return render_template(
        "index.html",
        period=period,
        interval=interval,
        ticker=ticker,
        chart_html=chart_html,
        metrics=metrics,
        buyer_consensus=buyer_consensus,
        chart_type=chart_type,
    )


if __name__ == "__main__":
    app.run(debug=True)

