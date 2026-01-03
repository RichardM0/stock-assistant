from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    ticker = None
    chart_html = None
    period = "1Y"
    interval = "1M"
    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper()
        period = request.form.get("period", "1Y")
        interval = request.form.get("interval", "1M")
        period_map = {
            "1D": "1d",
            "1W": "1wk",
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

        interval_map = {
            "1D": "1d",
            "1W": "1wk",
            "1M": "1mo",
            "1Y": "1y",
        }

        df = yf.download(ticker, period=period_map[period], interval=interval_map[interval])
        df.reset_index(inplace=True)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df["Date"],
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"]
                )
            ]
        )

        fig.update_layout(
            title=f"{ticker} — {label_desc[interval]} intervals over {label_desc[period]}",

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

        fig.update_traces(
            increasing=dict(line=dict(color="#22C55E")),
            decreasing=dict(line=dict(color="#F87171")),
            whiskerwidth=0.4
        )

        chart_html = fig.to_html(
            full_html=False,
            config={"responsive": True}
        )

    return render_template("index.html", chart_html=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
