"""
This module implements the core logic of the project.
The module import util and TechnicalIndicators modules.
The util module contains helper functions, that gather and clean the data
The TechnicalIndicators module contains functions that utilise this data to create 4 trading indicators
ReadME.txt contains further information on the project and the results

If the user wants to produce technical analysis on another stock, they need to change the symbol variable on line 43,
subject to the stock being in the data folder
"""


import datetime as dt
import os
import numpy as np
import pandas as pd
from util import *
from TechnicalIndicators import *



if __name__ == "__main__":

    # Step1- Specify the time-range and the stocks we want to work with
    start_date = '2018-01-01'
    end_date = '2019-12-31'
    dates = pd.date_range(start_date, end_date)

    df = get_data(['AAPL', 'RUN', 'JNJ', 'BA'], dates)

    # The df dataframe will now have the dates for all the above stocks when trading was taking place
    # print(df.head(10))

    # Step2- Deal with Missing values and Normalise the dataset
    fill_na(df)
    df = normalize_data(df)
    df = df.drop(['RUT'], axis=1)  # Drop RUT
    # print(df.head(10))


    # Step3- Technical Indicator Analysis- Enriching the data and producing important statistics
    # We focus on getting technical indicator values and plot for one symbol for now
    symbol = 'RUN'

    # Get the values for the Bollinger Band technical indicator
    rollingMean_df = get_rolling_mean(df[symbol], 20)
    rollingSTD_df = get_rolling_std(df[symbol], 20)
    upper_band, lower_band = get_bollinger_bands(rollingMean_df, rollingSTD_df)
    bollinger_values = get_bollinger_value(df[symbol], lower_band, upper_band)

    # Chart1 - Plot Normalised RUN values, rolling mean and Bollinger Bands
    ax = df[symbol].plot(title="Bollinger Bands", label='Normalised Stock Price')
    rollingMean_df.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='Upper Band', ax=ax)
    lower_band.plot(label='Lower BBand', ax=ax)
    # Call the helper function in util.py to specify labels, legends and save the plot
    plot_data("Bollinger.png", ax, xlabel="Date", ylabel="Units")


    # Get the values for the Momentum technical indicator
    momentum = get_momentum_signal(df[symbol], 20)

    # Chart2 - Plot Normalised RUN values and Momentum signal
    ax = df[symbol].plot(title="Momentum Signal", label='Normalised Stock Price')
    momentum.plot(label='Momentum(%)', ax=ax)
    plot_data("Momentum.png", ax, xlabel="Date", ylabel="Units")


    # Get the values for the SMA indicator
    sma = get_sma_signal(df[symbol], rollingMean_df)

    # Chart3 - Plot Normalised RUN values and SMA signal
    ax = df[symbol].plot(title="SMA Signal", label='Normalised Stock Price')
    rollingMean_df.plot(label='Rolling mean', ax=ax)
    sma.plot(label='SMA(%)', ax=ax)
    plot_data("SMA.png", ax, xlabel="Date", ylabel="Units")


    # Get the values for the Volatility indicator
    daily_returns, vol_signal = compute_volatility_signal(df[symbol], 20)

    # Chart4 - Plot Normalised RUN values and vol signal of daily returns
    ax = df[symbol].plot(title="Volatility Signal", label='Normalised Stock Price')
    daily_returns.plot(label='Daily Return(%)', ax=ax)
    vol_signal.plot(label='Volatility of returns(%)', ax=ax)
    plot_data("Volatility Daily Returns.png", ax, xlabel="Date", ylabel="Units")


    # Producing important statistics for this stock

    cum_return = ((df[symbol][-1] / df[symbol][0]) - 1) * 100
    daily_rets = (df[symbol] / df[symbol].shift(1)) - 1
    daily_rets = daily_rets[1:]
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
    avg_daily_ret *= 100
    std_daily_ret *= 100

    print('Printing Statistics for: ' + symbol)
    print('Sharpe Ratio: ', sharpe_ratio)
    print('Cum Return:', cum_return, '%', '\nStd Daily returns', std_daily_ret, '%', '\nAvg Daily returns', avg_daily_ret, '%\n')




