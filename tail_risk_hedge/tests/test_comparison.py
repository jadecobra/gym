import unittest
import unittest.mock
import pandas
import os


import main
import tail_risk_hedge

class TestComparisonMode(unittest.TestCase):
    def setUp(self):
        self.portfolio_value = 100000
        self.insurance_ratios = [0.01, 0.02, 0.03]
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

    def test_run_comparison(self):
        # Test that the comparison function returns a DataFrame with expected shape and columns
        result_df = main.run_comparison(
            self.data_provider,
            self.portfolio_value,
            self.insurance_ratios,
            "stable",
            iterations=2
        )

        # Check that we have the expected number of rows (iterations * ratios)
        self.assertEqual(len(result_df), 2 * len(self.insurance_ratios))

        # Check that the DataFrame contains all expected columns
        expected_columns = [
            'scenario', 'price_value_at_start', 'price_value_at_end',
            'portfolio_value_at_start', 'portfolio_value_at_end_with_insurance',
            'portfolio_value_percent_change_with_insurance',
            'difference_between_portfolio_profit_with_insurance_and_without_insurance',
            'insurance_ratio'
        ]
        for col in expected_columns:
            self.assertIn(col, result_df.columns)

        # Check that insurance ratios in results match input ratios
        self.assertCountEqual(result_df['insurance_ratio'].unique(), self.insurance_ratios)

    def test_run_comparison_crash_scenario(self):
        # Test that the crash scenario produces expected results
        result_df = main.run_comparison(
            self.data_provider,
            self.portfolio_value,
            self.insurance_ratios,
            "crash",
            iterations=1
        )

        # In crash scenarios, higher insurance ratios should generally provide better protection
        grouped = result_df.groupby('insurance_ratio')
        avg_protection = grouped['difference_between_portfolio_profit_with_insurance_and_without_insurance'].mean()

        # Check if protection increases with higher insurance ratio (not always true but generally expected)
        # This is a soft check - we use assertGreaterEqual with the lowest and highest ratio only
        min_ratio = min(self.insurance_ratios)
        max_ratio = max(self.insurance_ratios)
        self.assertGreaterEqual(avg_protection[max_ratio], avg_protection[min_ratio])

    @unittest.mock.patch('builtins.print')  # Mock print to avoid cluttering test output
    def test_print_comparison_results(self, mock_print):
        # Create a mock DataFrame with comparison results
        data = []
        for ratio in self.insurance_ratios:
            for _ in range(2):  # 2 iterations
                data.append({
                    'insurance_ratio': ratio,
                    'scenario': 'stable',
                    'portfolio_value_percent_change_with_insurance': 0.05,
                    'portfolio_value_percent_change_without_insurance': 0.04,
                    'difference_between_portfolio_profit_with_insurance_and_without_insurance': 1000
                })
                data.append({
                    'insurance_ratio': ratio,
                    'scenario': 'crash',
                    'portfolio_value_percent_change_with_insurance': -0.1,
                    'portfolio_value_percent_change_without_insurance': -0.2,
                    'difference_between_portfolio_profit_with_insurance_and_without_insurance': 10000
                })

        df = pandas.DataFrame(data)
        key_metrics = [
            'portfolio_value_percent_change_with_insurance',
            'portfolio_value_percent_change_without_insurance',
            'difference_between_portfolio_profit_with_insurance_and_without_insurance'
        ]

        # Test that the function runs without errors
        main.print_comparison_results(df, key_metrics)

        # Verify print was called at least once
        mock_print.assert_called()

    def test_run_scenario(self):
        # Test that run_scenario returns the expected metrics
        metrics = main.run_scenario(self.data_provider, self.portfolio_value, 0.01, "stable")

        # Check that the metrics contain all expected keys
        expected_keys = [
            'scenario', 'price_value_at_start', 'price_value_at_end',
            'portfolio_value_at_start', 'portfolio_value_at_end_with_insurance'
        ]
        for key in expected_keys:
            self.assertIn(key, metrics)

        # Check that the portfolio value matches the input
        self.assertEqual(metrics['portfolio_value_at_start'], self.portfolio_value)

if __name__ == "__main__":
    unittest.main()