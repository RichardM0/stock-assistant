from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

from utils.cache import cache
from services.maps import label_desc, period_map
from services.chart import generate_chart
from services.market_data import get_market_returns
from utils.finance_utils import (
    ticker_returns,
    calculate_volatility,
    get_buyer_consensus,
    get_max_drawdown,
)
from utils.formatting import format_large_number

app = Flask(__name__)

cache.init_app(app, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
})

@app.route("/", methods=["GET", "POST"])
def home():
    metrics = None
    ticker = ""
    buyer_consensus = "No consensus"
    chart_html = None
    period = "1Y"
    interval = "1M"
    chart_type = "line"
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper()
        period = request.form.get("period", "1Y")
        interval = request.form.get("interval", "1M")
        chart_type = request.form.get("chart_type", "line")

        df = yf.download(ticker, period=period_map[period], interval=period_map[interval])

        if df.empty:
            error = f"'{ticker}' is not a valid ticker symbol."
            return render_template(
                "index.html",
                error=error,
                ticker="",
                period=period,
                interval=interval,
                chart_type=chart_type
            )

        df.reset_index(inplace=True)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        ticker_obj = yf.Ticker(ticker)
        ticker_info = ticker_obj.info
        ticker_fast = ticker_obj.fast_info

        stock_returns = ticker_returns(ticker, period_map[period])
        stock_data = yf.download(ticker, period="1y")
        market_returns = get_market_returns(period_map[period])


        fig = generate_chart(chart_type, df, ticker, interval, period)
        chart_html = fig.to_html(full_html=False, config={"responsive": True})

        div_yield = ticker_info.get("dividendYield")
        div_yield_str = f"{div_yield:.2f}" if div_yield else "N/A"

        try:
            market_cap = format_large_number(ticker_info.get("marketCap"))
        except:
            market_cap = "N/A"

        try:
            beta = f"{ticker_info.get('beta'):.3f}"
        except:
            beta = "N/A"

        metrics = {
            "Current Price": f"{ticker_fast.last_price:.2f}",
            "Market Cap": market_cap,
            "Beta": beta,
            "Volatility": f"{calculate_volatility(stock_returns):.3f}",
            "52W High": f"{stock_data['Close'].max().iloc[0]:.2f}",
            "52W Low": f"{stock_data['Close'].min().iloc[0]:.2f}",
            "Dividend Yield": div_yield_str,
            "Max Drawdown": f"{get_max_drawdown(stock_data).iloc[0]:.2f}",
        }

        buyer_consensus = get_buyer_consensus(ticker_obj)

    return render_template(
        "index.html",
        ticker=ticker,
        period=period,
        interval=interval,
        chart_type=chart_type,
        chart_html=chart_html,
        metrics=metrics,
        buyer_consensus=buyer_consensus,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
