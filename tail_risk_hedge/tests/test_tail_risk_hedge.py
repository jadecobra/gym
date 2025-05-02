import os
import random
import re
import tail_risk_hedge
import time
import unittest
import pandas as pd

class TestTailRiskHedge(unittest.TestCase):
    def setUp(self):
        self.portfolio_value = random.uniform(10000, 1000000)
        self.insurance_ratio = random.uniform(0.01, 0.05)
        self.cache_file = "test_price_cache.pkl"
        self.put_options_cache_file = "test_put_options_cache.pkl"
        self.data_provider = tail_risk_hedge.YahooFinanceDataProvider(
            seed=42, cache_file=self.cache_file, put_options_cache_file=self.put_options_cache_file
        )

    def tearDown(self):
        for cache_file in [self.cache_file, self.put_options_cache_file]:
            if os.path.exists(cache_file):
                os.remove(cache_file)

    def test_cache_usage(self):
        data = self.data_provider._fetch_historical_data()
        self.data_provider._save_cache(data, self.cache_file)
        os.utime(self.cache_file, (time.time(), time.time()))
        self.assertTrue(
            self.data_provider._load_data().equals(data), "Cache not used correctly"
        )

    def test_cache_refresh(self):
        data = self.data_provider._fetch_historical_data()
        self.data_provider._save_cache(data, self.cache_file)
        os.utime(
            self.cache_file,
            (
                time.time() - 2 * self.data_provider.cache_duration,
                time.time() - 2 * self.data_provider.cache_duration
            )
        )
        self.data_provider._load_data()
        self.assertTrue(os.path.exists(self.cache_file), "New cache not created")
        cache_mtime = os.path.getmtime(self.cache_file)
        self.assertTrue(time.time() - cache_mtime < 60, "Cache not refreshed")

    def test_put_options_cache_usage(self):
        price_at_start = self.data_provider.historical_data['Close'].iloc[-1]
        puts, expiry = self.data_provider._fetch_option_chain(price_at_start)
        self.data_provider._save_cache(
            (puts, expiry, (price_at_start * 0.7, price_at_start * 0.9)),
            self.put_options_cache_file
        )
        os.utime(self.put_options_cache_file, (time.time(), time.time()))
        cached_puts, cached_expiry = self.data_provider._fetch_option_chain(price_at_start)
        if puts is not None:
            self.assertTrue(cached_puts.equals(puts), "Put options cache not used correctly")
            self.assertEqual(cached_expiry, expiry, "Put options expiry cache not used correctly")
        else:
            self.assertIsNone(cached_puts)
            self.assertEqual(cached_expiry, expiry)

    def test_put_options_cache_refresh(self):
        price_at_start = self.data_provider.historical_data['Close'].iloc[-1]
        puts, expiry = self.data_provider._fetch_option_chain(price_at_start)
        self.data_provider._save_cache(
            (puts, expiry, (price_at_start * 0.7, price_at_start * 0.9)),
            self.put_options_cache_file
        )
        os.utime(
            self.put_options_cache_file,
            (
                time.time() - 2 * self.data_provider.cache_duration,
                time.time() - 2 * self.data_provider.cache_duration
            )
        )
        # Fetch again to trigger refresh
        self.data_provider._fetch_option_chain(price_at_start)
        self.assertTrue(os.path.exists(self.put_options_cache_file), "New put options cache not created")
        cache_mtime = os.path.getmtime(self.put_options_cache_file)
        self.assertTrue(time.time() - cache_mtime < 60, "Put options cache not refreshed")

    def test_implied_volatility(self):
        self.assertTrue(0.1 <= self.data_provider._estimate_implied_volatility(lookback=60) <= 0.5)

    def test_implied_volatility_with_historical_data(self):
        self.data_provider.historical_data = self.data_provider.historical_data.iloc[:10]
        self.assertEqual(self.data_provider._estimate_implied_volatility(lookback=60), 0.2)

    def test_fetch_option_chain(self):
        price_at_start = self.data_provider.historical_data['Close'].iloc[-1]
        out_of_the_money_puts, put_expiration_date = self.data_provider._fetch_option_chain(price_at_start)
        if out_of_the_money_puts is not None:
            self.assertFalse(out_of_the_money_puts.empty)
            self.assertTrue((out_of_the_money_puts['strike'] <= price_at_start * 0.9).all())
            self.assertTrue((out_of_the_money_puts['strike'] >= price_at_start * 0.7).all())
            self.assertTrue((out_of_the_money_puts['lastPrice'] >= 0).all())
            self.assertTrue(bool(re.match(r'\d{4}-\d{2}-\d{2}', put_expiration_date)))
        else:
            self.assertIsNone(out_of_the_money_puts)
            self.assertIsNone(put_expiration_date)

    def test_option_strategy_format(self):
        data = self.data_provider.generate_scenario("stable")
        metrics = tail_risk_hedge.calculate_portfolio_metrics(
            portfolio_value=self.portfolio_value,
            insurance_ratio=self.insurance_ratio,
            **data
        )
        self.assertEqual(
            metrics["option_strategy"],
            f'buy {metrics["number_of_contracts"]} put contracts at {data["strike_price"]} strike price to expire on {data["expiry_date"]}'
        )

    def test_calculate_equity_value(self):
        equity = tail_risk_hedge.calculate_equity_value(self.portfolio_value, 0.99)
        self.assertAlmostEqual(equity, self.portfolio_value * 0.99)
        self.assertEqual(tail_risk_hedge.calculate_equity_value(0, 0.99), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_equity_value(-100, 0.99)

    def test_calculate_insurance_budget(self):
        budget = tail_risk_hedge.calculate_insurance_budget(self.portfolio_value, self.insurance_ratio)
        self.assertAlmostEqual(budget, self.portfolio_value * self.insurance_ratio)
        self.assertEqual(tail_risk_hedge.calculate_insurance_budget(0, self.insurance_ratio), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_insurance_budget(self.portfolio_value, -0.01)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_insurance_budget(-100000, self.insurance_ratio)

    def test_calculate_number_of_contracts_to_purchase(self):
        hedge_budget = self.portfolio_value * self.insurance_ratio
        option_price = random.uniform(0.5, 5)
        number_contracts_to_purchase = tail_risk_hedge.calculate_number_of_contracts_to_purchase(hedge_budget, option_price)
        self.assertEqual(number_contracts_to_purchase, int(hedge_budget / (option_price * 100)))
        self.assertEqual(
            tail_risk_hedge.calculate_number_of_contracts_to_purchase(0, option_price), 0
        )
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_number_of_contracts_to_purchase(hedge_budget, 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_number_of_contracts_to_purchase(-1000, option_price)

    def test_calculate_option_payoff_stable(self):
        data = self.data_provider.generate_scenario("stable")
        payoff = tail_risk_hedge.calculate_option_payoff(
            data["strike_price"], data["price_at_end"], data["option_value_end"]
        )
        self.assertEqual(payoff, 0)

    def test_calculate_option_payoff_crash(self):
        data = self.data_provider.generate_scenario("crash")
        payoff = tail_risk_hedge.calculate_option_payoff(
            data["strike_price"], data["price_at_end"], data["option_value_end"]
        )
        self.assertEqual(payoff, data["option_value_end"])
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_option_payoff(
                data["strike_price"],
                -350,
                data["option_value_end"]
            )

    def test_calculate_price_value_change_stable(self):
        data = self.data_provider.generate_scenario("stable")
        self.assertAlmostEqual(
            tail_risk_hedge.calculate_price_value_change(data["price_at_start"], data["price_at_end"]),
            (data["price_at_end"] - data["price_at_start"]) / data["price_at_start"]
        )

    def test_calculate_price_value_change_crash(self):
        data = self.data_provider.generate_scenario("crash")
        self.assertAlmostEqual(
            tail_risk_hedge.calculate_price_value_change(data["price_at_start"], data["price_at_end"]),
            (data["price_at_end"] - data["price_at_start"]) / data["price_at_start"]
        )
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_price_value_change(data["price_at_start"], 0)

    def test_calculate_portfolio_metrics(self):
        scenario = random.choice(('stable', 'crash'))
        data = self.data_provider.generate_scenario(scenario)
        metrics = tail_risk_hedge.calculate_portfolio_metrics(
            portfolio_value=self.portfolio_value,
            insurance_ratio=self.insurance_ratio,
            **data
        )
        price_change = (data["price_at_end"] - data["price_at_start"]) / data["price_at_start"]
        equity_start = self.portfolio_value * (1 - self.insurance_ratio)
        equity_end = equity_start * (1 + price_change)
        insurance_budget = self.portfolio_value * self.insurance_ratio
        option_payoff = tail_risk_hedge.calculate_option_payoff(
            data['strike_price'], data['price_at_end'], data['option_value_end'])
        contracts = tail_risk_hedge.calculate_number_of_contracts_to_purchase(
            insurance_budget, data['option_price']
        )
        self.assertEqual(metrics["scenario"], scenario)
        self.assertAlmostEqual(
            metrics["price_value_percent_change"], round(price_change, 2)
        )
        self.assertAlmostEqual(metrics["equity_at_start"], round(equity_start, 2))
        self.assertAlmostEqual(metrics["insurance_strategy_cost"], round(insurance_budget, 2))
        self.assertAlmostEqual(metrics["put_option_price"], round(data["option_price"], 2))
        self.assertAlmostEqual(
            metrics["portfolio_value_at_end_with_insurance"],
            round(equity_end + (option_payoff * contracts * 100), 2)
        )
        self.assertEqual(
            metrics["number_of_contracts"],
            int(insurance_budget / (data["option_price"] * 100))
        )
        self.assertAlmostEqual(
            metrics["portfolio_value_at_end_without_insurance"],
            round(self.portfolio_value * (1 + price_change), 2)
        )

    def test_calculate_portfolio_metrics_invalid_inputs(self):
        data = self.data_provider.generate_scenario("stable")
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_portfolio_metrics(
                portfolio_value=-self.portfolio_value,
                insurance_ratio=self.insurance_ratio,
                **data
            )
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_portfolio_metrics(
                portfolio_value=self.portfolio_value,
                insurance_ratio=-self.insurance_ratio,
                **data
            )

if __name__ == "__main__":
    unittest.main()