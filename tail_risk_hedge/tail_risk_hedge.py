import yfinance as yf
import pandas as pd
import random
import math
import os
import pickle
import time
import numpy as np
from datetime import datetime, timedelta

class YahooFinanceDataProvider:
    def __init__(self, ticker="SPY", seed=None, cache_file="spy_cache.pkl", cache_duration=86400):
        if seed is not None:
            random.seed(seed)
        self.ticker = ticker
        self.spy = yf.Ticker(ticker)
        self.cache_file = cache_file
        self.cache_duration = cache_duration
        self.historical_data = self._load_data()
        self.risk_free_rate = 0.04
        self.time_to_expiry = 2 / 12

    def _load_data(self):
        if self._is_cache_valid():
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except (FileNotFoundError, pickle.PickleError):
                pass
        data = self._fetch_historical_data()
        self._save_cache(data)
        return data

    def _is_cache_valid(self):
        if not os.path.exists(self.cache_file):
            return False
        cache_age = time.time() - os.path.getmtime(self.cache_file)
        return cache_age < self.cache_duration

    def _fetch_historical_data(self):
        data = self.spy.history(period="1y", interval="1d")
        if data.empty:
            raise ValueError("No historical data retrieved from Yahoo Finance")
        return data[['Open', 'High', 'Low', 'Close']].reset_index()

    def _save_cache(self, data):
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(data, f)
        except OSError as e:
            print(f"Warning: Failed to save cache: {e}")

    def _estimate_implied_volatility(self, lookback=60):
        if len(self.historical_data) < lookback:
            return 0.2
        closes = self.historical_data['Close'].tail(lookback)
        log_returns = np.log(closes / closes.shift(1)).dropna()
        volatility = np.std(log_returns) * np.sqrt(252)
        return max(0.1, min(0.5, volatility))

    def _fetch_option_chain(self, spy_start):
        try:
            expirations = self.spy.options
            target_date = datetime.now() + timedelta(days=60)
            target_date = target_date.date()

            closest_expiry = None
            min_diff = float('inf')
            for exp in expirations:
                exp_date = datetime.strptime(exp, '%Y-%m-%d').date()
                diff = abs((exp_date - target_date).days)
                if diff < min_diff:
                    min_diff = diff
                    closest_expiry = exp

            if not closest_expiry:
                raise ValueError("No suitable option expiration found")

            opt_chain = self.spy.option_chain(closest_expiry)
            puts = opt_chain.puts
            otm_puts = puts[
                (puts['strike'] <= spy_start * 0.9) &
                (puts['strike'] >= spy_start * 0.7)
            ]

            if otm_puts.empty:
                raise ValueError("No OTM put options available")

            return otm_puts, closest_expiry
        except Exception as e:
            print(f"Warning: Failed to fetch option chain: {e}")
            return None, None

    def generate_scenario(self, scenario_type="stable"):
        if self.historical_data.empty:
            raise ValueError("No historical data available")

        max_idx = len(self.historical_data) - 40
        if max_idx < 0:
            raise ValueError("Insufficient historical data")
        start_idx = random.randint(0, max_idx)
        spy_start = self.historical_data.loc[start_idx, 'Close']

        otm_puts, expiry_date = self._fetch_option_chain(spy_start)

        if otm_puts is None or otm_puts.empty:
            volatility = self._estimate_implied_volatility()
            if scenario_type == "crash":
                volatility *= 1.5
            strike_price = spy_start * random.uniform(0.7, 0.9)
            option_price = max(0.5, min(10, volatility * spy_start * 0.01))
            expiry_date = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
        else:
            put = otm_puts.sample(n=1).iloc[0]
            strike_price = put['strike']
            option_price = put['lastPrice']
            if option_price <= 0:
                option_price = put.get('bid', 0.5) or 0.5

        if scenario_type == "stable":
            end_idx = random.randint(start_idx + 1, start_idx + 40)
            spy_end = self.historical_data.loc[end_idx, 'Close']
            if spy_end > spy_start * 1.2 or spy_end < spy_start * 0.9:
                spy_end = spy_start * random.uniform(0.95, 1.1)
        else:
            end_idx = random.randint(start_idx + 1, start_idx + 40)
            spy_end = self.historical_data.loc[end_idx, 'Close']
            if spy_end > spy_start * 0.9:
                spy_end = spy_start * random.uniform(0.6, 0.9)

        option_value_end = 0 if scenario_type == "stable" else max(0, strike_price - spy_end)

        return {
            "spy_start": spy_start,
            "spy_end": spy_end,
            "strike_price": strike_price,
            "option_price": option_price,
            "option_value_end": option_value_end,
            "expiry_date": expiry_date
        }

