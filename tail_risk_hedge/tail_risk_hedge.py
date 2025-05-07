import datetime
import functools
import numpy
import os
import pandas
import pickle
import requests
import random
import time
import yfinance

def backoff_retries(max_retries=3, base_delay=1, cache_type=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0] if args else None  # Instance for accessing cache
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except yfinance.exceptions.YFRateLimitError:
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                    else:
                        if self and cache_type:
                            try:
                                cached_data = self._load_cached_data(cache_type)
                                if cached_data is not None:
                                    if cache_type == 'historical' and (cached_data.empty or cached_data is None):
                                        raise ValueError("Cached historical data is empty")
                                    print(f"Using cached {cache_type} data due to persistent rate limit error")
                                    return cached_data
                                else:
                                    raise ValueError(f"No valid cached {cache_type} data available")
                            except (FileNotFoundError, pickle.PickleError, ValueError) as e:
                                raise ValueError(f"Failed to load cached {cache_type} data: {e}")
                        raise
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                    else:
                        raise ValueError(f"Network error: {e}")
        return wrapper
    return decorator

class YahooFinanceDataProvider:
    CACHE_VERSION = '1.0'

    def __init__(self, *, ticker="SPY", seed=None, cache_file="price_cache.pkl", put_options_cache_file="put_options_cache.pkl", vix_cache_file="vix_cache.pkl", cache_duration=86400, risk_free_rate=0.04, time_to_expiry=2/12):
        if seed is not None:
            random.seed(seed)
        self.ticker = ticker
        self.ticker_data = yfinance.Ticker(ticker)
        self.cache_duration = cache_duration
        self.risk_free_rate = risk_free_rate
        self.time_to_expiry = time_to_expiry
        self.cache_files = {
            'historical': cache_file,
            'put_options': put_options_cache_file,
            'vix': vix_cache_file
        }
        self.historical_data = self._load_cached_data('historical', self._fetch_historical_data)
        self.put_options_cache = self._load_cached_data('put_options', default_value=None)
        self.vix_cache = self._load_cached_data('vix', default_value=None)

    def _load_cached_data(self, cache_type, fetch_function=None, default_value=None):
        cache_file = self.cache_files[cache_type]
        if self._is_cache_valid(cache_file):
            try:
                with open(cache_file, "rb") as f:
                    cache_data = pickle.load(f)
                    if cache_data.get('version') != self.CACHE_VERSION:
                        raise ValueError("Invalid cache version")
                    data = cache_data['data']
                    if cache_type == 'historical' and (data is None or data.empty):
                        raise ValueError("No historical data available")
                    return data
            except (FileNotFoundError, pickle.PickleError, ValueError, KeyError):
                pass
        if fetch_function is not None:
            data = fetch_function()
            self._save_cache(data, cache_file)
            return data
        return default_value

    def _is_cache_valid(self, cache_file):
        if not os.path.exists(cache_file):
            return False
        cache_age = time.time() - os.path.getmtime(cache_file)
        return cache_age < self.cache_duration

    def _save_cache(self, data, cache_file):
        try:
            cache_data = {'version': self.CACHE_VERSION, 'data': data}
            with open(cache_file, "wb") as f:
                pickle.dump(cache_data, f)
        except OSError as e:
            print(f"Warning: Failed to save cache to {cache_file}: {e}")

    @backoff_retries(cache_type='historical')
    def _fetch_historical_data(self):
        time.sleep(0.1)  # Throttle requests
        data = self.ticker_data.history(period="1y", interval="1d")
        if data.empty:
            raise ValueError("No historical data retrieved from Yahoo Finance")
        return data[["Open", "High", "Low", "Close"]].reset_index()

    @backoff_retries(cache_type='vix')
    def _fetch_vix_data(self):
        time.sleep(0.1)  # Throttle requests
        vix_data = yfinance.Ticker("^VIX").history(period="1d")
        if not vix_data.empty:
            return vix_data["Close"].iloc[-1] / 100
        return None

    def _calculate_historical_volatility(self, lookback=60):
        if len(self.historical_data) < lookback:
            raise ValueError("Insufficient historical data for volatility calculation")
        closes = self.historical_data["Close"].tail(lookback)
        log_returns = numpy.log(closes / closes.shift(1)).dropna()
        return numpy.std(log_returns) * numpy.sqrt(252)

    def _get_volatility(self, scenario="stable"):
        if self.vix_cache is not None:
            volatility = self.vix_cache
            return volatility if scenario != "crash" else volatility * 1.5
        volatility = self._fetch_vix_data()
        if volatility is not None:
            self.vix_cache = volatility
            self._save_cache(volatility, self.cache_files['vix'])
            return volatility if scenario != "crash" else volatility * 1.5
        return 0.2 if scenario != "crash" else 0.3

    def _estimate_implied_volatility(self, *, option_price, price_at_start, strike_price, time_to_expiry, risk_free_rate, scenario="stable"):
        volatility = self._get_volatility(scenario)
        if volatility > 0:
            return volatility
        try:
            return self._calculate_historical_volatility()
        except ValueError:
            return 0.2 if scenario != "crash" else 0.3

    def get_date_difference(self, date1, date2):
        return abs((date1 - date2).days)

    def get_closest_expiration_date(self, expiration_dates, target_date):
        if not expiration_dates:
            raise ValueError("No expiration dates available")
        closest_date = datetime.datetime.strptime(expiration_dates[0], "%Y-%m-%d").date()
        min_diff = self.get_date_difference(closest_date, target_date)
        for date in expiration_dates:
            exp_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            diff = self.get_date_difference(exp_date, target_date)
            if diff < min_diff:
                min_diff = diff
                closest_date = exp_date
        return pandas.Timestamp(closest_date).strftime("%Y-%m-%d")

    @backoff_retries(cache_type='put_options')
    def _fetch_option_chain(self, price_at_start):
        time.sleep(0.1)  # Throttle requests
        cache = self._load_cached_data('put_options')
        if cache and price_at_start * 0.7 <= cache[2][1] and price_at_start * 0.9 >= cache[2][0]:
            return cache[0], cache[1]
        if not self.ticker_data.options:
            raise ValueError("No options data available for ticker")
        target_date = (datetime.datetime.now() + datetime.timedelta(days=60)).date()
        expiry_date = self.get_closest_expiration_date(self.ticker_data.options, target_date)
        option_chain = self.ticker_data.option_chain(expiry_date)
        puts = option_chain.puts
        out_of_the_money_puts = puts[(puts["strike"] <= price_at_start * 0.9) & (puts["strike"] >= price_at_start * 0.7)]
        price_range = (price_at_start * 0.7, price_at_start * 0.9)
        self.put_options_cache = (out_of_the_money_puts, expiry_date, price_range)
        self._save_cache(self.put_options_cache, self.cache_files['put_options'])
        return out_of_the_money_puts, expiry_date

    def get_start_index(self):
        length = len(self.historical_data)
        if length - 40 < 0:
            raise ValueError("Insufficient historical data")
        return random.randint(0, length - 40)

    def get_price_at_end(self, scenario, start_index, price_at_start):
        end_idx = random.randint(start_index + 1, start_index + 40)
        price_at_end = self.historical_data.loc[end_idx, "Close"]
        if scenario != "stable" and price_at_end > price_at_start * 0.9:
            price_at_end = price_at_start * random.uniform(0.6, 0.9)
        elif price_at_end > price_at_start * 1.2 or price_at_end < price_at_start * 0.9:
            price_at_end = price_at_start * random.uniform(0.95, 1.1)
        return price_at_end

    def generate_scenario(self, scenario="stable"):
        start_index = self.get_start_index()
        price_at_start = self.historical_data.loc[start_index, "Close"]
        puts, expiry_date = self._fetch_option_chain(price_at_start)
        if puts is None or puts.empty:
            strike_price = price_at_start * random.uniform(0.7, 0.9)
            volatility = self._estimate_implied_volatility(
                option_price=1.0,
                price_at_start=price_at_start,
                strike_price=strike_price,
                time_to_expiry=self.time_to_expiry,
                risk_free_rate=self.risk_free_rate,
                scenario=scenario
            )
            option_price = max(0.5, min(10, volatility * price_at_start * 0.01))
        else:
            put = puts.sample(n=1).iloc[0]
            strike_price = put["strike"]
            option_price = put["lastPrice"] if put["lastPrice"] > 0 else put.get("bid", 0.5)
        price_at_end = self.get_price_at_end(scenario, start_index, price_at_start)
        return {
            "price_at_start": price_at_start,
            "price_at_end": price_at_end,
            "strike_price": strike_price,
            "option_price": option_price,
            "expiry_date": expiry_date
        }

