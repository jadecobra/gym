import unittest
import itch_order_flow_messages
import datetime

@unittest.skip
class TestITCHOrderBook(unittest.TestCase):

    def test_format_timestamp(self):
        self.assertEqual(
            itch_order_flow_messages.format_time('23:59:01'),
            ''
        )