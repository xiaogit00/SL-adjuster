from src.services import db
import unittest
import asyncio
import logging

logger = logging.getLogger()
logger.level = logging.INFO
from src.utils import stoploss_adjuster

class TestCheckForSLAdjustment(unittest.TestCase):
    def setUp(self):
        print('\n-------------------\n')
    def tearDown(self):
        print("teardown running...")
    def test_will_adjust_long(self):
        print("Entering test 1: test_will_adjust")
        order_enriched = {
            "order_id": 1,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "order_type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "updated_at": 1768015698681,
            "filled_price": None,
            "ask_price": "136.12",
            "order_group_data": {
                "group_id": 1,
                "order_id": 1,
                "type": "STOP_MARKET",
                "direction": "LONG",
                "current_stop_loss": 95,
                "trailing_value": 3.5,
                "created_at": "2026-01-29T04:22:23.184374",
                "next_stoploss_price": 98.5,
                "trailing_price": 103.5,
            },
            "candle_data": {
                "order_id": 1,
                "candle_data": '{"open": "139.10", "high": "149.10", "low": "129.10", "close": "138.10"}',
                "trade_metadata": '{"risk_amount": 10, "fee": 0.1, "portfolio_threshold": 20, "rv_period": 2, "ema_period": 9, "rv_threshold": 2.8, "trailing_percentage": 0.7}',
                "created_at": "2026-01-29T04:22:23.215727+00:00",
                "group_id": 1,
            },
        }
        close_price = 105
        res = stoploss_adjuster.check_for_SL_adjustment(order_enriched, close_price)
        self.assertEqual(res, True)
    def test_wont_adjust_long(self):
        print("Entering test 2: test_wont_adjust")
        order_enriched = {
            "order_id": 1,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "order_type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "updated_at": 1768015698681,
            "filled_price": None,
            "ask_price": "136.12",
            "order_group_data": {
                "group_id": 1,
                "order_id": 1,
                "type": "STOP_MARKET",
                "direction": "LONG",
                "current_stop_loss": 95,
                "trailing_value": 3.5,
                "created_at": "2026-01-29T04:22:23.184374",
                "next_stoploss_price": 98.5,
                "trailing_price": 103.5,
            },
            "candle_data": {
                "order_id": 1,
                "candle_data": '{"open": "139.10", "high": "149.10", "low": "129.10", "close": "138.10"}',
                "trade_metadata": '{"risk_amount": 10, "fee": 0.1, "portfolio_threshold": 20, "rv_period": 2, "ema_period": 9, "rv_threshold": 2.8, "trailing_percentage": 0.7}',
                "created_at": "2026-01-29T04:22:23.215727+00:00",
                "group_id": 1,
            },
        }
        close_price = 101
        res = stoploss_adjuster.check_for_SL_adjustment(order_enriched, close_price)
        self.assertEqual(res, False)
    def test_will_adjust_short(self):
        print("Entering test 3: test_will_adjust_short")
        order_enriched = {
            "order_id": 1,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "BUY",
            "order_type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "SHORT",
            "created_at": 1768015698681,
            "updated_at": 1768015698681,
            "filled_price": None,
            "ask_price": "136.12",
            "order_group_data": {
                "group_id": 1,
                "order_id": 1,
                "type": "STOP_MARKET",
                "direction": "SHORT",
                "current_stop_loss": 102,
                "trailing_value": 3.5,
                "created_at": "2026-01-29T04:22:23.184374",
                "next_stoploss_price": 98.5,
                "trailing_price": 95,
            },
            "candle_data": {
                "order_id": 1,
                "candle_data": '{"open": "139.10", "high": "149.10", "low": "129.10", "close": "138.10"}',
                "trade_metadata": '{"risk_amount": 10, "fee": 0.1, "portfolio_threshold": 20, "rv_period": 2, "ema_period": 9, "rv_threshold": 2.8, "trailing_percentage": 0.7}',
                "created_at": "2026-01-29T04:22:23.215727+00:00",
                "group_id": 1,
            },
        }
        close_price = 94
        res = stoploss_adjuster.check_for_SL_adjustment(order_enriched, close_price)
        self.assertEqual(res, True)
    def test_wont_adjust_short(self):
        print("Entering test 4: test_wont_adjust_short")
        order_enriched = {
            "order_id": 1,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "BUY",
            "order_type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "SHORT",
            "created_at": 1768015698681,
            "updated_at": 1768015698681,
            "filled_price": None,
            "ask_price": "136.12",
            "order_group_data": {
                "group_id": 1,
                "order_id": 1,
                "type": "STOP_MARKET",
                "direction": "SHORT",
                "current_stop_loss": 102,
                "trailing_value": 3.5,
                "created_at": "2026-01-29T04:22:23.184374",
                "next_stoploss_price": 98.5,
                "trailing_price": 95,
            },
            "candle_data": {
                "order_id": 1,
                "candle_data": '{"open": "139.10", "high": "149.10", "low": "129.10", "close": "138.10"}',
                "trade_metadata": '{"risk_amount": 10, "fee": 0.1, "portfolio_threshold": 20, "rv_period": 2, "ema_period": 9, "rv_threshold": 2.8, "trailing_percentage": 0.7}',
                "created_at": "2026-01-29T04:22:23.215727+00:00",
                "group_id": 1,
            },
        }
        close_price = 96
        res = stoploss_adjuster.check_for_SL_adjustment(order_enriched, close_price)
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()