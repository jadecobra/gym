import unittest
import pandas_datareader_demo
import pandas_datareader


class TestGettingData(unittest.TestCase):

    sp_500 = pandas_datareader_demo.get_sp_500()

    @unittest.skip
    def test_sp_500_classification_data(self):
        self.assertEqual(
            sorted(self.sp_500[0].columns),
            sorted([
                'CIK',
                'Date first added',
                'Founded',
                'GICS Sector',
                'GICS Sub-Industry',
                'Headquarters Location',
                'SEC filings',
                'Security',
                'Symbol'
            ])
        )

    @unittest.skip
    def test_sp_500_date_added_data(self):
        self.assertEqual(
            sorted(self.sp_500[1].columns),
            sorted([
                'Added', 'Added.1', 'Date', 'Reason', 'Removed', 'Removed.1'
            ])
        )

    @unittest.skip
    def test_get_nasdaq_symbols(self):
        self.assertEqual(
            sorted(pandas_datareader.nasdaq_trader.get_nasdaq_symbols().columns),
            [
                'CQS Symbol',
                'ETF',
                'Financial Status',
                'Listing Exchange',
                'Market Category',
                'NASDAQ Symbol',
                'Nasdaq Traded',
                'NextShares',
                'Round Lot Size',
                'Security Name',
                'Test Issue'
            ]
        )