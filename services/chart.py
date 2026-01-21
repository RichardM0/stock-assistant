import plotly.graph_objects as go 
import numpy as np
import pandas as pd
from services.maps import label_desc

def generate_compare_chart(df1, df2, ticker1, ticker2, interval, period):
    returns1 = df1["Close"].pct_change().dropna()
    returns2 = df2["Close"].pct_change().dropna()
    df1["percent"] = np.cumprod(1+returns1)-1
    df2["percent"] = np.cumprod(1+returns2)-1

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df1["Date"],
        y=df1["percent"],
        mode="lines",
        name=ticker1,
        line=dict(width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df2["Date"],
        y=df2["percent"],
        mode="lines",
        name=ticker2,
        line=dict(width=2)
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{ticker1} vs {ticker2} — Cumulative Percentage</b><br>"
                 f"<span style='font-size:12px'>{label_desc[interval]} over {label_desc[period]}</span>",
            x=0.5
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
            ticks="",
            constrain="domain"
        ),
        yaxis=dict(
            title="percent Price (Start = 100)",
            showgrid=True,
            gridcolor="rgba(148,163,184,0.15)",
            ticks=""
        ),
        margin=dict(l=40, r=60, t=60, b=40),
        autosize=True,
        showlegend=True,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB")
        )
    )

    return fig

def generate_chart(chart_type, df, ticker, interval, period):
    fig = go.Figure()

    if chart_type == "candle":
        fig.add_trace(go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            line=dict(color="#38BDF8", width=2)
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>{ticker} — {label_desc[interval]} over {label_desc[period]}</b>",
            x=0.5
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Roboto, Arial, sans-serif", color="#E5E7EB", size=14),
        xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", ticks="", constrain="domain"),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", ticks=""),
        margin=dict(l=40, r=60, t=60, b=40),
        xaxis_rangeslider_visible=False,
        autosize=True,
        showlegend=False
    )

    return fig

def monte_carlo_chart(price_paths, ticker):
    fig = go.Figure()

    # Plot only first 100 paths (performance)
    for i in range(min(100, price_paths.shape[1])):
        fig.add_trace(go.Scatter(
            y=price_paths[:, i],
            mode="lines",
            line=dict(width=1),
            opacity=0.2,
            showlegend=False
        ))

    fig.update_layout(
        title=f"{ticker} — Monte Carlo Price Simulation",
        xaxis_title="Days Ahead",
        yaxis_title="Price",
        template="plotly_dark",
        height=450
    )

    return fig