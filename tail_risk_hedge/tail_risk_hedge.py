import datetime
import numpy
import os
import pandas
import pickle
import random
import time
import yfinance
from scipy.optimize import bisect

class YahooFinanceDataProvider:
    def __init__(
        self, ticker='SPY', seed=None, cache_file='price_cache.pkl',
        put_options_cache_file='put_options_cache.pkl', cache_duration=86400
    ):
        if seed is not None:
            random.seed(seed)
        self.ticker = ticker
        self.ticker_data = yfinance.Ticker(ticker)
        self.cache_file = cache_file
        self.put_options_cache_file = put_options_cache_file
        self.cache_duration = cache_duration
        self.risk_free_rate = 0.04
        self.time_to_expiry = 2 / 12
        self.historical_data = self._load_data()
        self.put_options_cache = self._load_put_options_cache()

    def _load_data(self):
        if self._is_cache_valid(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except (FileNotFoundError, pickle.PickleError):
                pass
        data = self._fetch_historical_data()
        self._save_cache(data, self.cache_file)
        if data.empty:
            raise ValueError('No historical data available')
        return data

    def _load_put_options_cache(self):
        if self._is_cache_valid(self.put_options_cache_file):
            try:
                with open(self.put_options_cache_file, 'rb') as f:
                    return pickle.load(f)
            except (FileNotFoundError, pickle.PickleError):
                pass
        return None

    def _is_cache_valid(self, cache_file):
        if not os.path.exists(cache_file):
            return False
        cache_age = time.time() - os.path.getmtime(cache_file)
        return cache_age < self.cache_duration

    def _fetch_historical_data(self):
        data = self.ticker_data.history(period='1y', interval='1d')
        if data.empty:
            raise ValueError('No historical data retrieved from Yahoo Finance')
        return data[['Open', 'High', 'Low', 'Close']].reset_index()

    def _save_cache(self, data, cache_file):
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except OSError as e:
            print(f'Warning: Failed to save cache to {cache_file}: {e}')

    def _binomial_tree_price(self, S, K, T, r, sigma, N=100):
        """Calculate put option price using a binomial tree."""
        dt = T / N
        u = numpy.exp(sigma * numpy.sqrt(dt))
        d = 1 / u
        p = (numpy.exp(r * dt) - d) / (u - d)
        if not 0 <= p <= 1:
            return None  # Invalid probabilities
        discount = numpy.exp(-r * dt)

        # Initialize asset prices at maturity
        stock_prices = numpy.zeros(N + 1)
        stock_prices[0] = S * (d ** N)
        for i in range(1, N + 1):
            stock_prices[i] = stock_prices[i - 1] * u / d

        # Initialize option values at maturity (put option)
        option_values = numpy.maximum(0, K - stock_prices)

        # Backward induction
        for step in range(N - 1, -1, -1):
            for i in range(step + 1):
                option_values[i] = discount * (
                    p * option_values[i + 1] + (1 - p) * option_values[i]
                )
                # Early exercise for American option
                stock_price = S * (u ** (step - i)) * (d ** i)
                option_values[i] = max(option_values[i], K - stock_price)

        return option_values[0]

    def _estimate_implied_volatility(
        self, option_price, price_at_start, strike_price, time_to_expiry, risk_free_rate, scenario='stable', lookback=60
    ):
        """Estimate implied volatility using binomial tree and bisection."""
        # Try VIX first if available
        try:
            vix_data = yfinance.Ticker('^VIX').history(period='1d')
            if not vix_data.empty:
                vix = vix_data['Close'].iloc[-1] / 100  # Convert to decimal
                return vix if scenario != 'crash' else vix * 1.5
        except Exception as e:
            print(f'Warning: Failed to fetch VIX: {e}')

        # Fallback to binomial tree
        def objective(sigma):
            tree_price = self._binomial_tree_price(price_at_start, strike_price, time_to_expiry, risk_free_rate, sigma)
            return tree_price - option_price if tree_price is not None else 1e10

        try:
            # Use bisection to find sigma where tree price matches market price
            sigma = bisect(objective, 0.01, 2.0, xtol=1e-4)
            return sigma if scenario != 'crash' else sigma * 1.5
        except Exception as e:
            print(f'Warning: Binomial tree failed: {e}')
            # Fallback to historical volatility
            if len(self.historical_data) < lookback:
                return 0.2
            closes = self.historical_data['Close'].tail(lookback)
            log_returns = numpy.log(closes / closes.shift(1)).dropna()
            volatility = numpy.std(log_returns) * numpy.sqrt(252)
            return volatility if scenario != 'crash' else volatility * 1.5

    @staticmethod
    def get_date_difference(date1, date2):
        return abs((date1 - date2).days)

    def get_closest_expiration_date(self, expiration_dates, target_date):
        closest_expiration_date = datetime.datetime.strptime(expiration_dates[0], '%Y-%m-%d').date()
        minimum_difference = self.get_date_difference(closest_expiration_date, target_date)

        for expiration_date in expiration_dates:
            expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()
            number_of_days = self.get_date_difference(expiration_date, target_date)
            if number_of_days < minimum_difference:
                minimum_difference = number_of_days
                closest_expiration_date = expiration_date

        if not closest_expiration_date:
            raise ValueError('No suitable option expiration found')
        return pandas.Timestamp(closest_expiration_date, unit='s').strftime('%Y-%m-%d')

    def _fetch_option_chain(self, price_at_start):
        if not self._is_cache_valid(self.put_options_cache_file) or self.put_options_cache is None:
            self.put_options_cache = None
        else:
            cached_puts, cached_expiry, cached_price_range = self.put_options_cache
            if (price_at_start * 0.7 <= cached_price_range[1] and
                price_at_start * 0.9 >= cached_price_range[0]):
                return cached_puts, cached_expiry

        target_date = (datetime.datetime.now() + datetime.timedelta(days=60)).date()
        closest_expiration_date = self.get_closest_expiration_date(
            self.ticker_data.options, target_date
        )
        try:
            option_chain = self.ticker_data.option_chain(closest_expiration_date)
            puts = option_chain.puts
            out_of_the_money_puts = puts[
                (puts['strike'] <= price_at_start * 0.9) &
                (puts['strike'] >= price_at_start * 0.7)
            ]
        except yfinance.exceptions.YFRateLimitError as error:
            print(f'Warning: Failed to fetch option chain: {error}')
            out_of_the_money_puts = None
            puts = None

        price_range = (price_at_start * 0.7, price_at_start * 0.9)
        self.put_options_cache = (out_of_the_money_puts, closest_expiration_date, price_range)
        self._save_cache(self.put_options_cache, self.put_options_cache_file)
        return out_of_the_money_puts, closest_expiration_date

    def get_start_index(self):
        length = len(self.historical_data)
        if length-40 < 0:
            raise ValueError('Insufficient historical data')
        return random.randint(0, length-40)

    def get_price_at_end(self, scenario, start_index, price_at_start):
        end_idx = random.randint(start_index + 1, start_index + 40)
        price_at_end = self.historical_data.loc[end_idx, 'Close']

        if scenario != 'stable' and price_at_end > price_at_start * 0.9:
            price_at_end = price_at_start * random.uniform(0.6, 0.9)
        else:
            if price_at_end > price_at_start * 1.2 or price_at_end < price_at_start * 0.9:
                price_at_end = price_at_start * random.uniform(0.95, 1.1)
        return price_at_end

    def generate_scenario(self, scenario='stable'):
        start_index = self.get_start_index()
        price_at_start = self.historical_data.loc[start_index, 'Close']

        out_of_the_money_puts, put_expiration_date = self._fetch_option_chain(price_at_start)

        if out_of_the_money_puts is None or out_of_the_money_puts.empty:
            put_expiration_date = (
                datetime.datetime.now() + datetime.timedelta(days=60)
            ).strftime('%Y-%m-%d')
            strike_price = price_at_start * random.uniform(0.7, 0.9)
            option_price = max(0.5, min(10, self._estimate_implied_volatility(
                option_price=1.0,  # Placeholder for synthetic pricing
                price_at_start=price_at_start,
                strike_price=strike_price,
                time_to_expiry=self.time_to_expiry,
                risk_free_rate=self.risk_free_rate,
                scenario=scenario
            ) * price_at_start * 0.01))
        else:
            put = out_of_the_money_puts.sample(n=1).iloc[0]
            strike_price = put['strike']
            option_price = put['lastPrice']
            if option_price <= 0:
                option_price = put.get('bid', 0.5) or 0.5

        price_at_end = self.get_price_at_end(scenario, start_index, price_at_start)

        return {
            'price_at_start': price_at_start,
            'price_at_end': price_at_end,
            'strike_price': strike_price,
            'option_price': option_price,
            'expiry_date': put_expiration_date
        }

def calculate_equity_value(portfolio_value, equity_ratio):
    if portfolio_value < 0:
        raise ValueError('Portfolio value cannot be negative')
    return portfolio_value * equity_ratio

def calculate_insurance_budget(portfolio_value, insurance_ratio):
    if portfolio_value < 0:
        raise ValueError('Portfolio value cannot be negative')
    if insurance_ratio < 0:
        raise ValueError('insurance ratio cannot be negative')
    return portfolio_value * insurance_ratio

def calculate_number_of_contracts_to_purchase(insurance_budget, option_price):
    if option_price <= 0:
        raise ValueError('Option price must be positive')
    if insurance_budget < 0:
        raise ValueError('insurance budget cannot be negative')
    return int(insurance_budget / (option_price * 100))

def calculate_option_payoff(strike_price, price_at_end):
    if price_at_end < 0:
        raise ValueError('price end price cannot be negative')
    if strike_price < 0:
        raise ValueError('strike price cannot be negative')
    return max(0, strike_price - price_at_end)

def calculate_price_value_change(price_at_start, price_at_end):
    if price_at_end <= 0:
        raise ValueError('price end price must be positive')
    return (price_at_end - price_at_start) / price_at_start

def calculate_portfolio_metrics(
        *, portfolio_value=0, insurance_ratio=0.1, price_at_start=0, price_at_end=0,
        strike_price=0, option_price=0, expiry_date=0
    ):
    if portfolio_value < 0:
        raise ValueError('Portfolio value cannot be negative')
    if insurance_ratio < 0:
        raise ValueError('insurance ratio cannot be negative')

    equity_ratio = 1 - insurance_ratio
    equity_start = calculate_equity_value(portfolio_value, equity_ratio)
    insurance_budget = calculate_insurance_budget(portfolio_value, insurance_ratio)
    contracts = calculate_number_of_contracts_to_purchase(
        insurance_budget, option_price
    )
    price_change = calculate_price_value_change(price_at_start, price_at_end)
    equity_end = equity_start * (1 + price_change)
    option_payoff = calculate_option_payoff(strike_price, price_at_end)
    portfolio_end_with_insurance = equity_end + (option_payoff * contracts * 100)
    portfolio_end_without_insurance = portfolio_value * (1 + price_change)
    portfolio_change_with_insurance = (
        (portfolio_end_with_insurance - portfolio_value) / portfolio_value
    )
    portfolio_change_without_insurance = (
        (portfolio_end_without_insurance - portfolio_value) / portfolio_value
    )

    scenario = 'stable' if price_at_end >= strike_price else 'crash'
    option_strategy = f'buy {contracts} put contracts at {strike_price} strike price to expire on {expiry_date}'

    return {
        'scenario': scenario,
        'price_value_at_start': round(price_at_start, 2),
        'price_value_at_end': round(price_at_end, 2),
        'price_value_percent_change': round(price_change, 2),
        'equity_at_start': round(equity_start, 2),
        'equity_at_end': round(equity_end, 2),
        'insurance_strategy_cost': round(insurance_budget, 2),
        'insurance_strategy_cost_as_percentage_of_portfolio': insurance_ratio,
        'number_of_contracts': contracts,
        'put_option_price': round(option_price, 2),
        'option_strategy': option_strategy,
        'portfolio_value_at_start': portfolio_value,
        'portfolio_value_at_end_with_insurance': round(portfolio_end_with_insurance, 2),
        'portfolio_value_at_end_without_insurance': round(portfolio_end_without_insurance, 2),
        'portfolio_value_percent_change_with_insurance': round(portfolio_change_with_insurance, 2),
        'portfolio_value_percent_change_without_insurance': round(portfolio_change_without_insurance, 2),
        'portfolio_profit_loss_with_insurance': round(portfolio_end_with_insurance - portfolio_value, 2),
        'portfolio_profit_loss_without_insurance': round(portfolio_end_without_insurance - portfolio_value, 2),
        'difference_between_portfolio_profit_with_insurance_and_without_insurance': round(
            portfolio_end_with_insurance - portfolio_end_without_insurance, 2
        ),
    }