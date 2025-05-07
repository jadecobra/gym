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
        self.cache_files = {
            'price': "test_price_cache.pkl",
            'put_options': "test_put_options_cache.pkl",
            'vix': "test_vix_cache.pkl"
        }
        self.data_provider = tail_risk_hedge.YahooFinanceDataProvider(
            cache_file=self.cache_files['price'],
            put_options_cache_file=self.cache_files['put_options'],
            vix_cache_file=self.cache_files['vix'],
            seed=42
        )
        self.key_metrics = [
            'portfolio_value_percent_change_with_insurance',
            'portfolio_value_percent_change_without_insurance',
            'difference_between_portfolio_profit_with_insurance_and_without_insurance'
        ]

    def tearDown(self):
        for cache_file in self.cache_files.values():
            if os.path.exists(cache_file):
                os.remove(cache_file)

    def _create_mock_comparison_data(self, iterations=2):
        data = []
        for ratio in self.insurance_ratios:
            for _ in range(iterations):
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
        return pandas.DataFrame(data)

    def test_run_comparison(self):
        result_df = main.run_comparison(
            self.data_provider,
            self.portfolio_value,
            self.insurance_ratios,
            "stable",
            iterations=2
        )
        self.assertEqual(len(result_df), 2 * len(self.insurance_ratios))
        expected_columns = [
            'scenario', 'price_value_at_start', 'price_value_at_end',
            'portfolio_value_at_start', 'portfolio_value_at_end_with_insurance',
            'portfolio_value_percent_change_with_insurance',
            'difference_between_portfolio_profit_with_insurance_and_without_insurance',
            'insurance_ratio'
        ]
        for col in expected_columns:
            self.assertIn(col, result_df.columns)
        self.assertCountEqual(result_df['insurance_ratio'].unique(), self.insurance_ratios)

    def test_run_comparison_crash_scenario(self):
        result_df = main.run_comparison(
            self.data_provider,
            self.portfolio_value,
            self.insurance_ratios,
            "crash",
            iterations=1
        )
        grouped = result_df.groupby('insurance_ratio')
        avg_protection = grouped['difference_between_portfolio_profit_with_insurance_and_without_insurance'].mean()
        min_ratio = min(self.insurance_ratios)
        max_ratio = max(self.insurance_ratios)
        self.assertGreaterEqual(avg_protection[max_ratio], avg_protection[min_ratio])

    @unittest.mock.patch('builtins.print')
    def test_print_comparison_results(self, mock_print):
        df = self._create_mock_comparison_data()
        main.ResultPrinter.print_comparison_results(df, self.key_metrics)
        mock_print.assert_called()

    def test_run_scenario(self):
        metrics = main.run_scenario(self.data_provider, self.portfolio_value, 0.01, "stable")
        expected_keys = [
            'scenario', 'price_value_at_start', 'price_value_at_end',
            'portfolio_value_at_start', 'portfolio_value_at_end_with_insurance'
        ]
        for key in expected_keys:
            self.assertIn(key, metrics)
        self.assertEqual(metrics['portfolio_value_at_start'], self.portfolio_value)

if __name__ == "__main__":
    unittest.main()