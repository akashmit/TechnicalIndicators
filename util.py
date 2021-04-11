import pandas as pd
import os
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(symbol))


def get_data(symbols, dates, colname="Adj Close"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    symbols = ["RUT"] + list(symbols)

    for symbol in symbols:
        df_temp = pd.read_csv(
            symbol_to_path(symbol),
            index_col="Date",
            parse_dates=True,
            usecols=["Date", colname],
            na_values=["nan"],
        )
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)
        if symbol == "RUT":  # drop dates RUT did not trade
            df = df.dropna(subset=["RUT"])

    return df


def fill_na(prices):
    """
    Fill missing values in data frame, in place.
    If a stock was not trading on a valid trading date, we want to fill the price with the value from last day:ffill
    If a stock was not trading at the beginning of the period, we want to fill it with the prices from the front: bfill

    """
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)


def normalize_data(prices):
    """Standardise the data so that the first value of each column is 1"""
    return prices/prices.iloc[0, :]


def plot_data(figure_name, ax, xlabel="Date", ylabel="Normalised Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc='best', fontsize='xx-small')

    plt.savefig('plots/' + figure_name)
    # plt.show()
    plt.close()







