import unittest
import argparse
import main

class TestMain(unittest.TestCase):
    def _create_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--portfolio", type=float, default=100000)
        parser.add_argument("--ratio", type=float, default=0.01)
        parser.add_argument("--min-ratio", type=float, default=0.01)
        parser.add_argument("--max-ratio", type=float, default=0.03)
        parser.add_argument("--ratio-steps", type=int, default=5)
        parser.add_argument("--iterations", type=int, default=10)
        return parser

    def test_arg_validation(self):
        parser = self._create_parser()
        test_cases = [
            (["--portfolio", "-100"], "Negative portfolio value"),
            (["--ratio", "-0.01"], "Negative ratio"),
            (["--min-ratio", "-0.01"], "Negative min-ratio"),
            (["--ratio-steps", "0"], "Zero ratio-steps"),
            (["--iterations", "0"], "Zero iterations")
        ]
        for args, error_msg in test_cases:
            with self.subTest(args=args, msg=error_msg):
                with self.assertRaises(SystemExit):
                    parser.parse_args(args)

    def test_comparison_function(self):
        data_provider = main.tail_risk_hedge.YahooFinanceDataProvider(seed=42)
        result_df = main.run_comparison(data_provider, 100000, [0.01, 0.02], "stable", iterations=1)
        self.assertEqual(len(result_df), 2)  # One row per ratio
        self.assertIn("insurance_ratio", result_df.columns)

if __name__ == "__main__":
    unittest.main()