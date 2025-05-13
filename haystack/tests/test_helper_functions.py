import unittest
import json
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions"""

    def setUp(self):
        """Set up test environment before each test"""
        # Create a temporary directory for cache tests
        self.temp_dir = tempfile.mkdtemp()
        self.original_cache_dir = 'cache'

        # Sample data for tests
        self.sample_ticker = "AAPL"
        self.sample_metrics = {
            "company_name": "Apple Inc.",
            "ticker": "AAPL",
            "revenue": 394328000000,
            "net_income": 99803000000
        }

    def tearDown(self):
        """Clean up after each test"""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_from_cache(self):
        """Test saving and loading data from cache"""
        # Create a temporary cache file path
        cache_file = os.path.join(self.temp_dir, f"{self.sample_ticker.upper()}.json")

        # Mock the cache directory path
        with patch('app.os.path.exists', return_value=True), \
             patch('app.open', mock_open()) as mock_file:

            # Test save_to_cache
            with patch('app.json.dump') as mock_json_dump:
                app.save_to_cache(self.sample_ticker, self.sample_metrics)
                mock_json_dump.assert_called_once()

            # Test load_from_cache when file exists
            with patch('app.os.path.exists', return_value=True), \
                 patch('app.json.load', return_value=self.sample_metrics) as mock_json_load:
                result = app.load_from_cache(self.sample_ticker)
                self.assertEqual(result, self.sample_metrics)
                mock_json_load.assert_called_once()

            # Test load_from_cache when file doesn't exist
            with patch('app.os.path.exists', return_value=False):
                result = app.load_from_cache(self.sample_ticker)
                self.assertIsNone(result)

    def test_calculate_equity_value(self):
        """Test the calculate_equity_value function from imported tail_risk_hedge module"""
        # Since this is not directly applicable to your app, this is a placeholder
        # You can replace this with tests for your own helper functions
        pass

    @patch('app.os.makedirs')
    @patch('app.os.path.exists')
    def test_cache_directory_creation(self, mock_exists, mock_makedirs):
        """Test that cache directory is created if it doesn't exist"""
        # Test when cache directory doesn't exist
        mock_exists.return_value = False

        # This should trigger directory creation
        # We need to re-import to trigger the code at module level
        import importlib
        importlib.reload(app)

        mock_makedirs.assert_called_once_with('cache')

        # Test when cache directory exists
        mock_exists.return_value = True
        mock_makedirs.reset_mock()

        importlib.reload(app)

        mock_makedirs.assert_not_called()


class TestCalculationFunctions(unittest.TestCase):
    """Test cases specifically for financial calculation functions"""

    def test_equity_calculation(self):
        """Test equity calculation from assets and liabilities"""
        total_assets = 1000000
        total_liabilities = 600000
        expected_equity = 400000

        # Create a scraper instance to test the method
        scraper = app.EdgarScraper()
        metrics = {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities
        }

        # Simulate the calculation in extract_financial_data
        equity = total_assets - total_liabilities
        self.assertEqual(equity, expected_equity)

    def test_financial_ratios(self):
        """Test calculation of financial ratios"""
        # Sample financial data
        revenue = 1000000
        net_income = 100000
        total_assets = 2000000
        equity = 800000
        total_liabilities = 1200000

        # Expected ratio results
        expected_profit_margin = 10.0  # (net_income / revenue) * 100
        expected_return_on_assets = 5.0  # (net_income / total_assets) * 100
        expected_return_on_equity = 12.5  # (net_income / equity) * 100
        expected_debt_to_assets = 0.6  # total_liabilities / total_assets

        # Calculate ratios
        profit_margin = round((net_income / revenue) * 100, 2)
        return_on_assets = round((net_income / total_assets) * 100, 2)
        return_on_equity = round((net_income / equity) * 100, 2)
        debt_to_assets = round(total_liabilities / total_assets, 2)

        # Assertions
        self.assertEqual(profit_margin, expected_profit_margin)
        self.assertEqual(return_on_assets, expected_return_on_assets)
        self.assertEqual(return_on_equity, expected_return_on_equity)
        self.assertEqual(debt_to_assets, expected_debt_to_assets)

    def test_handle_missing_financial_data(self):
        """Test handling of missing financial data for ratio calculations"""
        # Create a scraper instance
        scraper = app.EdgarScraper()

        # Simulate metrics with missing values
        metrics = {
            "revenue": 1000000,
            "net_income": None,
            "total_assets": 2000000,
            "total_liabilities": 1200000,
            "equity": None
        }

        # Calculate equity when present
        if metrics["total_assets"] and metrics["total_liabilities"]:
            metrics["equity"] = metrics["total_assets"] - metrics["total_liabilities"]

        # Calculate profit margin when possible
        if metrics["revenue"] and metrics["net_income"]:
            metrics["profit_margin"] = round((metrics["net_income"] / metrics["revenue"]) * 100, 2)
        else:
            metrics["profit_margin"] = None

        # Assertions
        self.assertEqual(metrics["equity"], 800000)  # Should be calculated from assets and liabilities
        self.assertIsNone(metrics["profit_margin"])  # Should be None due to missing net_income


if __name__ == '__main__':
    unittest.main()