def calculate_equity_value(portfolio_value, equity_ratio):
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    return portfolio_value * equity_ratio

def calculate_insurance_budget(portfolio_value, insurance_ratio):
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    if insurance_ratio < 0:
        raise ValueError("Insurance ratio cannot be negative")
    return portfolio_value * insurance_ratio

def calculate_number_of_contracts(insurance_budget, option_price):
    if insurance_budget < 0:
        raise ValueError("Insurance budget cannot be negative")
    if option_price <= 0:
        raise ValueError("Option price must be positive")
    return int(insurance_budget / (option_price * 100))

def calculate_option_payoff(strike_price, price_at_end):
    if strike_price < 0:
        raise ValueError("Strike price cannot be negative")
    if price_at_end < 0:
        raise ValueError("Price at end cannot be negative")
    return max(0, strike_price - price_at_end)

def calculate_price_change(price_at_start, price_at_end):
    if price_at_end <= 0:
        raise ValueError("Price at end must be positive")
    return (price_at_end - price_at_start) / price_at_start

def calculate_portfolio_metrics(*, portfolio_value, insurance_ratio, price_at_start, price_at_end, strike_price, option_price, expiry_date):
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    if insurance_ratio < 0:
        raise ValueError("Insurance ratio cannot be negative")
    equity_ratio = 1 - insurance_ratio
    equity_start = calculate_equity_value(portfolio_value, equity_ratio)
    insurance_budget = calculate_insurance_budget(portfolio_value, insurance_ratio)
    contracts = calculate_number_of_contracts(insurance_budget, option_price)
    price_change = calculate_price_change(price_at_start, price_at_end)
    equity_end = equity_start * (1 + price_change)
    option_payoff = calculate_option_payoff(strike_price, price_at_end)
    portfolio_end_with_insurance = equity_end + (option_payoff * contracts * 100)
    portfolio_end_without_insurance = portfolio_value * (1 + price_change)
    portfolio_change_with_insurance = (portfolio_end_with_insurance - portfolio_value) / portfolio_value
    portfolio_change_without_insurance = (portfolio_end_without_insurance - portfolio_value) / portfolio_value
    scenario = "stable" if price_at_end >= strike_price else "crash"
    option_strategy = f"buy {contracts} put contracts at {strike_price} strike price to expire on {expiry_date}"
    return {
        "scenario": scenario,
        "price_value_at_start": round(price_at_start, 2),
        "price_value_at_end": round(price_at_end, 2),
        "price_value_percent_change": round(price_change, 2),
        "equity_at_start": round(equity_start, 2),
        "equity_at_end": round(equity_end, 2),
        "insurance_strategy_cost": round(insurance_budget, 2),
        "insurance_strategy_cost_as_percentage_of_portfolio": insurance_ratio,
        "number_of_contracts": contracts,
        "put_option_price": round(option_price, 2),
        "option_strategy": option_strategy,
        "portfolio_value_at_start": portfolio_value,
        "portfolio_value_at_end_with_insurance": round(portfolio_end_with_insurance, 2),
        "portfolio_value_at_end_without_insurance": round(portfolio_end_without_insurance, 2),
        "portfolio_value_percent_change_with_insurance": round(portfolio_change_with_insurance, 2),
        "portfolio_value_percent_change_without_insurance": round(portfolio_change_without_insurance, 2),
        "portfolio_profit_loss_with_insurance": round(portfolio_end_with_insurance - portfolio_value, 2),
        "portfolio_profit_loss_without_insurance": round(portfolio_end_without_insurance - portfolio_value, 2),
        "difference_between_portfolio_profit_with_insurance_and_without_insurance": round(
            portfolio_end_with_insurance - portfolio_end_without_insurance, 2
        ),
    }