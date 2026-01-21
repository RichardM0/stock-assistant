import numpy as np
import pandas as pd
import yfinance as yf
from services.simulation_cache import simulation_cache

# Provides a monte carlo simulation to "predict" what the price of a stock will be
#   in some amount of days ahead
def monte_carlo_simulation(ticker, days_ahead, simulations=10000):
    # download recent, but historical data so results are not skewed
    df = yf.download(ticker, period="5y", interval="1d")
    # use log results for better accuracy
    log_returns = np.log(df["Close"] / df["Close"].shift(1)).dropna()

    # initialize mu (mean) and sigma (variance)
    mu = log_returns.mean().item()
    sigma = log_returns.std().item()

    # get the most recent price
    last_price = yf.Ticker(ticker).fast_info['lastPrice'] if yf.Ticker(ticker).fast_info['lastPrice'] else df["Close"].iloc[-1]

    # annualize factor
    dt = 1 / 252

    # create an array of zeros to start simulation
    price_paths = np.zeros((days_ahead, simulations))

    # set first path to the most recent price (stable path)
    price_paths[0] = last_price

    # perform simulation
    for t in range(1, days_ahead):
        z = np.random.normal(0, 1, simulations)
        price_paths[t] = price_paths[t - 1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
        )

    # return simulation results
    return price_paths

# makes sure the simulation isnt ran every single time (efficiency and less randomness)
def get_cached_simulation(ticker, days_ahead):
    key = (ticker, days_ahead)

    if key not in simulation_cache:
        simulation_cache[key] = monte_carlo_simulation(ticker, days_ahead)
    return simulation_cache[key]