def calculate_equity_value(portfolio_value, equity_ratio):
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    return portfolio_value * equity_ratio

def calculate_hedge_budget(portfolio_value, hedge_ratio):
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    if hedge_ratio < 0:
        raise ValueError("Hedge ratio cannot be negative")
    return portfolio_value * hedge_ratio

def calculate_contracts(hedge_budget, option_price):
    if option_price <= 0:
        raise ValueError("Option price must be positive")
    if hedge_budget < 0:
        raise ValueError("Hedge budget cannot be negative")
    return int(hedge_budget / (option_price * 100))

def calculate_option_payoff(strike_price, spy_end, option_value_end):
    if spy_end < 0:
        raise ValueError("SPY end price cannot be negative")
    return max(0, option_value_end)

def calculate_spy_value_change(spy_start, spy_end):
    if spy_end <= 0:
        raise ValueError("SPY end price must be positive")
    return (spy_end - spy_start) / spy_start

def calculate_portfolio_metrics(*, portfolio_value, hedge_ratio, spy_start, spy_end, strike_price, option_value_end, option_price, expiry_date):
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    if hedge_ratio < 0:
        raise ValueError("Hedge ratio cannot be negative")

    equity_ratio = 1 - hedge_ratio
    equity_start = calculate_equity_value(portfolio_value, equity_ratio)
    hedge_budget = calculate_hedge_budget(portfolio_value, hedge_ratio)
    contracts = calculate_contracts(hedge_budget, option_price)
    spy_change = calculate_spy_value_change(spy_start, spy_end)
    equity_end = equity_start * (1 + spy_change)
    option_payoff = calculate_option_payoff(strike_price, spy_end, option_value_end)
    portfolio_end_with_hedge = equity_end + option_payoff * contracts * 100
    portfolio_end_without_hedge = portfolio_value * (1 + spy_change)
    portfolio_change_with_hedge = (portfolio_end_with_hedge - portfolio_value) / portfolio_value
    portfolio_change_without_hedge = (portfolio_end_without_hedge - portfolio_value) / portfolio_value

    scenario = "stable" if spy_end >= strike_price else "crash"
    option_strategy = f"buy {contracts} put contracts at {strike_price} strike price to expire on {expiry_date}"

    return {
        "scenario": scenario,
        "spy_value_at_start": spy_start,
        "spy_value_at_end": spy_end,
        "spy_value_percent_change": spy_change,
        "equity_at_start": equity_start,
        "equity_at_end": equity_end,
        "hedge_strategy_cost": hedge_budget,
        "hedge_strategy_cost_as_percentage_of_portfolio": hedge_ratio,
        "number_of_contracts": contracts,
        "put_option_price": option_price,
        "option_strategy": option_strategy,
        "portfolio_value_at_start": portfolio_value,
        "portfolio_value_at_end_with_hedge": portfolio_end_with_hedge,
        "portfolio_value_at_end_without_hedge": portfolio_end_without_hedge,
        "portfolio_value_percent_change_with_hedge": portfolio_change_with_hedge,
        "portfolio_value_percent_change_without_hedge": portfolio_change_without_hedge,
        "portfolio_profit_loss_with_hedge": portfolio_end_with_hedge - portfolio_value,
        "portfolio_profit_loss_without_hedge": portfolio_end_without_hedge - portfolio_value,
        "difference_between_portfolio_profit_with_hedge_and_without_hedge": (
            portfolio_end_with_hedge - portfolio_end_without_hedge
        ),
    }