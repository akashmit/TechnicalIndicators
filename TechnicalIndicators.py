import datetime as dt
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_rolling_mean(prices, window):
    """Return rolling mean for a specified window size"""
    return prices.rolling(window=window).mean()


def get_rolling_std(prices, window):
    """Return rolling std for a specified window size"""
    return prices.rolling(window=window).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower bollinger bands"""
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd

    return upper_band, lower_band


def get_bollinger_value(prices, lower_band, upper_band):
    bollinger_value = ((prices - lower_band) / (upper_band - lower_band) - 1) / 2
    return bollinger_value

    # So if bg > 0.0: Sell signal- Price has deviated too much upwards
    # If bg < -0.5: Buy signal- Price has deviated too much downwards


def get_momentum_signal(prices, window):
    """Returns the momentum signal for the last xth day"""

    momentum = prices / prices.shift(window) - 1

    return momentum


def get_sma_signal(prices, rolling_mean):
    # If sma is a big negative value- BUY, else if sma is a big positive value- SELL
    # Usually the value is again in the range [-0.5, 0.5].
    # THe idea is that when value is say > 0.2, price is quite high compared to SMA, so sell!!
    sma = prices / rolling_mean - 1

    return sma


def compute_volatility_signal(prices, window):
    """Compute and return the daily return values."""

    daily_returns = (prices / prices.shift(1)) - 1
    volatility_signal = daily_returns.rolling(window=window).std()

    return daily_returns, volatility_signal
