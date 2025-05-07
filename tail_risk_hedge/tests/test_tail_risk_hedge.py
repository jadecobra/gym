import unittest
import unittest.mock
import yfinance
import tail_risk_hedge
import os
import time
import re
import pandas


class TestYahooFinanceDataProvider(unittest.TestCase):
    def setUp(self):
        self.cache_file = "test_cache.pkl"
        self.put_options_cache_file = "test_put_options_cache.pkl"
        self.vix_cache_file = "test_vix_cache.pkl"
        self.data_provider = tail_risk_hedge.YahooFinanceDataProvider(
            cache_file=self.cache_file,
            put_options_cache_file=self.put_options_cache_file,
            vix_cache_file=self.vix_cache_file,
            seed=42
        )

    def tearDown(self):
        for cache_file in [self.cache_file, self.put_options_cache_file, self.vix_cache_file]:
            if os.path.exists(cache_file):
                os.remove(cache_file)

    @unittest.mock.patch('yfinance.Ticker')
    def test_backoff_retries(self, mock_ticker):
        mock_ticker.side_effect = [yfinance.exceptions.YFRateLimitError("Rate limited"), {"Close": [100]}]
        start_time = time.time()
        data = self.data_provider._fetch_historical_data()
        self.assertGreaterEqual(time.time() - start_time, 1)  # Ensure delay
        self.assertIsNotNone(data)

    @unittest.mock.patch('yfinance.Ticker')
    def test_cache_reduces_api_calls(self, mock_ticker):
        self.data_provider._fetch_historical_data()
        self.data_provider._load_historical_data()
        mock_ticker.assert_not_called()  # Ensure cache is used

    @unittest.mock.patch('yfinance.Ticker')
    def test_fetch_vix_data_empty(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pandas.DataFrame()
        result = self.data_provider._fetch_vix_data()
        self.assertIsNone(result)

    @unittest.mock.patch('yfinance.Ticker')
    def test_fetch_option_chain_empty_options(self, mock_ticker):
        mock_ticker.return_value.options = []
        with self.assertRaises(ValueError, msg="No options data available for ticker"):
            self.data_provider._fetch_option_chain(100)

    @unittest.mock.patch('yfinance.Ticker')
    def test_backoff_retries_fallback_to_cache(self, mock_ticker):
        # Simulate persistent rate limit error
        mock_ticker.side_effect = yfinance.exceptions.YFRateLimitError("Rate limited")
        # Create a valid legacy cache file (no version field)
        mock_data = pandas.DataFrame({"Open": [100], "High": [101], "Low": [99], "Close": [100]})
        with open(self.cache_file, "wb") as f:
            pickle.dump(mock_data, f)
        os.utime(self.cache_file, (time.time(), time.time()))
        # Call fetch method, should fallback to cache
        with unittest.mock.patch('tail_risk_hedge.logger.info') as mock_log:
            data = self.data_provider._fetch_historical_data()
            mock_log.assert_called_with("Using cached historical data due to persistent rate limit error")
        self.assertTrue(data.equals(mock_data))
        # Test invalid legacy cache (empty DataFrame)
        with open(self.cache_file, "wb") as f:
            pickle.dump(pandas.DataFrame(), f)
        os.utime(self.cache_file, (time.time(), time.time()))
        with unittest.mock.patch('tail_risk_hedge.logger.warning') as mock_log:
            data = self.data_provider._fetch_historical_data()
            mock_log.assert_any_call("No valid cached historical data available, using fallback")
        self.assertFalse(data.empty)
        self.assertEqual(len(data), 252)  # Synthetic data length

    def test_load_legacy_cache(self):
        # Create a legacy cache file (no version field)
        mock_data = pandas.DataFrame({"Open": [100], "High": [101], "Low": [99], "Close": [100]})
        with open(self.cache_file, "wb") as f:
            pickle.dump(mock_data, f)
        os.utime(self.cache_file, (time.time(), time.time()))
        # Load legacy cache
        loaded_data = self.data_provider._load_cached_data('historical')
        self.assertTrue(loaded_data.equals(mock_data))
        # Create a legacy VIX cache
        vix_data = 0.2
        with open(self.vix_cache_file, "wb") as f:
            pickle.dump(vix_data, f)
        os.utime(self.vix_cache_file, (time.time(), time.time()))
        loaded_vix = self.data_provider._load_cached_data('vix')
        self.assertEqual(loaded_vix, vix_data)
        # Test invalid legacy cache (empty historical data)
        with open(self.cache_file, "wb") as f:
            pickle.dump(pandas.DataFrame(), f)
        with unittest.mock.patch('tail_risk_hedge.logger.error') as mock_log:
            result = self.data_provider._load_cached_data('historical', default_value=None)
            mock_log.assert_called_with(f"Failed to load cache from {self.cache_file}: No historical data available")
            self.assertIsNone(result)

class TestTailRiskHedge(unittest.TestCase):
    def setUp(self):
        self.portfolio_value = 100000
        self.insurance_ratio = 0.01
        self.cache_file = "test_price_cache.pkl"
        self.put_options_cache_file = "test_put_options_cache.pkl"
        self.vix_cache_file = "test_vix_cache.pkl"
        self.data_provider = tail_risk_hedge.YahooFinanceDataProvider(
            cache_file=self.cache_file,
            put_options_cache_file=self.put_options_cache_file,
            vix_cache_file=self.vix_cache_file,
            seed=42
        )

    def tearDown(self):
        for cache_file in [self.cache_file, self.put_options_cache_file, self.vix_cache_file]:
            if os.path.exists(cache_file):
                os.remove(cache_file)

    def test_calculate_equity_value(self):
        result = tail_risk_hedge.calculate_equity_value(100000, 0.99)
        self.assertEqual(result, 99000)
        self.assertEqual(tail_risk_hedge.calculate_equity_value(0, 0.99), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_equity_value(-100, 0.99)

    def test_calculate_insurance_budget(self):
        result = tail_risk_hedge.calculate_insurance_budget(100000, 0.01)
        self.assertEqual(result, 1000)
        self.assertEqual(tail_risk_hedge.calculate_insurance_budget(0, 0.01), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_insurance_budget(-100, 0.01)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_insurance_budget(100000, -0.01)

    def test_calculate_number_of_contracts(self):
        result = tail_risk_hedge.calculate_number_of_contracts(1000, 1)
        self.assertEqual(result, 10)
        self.assertEqual(tail_risk_hedge.calculate_number_of_contracts(0, 1), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_number_of_contracts(1000, 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_number_of_contracts(-100, 1)

    def test_calculate_option_payoff(self):
        result = tail_risk_hedge.calculate_option_payoff(400, 350)
        self.assertEqual(result, 50)
        self.assertEqual(tail_risk_hedge.calculate_option_payoff(400, 450), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_option_payoff(400, -10)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_option_payoff(-400, 350)

    def test_calculate_price_change(self):
        result = tail_risk_hedge.calculate_price_change(500, 525)
        self.assertEqual(result, 0.05)
        self.assertEqual(tail_risk_hedge.calculate_price_change(500, 500), 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_price_change(500, 0)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_price_change(500, -10)

    def test_get_vix_volatility(self):
        volatility = self.data_provider._get_vix_volatility(scenario="stable")
        self.assertGreaterEqual(volatility, 0)
        crash_vol = self.data_provider._get_vix_volatility(scenario="crash")
        self.assertGreater(crash_vol, volatility)

    def test_vix_cache_usage(self):
        volatility = self.data_provider._get_vix_volatility(scenario="stable")
        self.data_provider._save_cache(volatility, self.vix_cache_file)
        os.utime(self.vix_cache_file, (time.time(), time.time()))
        cached_vol = self.data_provider._load_cached_data('vix')
        self.assertEqual(cached_vol, volatility, "VIX cache not used correctly")

    def test_vix_cache_refresh(self):
        initial_vol = 0.2
        self.data_provider._save_cache(initial_vol, self.vix_cache_file)
        os.utime(
            self.vix_cache_file,
            (time.time() - 2 * self.data_provider.cache_duration, time.time() - 2 * self.data_provider.cache_duration)
        )
        new_vol = self.data_provider._get_vix_volatility(scenario="stable")
        self.assertTrue(os.path.exists(self.vix_cache_file), "VIX cache not created")
        self.assertLess(time.time() - os.path.getmtime(self.vix_cache_file), 60, "VIX cache not refreshed")
        cached_vol = self.data_provider._load_cached_data('vix')
        self.assertEqual(cached_vol, new_vol, "VIX cache not updated with new volatility")

    def test_calculate_historical_volatility(self):
        volatility = self.data_provider._calculate_historical_volatility(lookback=60)
        self.assertGreaterEqual(volatility, 0)
        with self.assertRaises(ValueError):
            self.data_provider._calculate_historical_volatility(lookback=len(self.data_provider.historical_data) + 1)

    def test_cache_usage(self):
        data = self.data_provider._fetch_historical_data()
        self.data_provider._save_cache(data, self.cache_file)
        os.utime(self.cache_file, (time.time(), time.time()))
        self.assertTrue(self.data_provider._load_historical_data().equals(data))

    def test_cache_refresh(self):
        data = self.data_provider._fetch_historical_data()
        self.data_provider._save_cache(data, self.cache_file)
        os.utime(self.cache_file, (time.time() - 2 * self.data_provider.cache_duration, time.time() - 2 * self.data_provider.cache_duration))
        self.data_provider._load_historical_data()
        self.assertTrue(os.path.exists(self.cache_file))
        self.assertLess(time.time() - os.path.getmtime(self.cache_file), 60)

    def test_fetch_option_chain(self):
        price = self.data_provider.historical_data["Close"].iloc[-1]
        puts, expiry = self.data_provider._fetch_option_chain(price)
        if puts is not None:
            self.assertFalse(puts.empty)
            self.assertTrue((puts["strike"] <= price * 0.9).all())
            self.assertTrue((puts["strike"] >= price * 0.7).all())
            self.assertTrue(bool(re.match(r"\d{4}-\d{2}-\d{2}", expiry)))

    def test_generate_scenario(self):
        scenario = self.data_provider.generate_scenario(scenario="stable")
        self.assertGreater(scenario["price_at_start"], 0)
        self.assertGreater(scenario["price_at_end"], 0)
        self.assertGreater(scenario["strike_price"], 0)
        self.assertGreater(scenario["option_price"], 0)
        self.assertTrue(bool(re.match(r"\d{4}-\d{2}-\d{2}", scenario["expiry_date"])))

    def test_calculate_portfolio_metrics(self):
        scenario = self.data_provider.generate_scenario(scenario="stable")
        metrics = tail_risk_hedge.calculate_portfolio_metrics(
            portfolio_value=self.portfolio_value,
            insurance_ratio=self.insurance_ratio,
            price_at_start=scenario["price_at_start"],
            price_at_end=scenario["price_at_end"],
            strike_price=scenario["strike_price"],
            option_price=scenario["option_price"],
            expiry_date=scenario["expiry_date"]
        )
        price_change = (scenario["price_at_end"] - scenario["price_at_start"]) / scenario["price_at_start"]
        equity_start = self.portfolio_value * (1 - self.insurance_ratio)
        equity_end = equity_start * (1 + price_change)
        insurance_budget = self.portfolio_value * self.insurance_ratio
        contracts = int(insurance_budget / (scenario["option_price"] * 100))
        option_payoff = max(0, scenario["strike_price"] - scenario["price_at_end"])
        self.assertAlmostEqual(metrics["equity_at_start"], equity_start, places=2)
        self.assertAlmostEqual(metrics["equity_at_end"], equity_end, places=2)
        self.assertAlmostEqual(metrics["portfolio_value_at_end_with_insurance"], equity_end + (option_payoff * contracts * 100), places=2)
        with self.assertRaises(ValueError):
            tail_risk_hedge.calculate_portfolio_metrics(portfolio_value=-100000, insurance_ratio=0.01, **scenario)

if __name__ == "__main__":
    unittest.main()