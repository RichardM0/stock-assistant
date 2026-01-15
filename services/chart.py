import plotly.graph_objects as go 
from services.maps import label_desc


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
        xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", ticks=""),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)", ticks=""),
        margin=dict(l=40, r=60, t=60, b=40),
        xaxis_rangeslider_visible=False,
        autosize=True,
        showlegend=False
    )

    return fig