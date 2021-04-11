Steps taken to Formulate the data:

1- Extracted relevant data from Yahoo finance. Chose 4 different industries and one stock per industry from 2018-2019,
when the market was not as volatile.
AAPL: Stock Price for Apple (Information Technology)
RUN: Stock Price for Sunrun (Energy)
JNJ: Stock Price for Johnson & Johnson (Healthcare)
BA: Stock Price for Boeing (Industrials)


2- Created a util.py file, which reads in the data from the data folder and cleanses the data.

The core of util.py file is the get_data function.
The get_data function taken in a symbol(example RUN), and a range of dates. For each of these symbols, it extracts
prices for the date range, choosing the 'Adjusted Close' column as that is the column we most aptly resembles stock prices.
It combines the 'Adjusted Close' for all the symbols(i.e. stocks) into one dataframe. So the final dataframe from this
function will be a dataframe where the index is the dates and the column names are the stock symbols, with values
representing the Adjusted Close.
We also add in a Benchmark index- Russel 2000 here. There are two reasons for adding this-
1- To have a benchmark comparison for a trading strategy
2- To filter out days on which the market was closed for all other stocks.

The above get_data function relies on the symbol_to_path function, which returns the valid path to read in a file from.
Since our base path is the current working directory, and the data is stored in 'data', we add in 'data' to filepath
to read in data easily for multiple files.

util.py also contains functions that cleanses the data.
The fill_na function forward and backward fills prices so as to not leave any gaps in price.
The normalize_data function standardises the data to be able to compare prices across different stocks
By cleaning this data we make sure that every date within the date-range will have a valid price

util.py also has a function that acts as a helper to plot data and generate graphs- plot_data.


3- Created a TechnicalIndicators.py file, that creates 4 technical indicators-
Bollinger Bands, Momentum, Simple Moving Average and Volatility.
These signals can be used as standalone, or can be combined together to form effective Buy/Sell signals.


4- The main.py file utilises the above files and functions-

a) It reads in data for the symbol and data fields provides.
b) It selects one symbol and gathers the values of all indicators for this symbol
c) It plots the normalised stock price of the symbol wrt each indicator, which can be used to generated trading signals
d) It generates important statistics for the stock symbol

All output graphs produced by running this script can be found in this directory with the '.png' extension


Relevant Applications- Trading Strategy:

As a next step, the idea would be to combine these different indicators into a dataframe for a particular stock.
We could then apply a manual trading strategy by selecting thresholds and combinations of different indicators based
on which the strategy would buy/sell.

An example would be-
sell_signal = bollinger.iloc[i][symbol] > 0.0 and momentum.iloc[i][symbol] < -0.1 and sma.iloc[i][symbol] < 0.05)

Based on such a signal we could sell a certain number of shares, and accordingly create a portfolio.

We could further augment this manual trading strategy into a Machine Learning trading strategy by finding optimal
parameters for the thresholds and combinations. For this, classification algorithms such as Random Forrest can work
particularly well. The idea here would be that our indicators would form x_training_data. For our y_training_data,
we could use a simple percentage change formula and accordingly create y_label of -1/0/1 (for do sell/do nothing/buy).
We would then train our Random Forrest model with these(x_training_data, y_training_data) tuples.
To test how well this strategy does, we could select a future time-period(to avoid biases) and obtain the indicator
values(which would form the x_test_data). The algorithm would then be queried and the output would be y_labels, signaling
if we should buy/sell/do nothing.

