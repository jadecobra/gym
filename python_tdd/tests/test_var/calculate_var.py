import pandas_datareader
import pandas
import datetime
import numpy
import scipy

def get_prices(ticker=None, start=None, end=None):
    return pandas_datareader.data.DataReader(ticker, 'yahoo', start=start, end=end)['Adj Close']

def get_historical_prices(ticker):
    return pandas_datareader.data.DataReader(ticker, 'yahoo')['Adj Close']

def get_daily_returns(series):
    return numpy.log(series / series.shift(1))

def get_square_daily_returns(series):
    return numpy.square(series)

def get_daily_variance(series):
    return get_square_daily_returns(series).sum() / series.count()

def get_average_daily_returns(series):
    return abs(series.mean())

def get_daily_standard_deviation(series):
    return numpy.sqrt(numpy.square(series).sum() / series.count())

def get_annualized_variance(series):
    return series.sum()

def get_annualized_standard_deviation(series):
    return numpy.sqrt(series.sum())

def get_trading_days():
    return

def get_annualized_return(series):
    # create a function to calculate trading days
    return ((1 + get_average_daily_returns(series)) ** series.count()) - 1

def plot_histogram(returns):
    returns.hist()

def get_percentage(percentile):
    return 1 - (percentile / 100)

def get_zscore_for_dataset(percentile=None, daily_returns=None):
    result = scipy.stats.norm.ppf(
        get_percentage(percentile),
        daily_returns.mean(),
        daily_returns.std()
    )
    print(f'zscore for {percentile}th percentile: {result:.2f}')
    return result

def get_zscore(percentile=None, daily_returns=None):
    result = scipy.stats.norm.ppf(percentile/100)
    print(f'zscore for {percentile}th percentile: {result:.2f}')
    return result

def get_data(prices):
    return pandas.DataFrame({
        'adjusted_close': prices,
        'daily_returns': get_returns(prices),
        'square_daily_returns': get_square_daily_returns(prices),
    }).iloc[::-1]

def portfolio_zscore(value=None, percentile=None, daily_returns=None):
    return (
        portfolio_value
      * get_zscore(
            percentile=percentile,
            daily_returns=daily_returns
        )
    )

def daily_portfolio_zscore(value=None, percentile=None, daily_returns=None):
    return (
        get_daily_standard_deviation(daily_returns)
      * portfolio_zscore(
            value=portfolio_value,
            percentile=percentile,
            daily_returns=daily_returns,
        )
    )

def get_value_at_risk(portfolio_value=None, time=None, daily_returns=None, percentile=None, daily_variance=None):
    return (
        get_annualized_return(daily_returns)
      - daily_portfolio_zscore(
            value=portfolio_value,
            percentile=percentile,
            daily_returns=daily_returns
        )
    )

def calculate_var(portfolio_value=None, daily_returns=None):
    for percentile in (68, 90, 95, 99):
        print(
            get_value_at_risk(
                portfolio_value=portfolio_value,
                percentile=percentile,
                daily_returns=daily_returns,
            )
        )

def get_daily_returns(ticker=None, start=None, end=None):
    return get_returns(
        get_prices(
            ticker=ticker,
            start=start,
            end=end
        )
    )