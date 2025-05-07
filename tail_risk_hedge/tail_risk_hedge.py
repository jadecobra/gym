import datetime
import numpy
import os
import pandas
import pickle
import random
import time
import yfinance

class YahooFinanceDataProvider:
    def __init__(self, *, ticker="SPY", seed=None, cache_file="price_cache.pkl", put_options_cache_file="put_options_cache.pkl", vix_cache_file="vix_cache.pkl", cache_duration=86400):
        if seed is not None:
            random.seed(seed)
        self.ticker = ticker
        self.ticker_data = yfinance.Ticker(ticker)
        self.cache_file = cache_file
        self.put_options_cache_file = put_options_cache_file
        self.vix_cache_file = vix_cache_file
        self.cache_duration = cache_duration
        self.risk_free_rate = 0.04
        self.time_to_expiry = 2 / 12
        self.historical_data = self._load_historical_data()
        self.put_options_cache = self._load_put_options_cache()
        self.vix_cache = self._load_vix_cache()

    def _load_cached_data(self, cache_file, fetch_function=None, default_value=None):
        """
        Generic method to load data from cache if valid, otherwise fetch new data.

        Args:
            cache_file: Path to the cache file
            fetch_function: Function to call if cache is invalid (optional)
            default_value: Value to return if fetch_function is None and cache is invalid

        Returns:
            Cached data or newly fetched data or default value
        """
        if self._is_cache_valid(cache_file):
            try:
                with open(cache_file, "rb") as f:
                    return pickle.load(f)
            except (FileNotFoundError, pickle.PickleError):
                pass

        if fetch_function is not None:
            data = fetch_function()
            self._save_cache(data, cache_file)
            return data

        return default_value

    def _load_historical_data(self):
        data = self._load_cached_data(
            self.cache_file,
            fetch_function=self._fetch_historical_data
        )
        if data is None or data.empty:
            raise ValueError("No historical data available")
        return data

    def _load_put_options_cache(self):
        return self._load_cached_data(self.put_options_cache_file)

    def _load_vix_cache(self):
        return self._load_cached_data(self.vix_cache_file)

    def _is_cache_valid(self, cache_file):
        if not os.path.exists(cache_file):
            return False
        cache_age = time.time() - os.path.getmtime(cache_file)
        return cache_age < self.cache_duration

    def _fetch_historical_data(self):
        retries = 3
        for attempt in range(retries):
            try:
                data = self.ticker_data.history(period="1y", interval="1d")
                if data.empty:
                    raise ValueError("No historical data retrieved")
                return data[["Open", "High", "Low", "Close"]].reset_index()
            except yfinance.YFRateLimitError:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                else:
                    raise

    def _save_cache(self, data, cache_file):
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(data, f)
        except OSError as e:
            print(f"Warning: Failed to save cache to {cache_file}: {e}")

    def _get_vix_volatility(self, scenario="stable"):
        if self.vix_cache is not None:
            volatility = self.vix_cache
            return volatility if scenario != "crash" else volatility * 1.5

        try:
            vix_data = yfinance.Ticker("^VIX").history(period="1d")
            if not vix_data.empty:
                volatility = vix_data["Close"].iloc[-1] / 100
                self.vix_cache = volatility
                self._save_cache(volatility, self.vix_cache_file)
                return volatility if scenario != "crash" else volatility * 1.5
        except Exception as e:
            print(f"Warning: Failed to fetch VIX: {e}")
        return 0.2 if scenario != "crash" else 0.3

    def _calculate_historical_volatility(self, lookback=60):
        if len(self.historical_data) < lookback:
            raise ValueError("Insufficient historical data for volatility calculation")
        closes = self.historical_data["Close"].tail(lookback)
        log_returns = numpy.log(closes / closes.shift(1)).dropna()
        return numpy.std(log_returns) * numpy.sqrt(252)

    def _estimate_implied_volatility(self, *, option_price, price_at_start, strike_price, time_to_expiry, risk_free_rate, scenario="stable"):
        volatility = self._get_vix_volatility(scenario)
        if volatility > 0:
            return volatility
        try:
            return self._calculate_historical_volatility()
        except ValueError:
            return 0.2 if scenario != "crash" else 0.3

    def get_date_difference(self, date1, date2):
        return abs((date1 - date2).days)

    def get_closest_expiration_date(self, expiration_dates, target_date):
        closest_date = datetime.datetime.strptime(expiration_dates[0], "%Y-%m-%d").date()
        min_diff = self.get_date_difference(closest_date, target_date)
        for date in expiration_dates:
            exp_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            diff = self.get_date_difference(exp_date, target_date)
            if diff < min_diff:
                min_diff = diff
                closest_date = exp_date
        if not closest_date:
            raise ValueError("No suitable option expiration found")
        return pandas.Timestamp(closest_date).strftime("%Y-%m-%d")

    def _fetch_option_chain(self, price_at_start):
        if self._is_cache_valid(self.put_options_cache_file) and self.put_options_cache:
            cached_puts, cached_expiry, cached_price_range = self.put_options_cache
            if price_at_start * 0.7 <= cached_price_range[1] and price_at_start * 0.9 >= cached_price_range[0]:
                return cached_puts, cached_expiry

        target_date = (datetime.datetime.now() + datetime.timedelta(days=60)).date()
        expiry_date = self.get_closest_expiration_date(self.ticker_data.options, target_date)
        try:
            option_chain = self.ticker_data.option_chain(expiry_date)
            puts = option_chain.puts
            out_of_the_money_puts = puts[
                (puts["strike"] <= price_at_start * 0.9) & (puts["strike"] >= price_at_start * 0.7)
            ]
        except Exception as e:
            print(f"Warning: Failed to fetch option chain: {e}")
            out_of_the_money_puts = None
            expiry_date = (datetime.datetime.now() + datetime.timedelta(days=60)).strftime("%Y-%m-%d")

        price_range = (price_at_start * 0.7, price_at_start * 0.9)
        self.put_options_cache = (out_of_the_money_puts, expiry_date, price_range)
        self._save_cache(self.put_options_cache, self.put_options_cache_file)
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