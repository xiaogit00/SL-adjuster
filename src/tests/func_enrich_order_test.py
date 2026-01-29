from src.services import db
import unittest
import asyncio
import logging
from src.services import binanceREST
import json

logger = logging.getLogger()
logger.level = logging.INFO

class TestEnrichOrders(unittest.TestCase):
    def setUp(self):
        db.delete_orders()
        db.delete_order_groups()
        db.delete_candles()
        print('\n-------------------\n')
        print("Entering TestEnrichOrders positive case")
        order_groups_data = {
            "group_id": 1,
            "order_id": "1",
            "type": "STOP_MARKET",
            "direction": "LONG",
            "current_stop_loss": "95",
            "trailing_value": "3.5",
            "trailing_price": "103.5",
            "next_stoploss_price": "98.5"
        }

        candle_data=json.dumps({
            "open": "139.10",
            "high": "149.10",
            "low": "129.10",
            "close": "138.10",
        })


        trade_metadata = json.dumps({
            'risk_amount': 10,
            'fee': 0.1,
            'portfolio_threshold': 20,
            'rv_period': 2,
            'ema_period': 9,
            'rv_threshold': 2.8,
            'trailing_percentage': 0.7
        })
        db.insertNewOrderGroup(1, order_groups_data)
        db.insertNewCandle(candle_data, 1, 1, trade_metadata)


    def tearDown(self):
        print("teardown running...")
    def test_enrich_orders(self):
        latest_open_SL_order = {
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
            "ask_price": "136.12"
        }
        enriched_order = db.enrich_order(latest_open_SL_order)
        expected_keys = {"order_id", "status", 'symbol', "side", 'order_type', 'qty', 'direction', 'ask_price', 'updated_at', 'filled_price','created_at', 'order_group_data', 'candle_data'}
        self.assertEqual(set(enriched_order.keys()),expected_keys )

        self.assertIn("current_stop_loss", enriched_order['order_group_data'])
        self.assertIn("candle_data", enriched_order['candle_data'])
        
class TestEnrichOrdersNegativeCase1(unittest.TestCase):
    '''When order_groups table does not contain order_groups for orderID -> expects critical exception and stop program'''
    def setUp(self):
        db.delete_orders()
        db.delete_order_groups()
        db.delete_candles()
        print('\n-------------------\n')
        print("Entering TestEnrichOrders negative case")
        order_groups_data = {
            "group_id": 1,
            "order_id": "555",
            "type": "STOP_MARKET",
            "direction": "LONG",
            "current_stop_loss": "95",
            "trailing_value": "3.5",
            "trailing_price": "103.5",
            "next_stoploss_price": "98.5"
        }

        candle_data=json.dumps({
            "open": "139.10",
            "high": "149.10",
            "low": "129.10",
            "close": "138.10",
        })


        trade_metadata = json.dumps({
            'risk_amount': 10,
            'fee': 0.1,
            'portfolio_threshold': 20,
            'rv_period': 2,
            'ema_period': 9,
            'rv_threshold': 2.8,
            'trailing_percentage': 0.7
        })
        db.insertNewOrderGroup(1, order_groups_data)
        db.insertNewCandle(candle_data, 1, 1, trade_metadata)


    def tearDown(self):
        print("teardown running...")
    def test_enrich_orders(self):
        latest_open_SL_order = {
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
            "ask_price": "136.12"
        }
        with self.assertRaises(ValueError) as cm:
            db.enrich_order(latest_open_SL_order)

        self.assertIn("Not exactly 1 order_groups order found", str(cm.exception))

class TestEnrichOrdersNegativeCase2(unittest.TestCase):
    '''When order_groups is found, but candle for that order_id is not found'''
    def setUp(self):
        db.delete_orders()
        db.delete_order_groups()
        db.delete_candles()
        print('\n-------------------\n')
        print("Entering TestEnrichOrders negative case")
        order_groups_data = {
            "group_id": 1,
            "order_id": "1",
            "type": "STOP_MARKET",
            "direction": "LONG",
            "current_stop_loss": "95",
            "trailing_value": "3.5",
            "trailing_price": "103.5",
            "next_stoploss_price": "98.5"
        }

        db.insertNewOrderGroup(1, order_groups_data)


    def tearDown(self):
        print("teardown running...")
    def test_enrich_orders(self):
        latest_open_SL_order = {
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
            "ask_price": "136.12"
        }
        with self.assertRaises(ValueError) as cm:
            db.enrich_order(latest_open_SL_order)

        self.assertIn("Not exactly 1 candle found.", str(cm.exception))
if __name__ == '__main__':
    unittest.main()