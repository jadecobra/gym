import os
import random
import re
import tail_risk_hedge
import time
import unittest

class TestTailRiskHedge(unittest.TestCase):

    def setUp(self):
        self.portfolio_value = random.uniform(10000, 1000000)
        self.hedge_ratio = random.uniform(0.01, 0.05)
        self.cache_file = "test_spy_cache.pkl"
        self.data_provider = tail_risk_hedge.YahooFinanceDataProvider(
            seed=42, cache_file=self.cache_file
        )

    def tearDown(self):
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

    def test_cache_usage(self):
        data = self.data_provider._fetch_historical_data()
        self.data_provider._save_cache(data)
        os.utime(self.cache_file, (time.time(), time.time()))
        self.assertTrue(
            self.data_provider._load_data().equals(data), "Cache not used correctly"
        )

    def test_cache_refresh(self):
        data = self.data_provider._fetch_historical_data()
        self.data_provider._save_cache(data)
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

    def test_implied_volatility(self):
        self.assertTrue(0.1 <= self.data_provider._estimate_implied_volatility(lookback=60) <= 0.5)

    def test_implied_volatility_with_historical_data(self):
        self.data_provider.historical_data = self.data_provider.historical_data.iloc[:10]
        self.assertEqual(self.data_provider._estimate_implied_volatility(lookback=60), 0.2)

    def test_fetch_option_chain(self):
        spy_start = self.data_provider.historical_data['Close'].iloc[-1]
        out_of_the_money_puts, put_expiration_date = self.data_provider._fetch_option_chain(spy_start)
        if out_of_the_money_puts is not None:
            self.assertFalse(out_of_the_money_puts.empty)
            self.assertTrue((out_of_the_money_puts['strike'] <= spy_start * 0.9).all())
            self.assertTrue((out_of_the_money_puts['strike'] >= spy_start * 0.7).all())
            self.assertTrue((out_of_the_money_puts['lastPrice'] >= 0).all())
            self.assertTrue(bool(re.match(r'\d{4}-\d{2}-\d{2}', put_expiration_date)))
        else:
            self.assertIsNone(out_of_the_money_puts)
            self.assertIsNone(put_expiration_date)


    def test_option_strategy_format(self):
        data = self.data_provider.generate_scenario("stable")
        metrics = tail_risk_hedge.calculate_portfolio_metrics(
            portfolio_value=self.portfolio_value,
            hedge_ratio=self.hedge_ratio,
            **data
        )
        strategy = metrics["option_strategy"]
        self.assertTrue(
            bool(re.match(r'buy \d+ put contracts at \d+(\.\d+)? strike price to expire on \d{4}-\d{2}-\d{2}', strategy)),
            f"Invalid option strategy format: {strategy}"
        )
        self.assertEqual(strategy.split()[1], str(metrics["number_of_contracts"]))
        self.assertEqual(
            strategy,
            f'buy {metrics["number_of_contracts"]} put contracts at {data["strike_price"]} strike price to expire on {data["expiry_date"]}'
        )

    def test_calculate_equity_value(self):
        equity = tail_risk_hedge.calculate_equity_value(self.portfolio_value, 0.99)
        self.assertAlmostEqual(equity, self.portfolio_value * 0.99)
        self.assertEqual(tail_risk_hedge.calculate_equity_value(0, 0.99), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_equity_value(-100, 0.99)

    def test_calculate_hedge_budget(self):
        budget = tail_risk_hedge.calculate_hedge_budget(self.portfolio_value, self.hedge_ratio)
        self.assertAlmostEqual(budget, self.portfolio_value * self.hedge_ratio)
        self.assertEqual(tail_risk_hedge.calculate_hedge_budget(0, self.hedge_ratio), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_hedge_budget(self.portfolio_value, -0.01)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_hedge_budget(-100000, self.hedge_ratio)

    def test_calculate_number_of_contracts_to_purchase(self):
        hedge_budget = self.portfolio_value * self.hedge_ratio
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
            data["strike_price"], data["spy_end"], data["option_value_end"]
        )
        self.assertEqual(payoff, 0)

    def test_calculate_option_payoff_crash(self):
        data = self.data_provider.generate_scenario("crash")
        payoff = tail_risk_hedge.calculate_option_payoff(
            data["strike_price"], data["spy_end"], data["option_value_end"]
        )
        self.assertEqual(payoff, data["option_value_end"])
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_option_payoff(
                data["strike_price"],
                -350,
                data["option_value_end"]
            )

    def test_calculate_spy_value_change_stable(self):
        data = self.data_provider.generate_scenario("stable")
        self.assertAlmostEqual(
            tail_risk_hedge.calculate_spy_value_change(data["spy_start"], data["spy_end"]),
            (data["spy_end"] - data["spy_start"]) / data["spy_start"]
        )

    def test_calculate_spy_value_change_crash(self):
        data = self.data_provider.generate_scenario("crash")
        self.assertAlmostEqual(
            tail_risk_hedge.calculate_spy_value_change(data["spy_start"], data["spy_end"]),
            (data["spy_end"] - data["spy_start"]) / data["spy_start"]
        )
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_spy_value_change(data["spy_start"], 0)

    def test_calculate_portfolio_metrics(self):
        scenario = random.choice(('stable', 'crash'))
        data = self.data_provider.generate_scenario(scenario)
        metrics = tail_risk_hedge.calculate_portfolio_metrics(
            portfolio_value=self.portfolio_value,
            hedge_ratio=self.hedge_ratio,
            **data
        )
        spy_change = (data["spy_end"] - data["spy_start"]) / data["spy_start"]
        equity_start = self.portfolio_value * (1 - self.hedge_ratio)
        equity_end = equity_start * (1 + spy_change)
        budget = self.portfolio_value * self.hedge_ratio

        self.assertEqual(metrics["scenario"], scenario)
        self.assertAlmostEqual(metrics["spy_value_percent_change"], spy_change)
        self.assertAlmostEqual(metrics["equity_at_start"], equity_start)
        self.assertAlmostEqual(metrics["hedge_strategy_cost"], budget)
        self.assertAlmostEqual(metrics["put_option_price"], data["option_price"])
        self.assertAlmostEqual(metrics["portfolio_value_at_end_with_hedge"], equity_end)
        self.assertEqual(
            metrics["number_of_contracts"],
            int(budget / (data["option_price"] * 100))
        )
        self.assertAlmostEqual(
            metrics["portfolio_value_at_end_without_hedge"],
            self.portfolio_value * (1 + spy_change)
        )

    def test_calculate_portfolio_metrics_invalid_inputs(self):
        data = self.data_provider.generate_scenario("stable")
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_portfolio_metrics(
                portfolio_value=-self.portfolio_value,
                hedge_ratio=self.hedge_ratio,
                **data
            )
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_portfolio_metrics(
                portfolio_value=self.portfolio_value,
                hedge_ratio=-self.hedge_ratio,
                **data
            )

if __name__ == "__main__":
    unittest.main()