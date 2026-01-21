import numpy as np
import pandas as pd

def monte_carlo_summary(price_paths):
    final_prices = price_paths[-1]

    return {
        "expected": final_prices.mean(),
        "p5": np.percentile(final_prices, 5),
        "p95": np.percentile(final_prices, 95),
        "prob_up": np.mean(final_prices > price_paths[0, 0]) * 100,
        "prob_up5": np.mean(price_paths[-1] > price_paths[0, 0] * 1.05) * 100
    }