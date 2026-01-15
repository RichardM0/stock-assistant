from utils.finance_utils import (
    ticker_returns,
)

def get_market_returns(period):
    market_returns = ticker_returns("^SPX", period=period)
    return market_returns
