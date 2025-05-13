import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app


class TestEdgarScraper(unittest.TestCase):
    """Test cases for the EdgarScraper class"""

    def setUp(self):
        """Set up test environment before each test"""
        self.scraper = app.EdgarScraper()

        # Sample data for tests
        self.sample_cik = "0000320193"  # Apple Inc.
        self.sample_ticker = "AAPL"
        self.sample_company_tickers = {
            "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
            "1": {"cik_str": 789019, "ticker": "MSFT", "title": "Microsoft Corp"}
        }

        # Sample 10-K URLs and responses
        self.sample_10k_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm"
        self.sample_submission_data = {
            "cik": "0000320193",
            "filings": {
                "recent": {
                    "form": ["10-K", "8-K", "4", "10-Q"],
                    "filingDate": ["2022-10-28", "2022-10-28", "2022-10-28", "2022-07-29"],
                    "accessionNumber": ["0000320193-22-000108", "0000320193-22-000107", "0000320193-22-000106", "0000320193-22-000072"]
                }
            }
        }

        self.sample_filing_details = {
            "directory": {
                "item": [
                    {"name": "aapl-20220924.htm", "type": "text/html"},
                    {"name": "Financial_Report.xlsx", "type": "application/vnd.ms-excel"}
                ]
            }
        }

        # Sample HTML content
        self.sample_10k_html = """
        <html>
            <head>
                <title>Apple Inc. | Form 10-K</title>
                <meta name="documentdate" content="2022-09-24">
                <meta name="filing-date" content="2022-10-28">
            </head>
            <body>
                <company-name>Apple Inc.</company-name>
                <p>For the fiscal year ended September 24, 2022</p>
                <table>
                    <tr>
                        <td>Total Revenue</td>
                        <td>$394,328 million</td>
                    </tr>
                    <tr>
                        <td>Net Income</td>
                        <td>$99,803 million</td>
                    </tr>
                    <tr>
                        <td>Total Assets</td>
                        <td>$352,755 million</td>
                    </tr>
                    <tr>
                        <td>Total Liabilities</td>
                        <td>$302,083 million</td>
                    </tr>
                    <tr>
                        <td>Cash and Cash Equivalents</td>
                        <td>$23,646 million</td>
                    </tr>
                    <tr>
                        <td>Long-Term Debt</td>
                        <td>$98,959 million</td>
                    </tr>
                    <tr>
                        <td>Operating Income</td>
                        <td>$119,437 million</td>
                    </tr>
                </table>
            </body>
        </html>
        """

    @patch('app.requests.get')
    def test_search_company_success(self, mock_get):
        """Test successful company search by ticker"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_company_tickers
        mock_get.return_value = mock_response

        # Call the method
        cik, error = self.scraper.search_company(self.sample_ticker)

        # Assertions
        self.assertEqual(cik, "0000320193")
        self.assertIsNone(error)
        mock_get.assert_called_once_with(
            "https://www.sec.gov/files/company_tickers.json",
            headers=self.scraper.headers
        )

    @patch('app.requests.get')
    def test_search_company_not_found(self, mock_get):
        """Test company search with non-existent ticker"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_company_tickers
        mock_get.return_value = mock_response

        # Call the method
        cik, error = self.scraper.search_company("NONEXIST")

        # Assertions
        self.assertIsNone(cik)
        self.assertIn("not found", error)

    @patch('app.requests.get')
    def test_search_company_request_error(self, mock_get):
        """Test company search with request error"""
        # Configure mock to raise an exception
        mock_get.side_effect = Exception("Connection error")

        # Call the method
        cik, error = self.scraper.search_company(self.sample_ticker)

        # Assertions
        self.assertIsNone(cik)
        self.assertIn("Error searching for company", error)

    @patch('app.requests.get')
    def test_get_recent_10k_url_success(self, mock_get):
        """Test successful retrieval of 10-K URL"""
        # Configure mocks
        mock_response_1 = MagicMock()
        mock_response_1.json.return_value = self.sample_submission_data

        mock_response_2 = MagicMock()
        mock_response_2.json.return_value = self.sample_filing_details

        mock_get.side_effect = [mock_response_1, mock_response_2]

        # Call the method
        url, error = self.scraper.get_recent_10k_url(self.sample_cik)

        # Assertions
        self.assertIsNotNone(url)
        self.assertIn("edgar/data/320193", url)
        self.assertIsNone(error)
        self.assertEqual(mock_get.call_count, 2)

    @patch('app.requests.get')
    def test_get_recent_10k_url_no_filings(self, mock_get):
        """Test 10-K URL retrieval with no filings"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"filings": {}}
        mock_get.return_value = mock_response

        # Call the method
        url, error = self.scraper.get_recent_10k_url(self.sample_cik)

        # Assertions
        self.assertIsNone(url)
        self.assertIn("No recent filings found", error)

    @patch('app.requests.get')
    def test_get_recent_10k_url_no_10k(self, mock_get):
        """Test 10-K URL retrieval with no 10-K filing"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "filings": {
                "recent": {
                    "form": ["8-K", "4", "10-Q"],
                    "filingDate": ["2022-10-28", "2022-10-28", "2022-07-29"],
                    "accessionNumber": ["0000320193-22-000107", "0000320193-22-000106", "0000320193-22-000072"]
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the method
        url, error = self.scraper.get_recent_10k_url(self.sample_cik)

        # Assertions
        self.assertIsNone(url)
        self.assertIn("No 10-K filing found", error)

    @patch('app.requests.get')
    def test_extract_financial_data_success(self, mock_get):
        """Test successful extraction of financial data"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.text = self.sample_10k_html
        mock_get.return_value = mock_response

        # Call the method
        metrics, error = self.scraper.extract_financial_data(self.sample_10k_url)

        # Assertions
        self.assertIsNotNone(metrics)
        self.assertIsNone(error)
        self.assertEqual(metrics["company_name"], "Apple Inc.")
        self.assertEqual(metrics["revenue"], 394328000000)
        self.assertEqual(metrics["net_income"], 99803000000)
        self.assertEqual(metrics["total_assets"], 352755000000)
        self.assertEqual(metrics["total_liabilities"], 302083000000)
        self.assertEqual(metrics["cash_and_equivalents"], 23646000000)
        self.assertEqual(metrics["long_term_debt"], 98959000000)
        self.assertEqual(metrics["operating_income"], 119437000000)
        self.assertEqual(metrics["fiscal_year_end"], "2022-09-24")
        self.assertEqual(metrics["filing_date"], "2022-10-28")

        # Calculated metrics
        self.assertEqual(metrics["equity"], 50672000000)  # total_assets - total_liabilities
        self.assertAlmostEqual(metrics["profit_margin"], 25.31, places=2)  # (net_income / revenue) * 100
        self.assertAlmostEqual(metrics["return_on_assets"], 28.29, places=2)  # (net_income / total_assets) * 100
        self.assertAlmostEqual(metrics["return_on_equity"], 196.96, places=2)  # (net_income / equity) * 100
        self.assertAlmostEqual(metrics["debt_to_assets_ratio"], 0.86, places=2)  # total_liabilities / total_assets

    @patch('app.requests.get')
    def test_extract_financial_data_request_error(self, mock_get):
        """Test financial data extraction with request error"""
        # Configure mock to raise an exception
        mock_get.side_effect = Exception("Connection error")

        # Call the method
        metrics, error = self.scraper.extract_financial_data(self.sample_10k_url)

        # Assertions
        self.assertIsNone(metrics)
        self.assertIn("Error extracting financial data", error)

    def test_parse_financial_value(self):
        """Test parsing of financial values from text"""
        # Test cases with different formats
        test_cases = [
            ("$394,328 million", 394328000000),
            ("394,328,000", 394328000),
            ("$1.5 billion", 1500000000),
            ("1.5b", 1500000000),
            ("$750 million", 750000000),
            ("750m", 750000000),
            ("1,234,567", 1234567),
            ("$1,234.56", 1234.56),
            ("invalid", None)
        ]

        for input_value, expected_output in test_cases:
            result = self.scraper._parse_financial_value(input_value)
            self.assertEqual(result, expected_output)

    def test_extract_fiscal_year(self):
        """Test extraction of fiscal year from document"""
        from bs4 import BeautifulSoup

        # Sample HTML with fiscal year mentions
        html_samples = [
            """<html><body><p>For the fiscal year ended September 24, 2022</p></body></html>""",
            """<html><body><p>Fiscal year ending on December 31, Caca</p></body></html>""",
            """<html><head><meta name="documentdate" content="2022-09-24"></head><body></body></html>"""
        ]

        expected_results = [
            "2022-09-24",  # First sample should extract from text
            None,          # Second sample has an invalid date
            "2022-09-24"   # Third sample should extract from meta tag
        ]

        for i, html in enumerate(html_samples):
            soup = BeautifulSoup(html, 'html.parser')
            result = self.scraper._extract_fiscal_year(soup)
            self.assertEqual(result, expected_results[i])

    def test_extract_filing_date(self):
        """Test extraction of filing date from document"""
        from bs4 import BeautifulSoup

        # Sample HTML with filing date mentions
        html_samples = [
            """<html><head><meta name="filing-date" content="2022-10-28"></head><body></body></html>""",
            """<html><body><p>Filed on: October 28, 2022</p></body></html>""",
            """<html><body><p>Date of report: October 28, 2022</p></body></html>"""
        ]

        expected_results = [
            "2022-10-28",  # First sample should extract from meta tag
            "2022-10-28",  # Second sample should extract from text
            "2022-10-28"   # Third sample should extract from text
        ]

        for i, html in enumerate(html_samples):
            soup = BeautifulSoup(html, 'html.parser')
            result = self.scraper._extract_filing_date(soup)
            self.assertEqual(result, expected_results[i])


if __name__ == '__main__':
    unittest.main()