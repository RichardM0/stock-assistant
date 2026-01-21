from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

from services.maps import label_desc, period_map
from services.chart import generate_chart, generate_compare_chart, monte_carlo_chart
from services.market_data import get_market_returns
from services.simulation import get_cached_simulation
from services.summary import monte_carlo_summary
from utils.finance_utils import  ticker_returns, calculate_volatility, get_buyer_consensus, get_max_drawdown
from utils.formatting import format_large_number

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    metrics = None
    ticker = ""
    compare_ticker = ""
    buyer_consensus = "No consensus"
    chart_html = None
    period = "1Y"
    interval = "1M"
    chart_type = "line"
    compare_html = None
    error = None
    mc_stats = ""
    last_price = ""

    if request.method == "POST":
        # storing inputs
        ticker = request.form.get("ticker", "").upper()
        compare_ticker = request.form.get("compare_ticker", "").upper()
        period = request.form.get("period", "1Y")
        interval = request.form.get("interval", "1M")
        chart_type = request.form.get("chart_type", "line")
        days_ahead = int(request.form.get("days_ahead", 90))

        # listing ticker information/data
        if ticker:
            df_main = yf.download(ticker, period=period_map[period], interval=period_map[interval])

            if df_main.empty:
                error = f"'{ticker}' is not a valid ticker symbol."
                return render_template(
                    "index.html",
                    error=error,
                    ticker="",
                    period=period,
                    interval=interval,
                    chart_type=chart_type
                )

            df_main.reset_index(inplace=True)

            if isinstance(df_main.columns, pd.MultiIndex):
                df_main.columns = df_main.columns.get_level_values(0)
            
            fig = generate_chart(chart_type, df_main, ticker, interval, period)
            chart_html = fig.to_html(full_html=False, config={"responsive": True})

        if compare_ticker:
            df_compare = yf.download(compare_ticker, period=period_map[period], interval=period_map[interval])

            if df_compare.empty:
                error = f"'{compare_ticker}' is not a valid ticker symbol."
                return render_template(
                    "index.html",
                    error=error,
                    ticker="",
                    period=period,
                    interval=interval,
                    chart_type=chart_type
                )

            df_compare.reset_index(inplace=True)

            if isinstance(df_compare.columns, pd.MultiIndex):
                df_compare.columns = df_compare.columns.get_level_values(0)

            compare_fig = generate_compare_chart(df_main, df_compare, ticker, compare_ticker, interval, period)
            compare_html = compare_fig.to_html(full_html=False, config={"responsive": True})


        # Metrics Section variables/data
        ticker_obj = yf.Ticker(ticker)
        ticker_info = ticker_obj.info
        ticker_fast = ticker_obj.fast_info

        stock_returns = ticker_returns(ticker, period_map[period])
        stock_data = yf.download(ticker, period="1y")
        market_returns = get_market_returns(period_map[period])

        div_yield = ticker_info.get("dividendYield")
        div_yield_str = f"{div_yield:.2f}" if div_yield else "N/A"

        # Summary Section variables/data
        price_paths = get_cached_simulation(ticker, days_ahead)
        mc_stats = monte_carlo_summary(price_paths)
        last_price = ticker_fast["lastPrice"] if ticker_fast["lastPrice"] else df_main["Close"].iloc[-1].item()
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
        compare_ticker=compare_ticker,
        period=period,
        interval=interval,
        chart_type=chart_type,
        chart_html=chart_html,
        compare_html=compare_html,
        metrics=metrics,
        buyer_consensus=buyer_consensus,
        error=error,
        mc_stats=mc_stats,
        last_price=f"{last_price:.2f}",
    )

if __name__ == "__main__":
    app.run(debug=True)
