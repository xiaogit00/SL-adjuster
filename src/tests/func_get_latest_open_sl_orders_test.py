from src.services import db
import unittest
import asyncio
import logging

logger = logging.getLogger()
logger.level = logging.INFO

class TestLatestOpenSLOrder(unittest.TestCase):
    def setUp(self):
        print('\n-------------------\n')
        print("Entering test 1: TestLatestOpenSLOrder")
        db.delete_orders()
        new_filled_SL_order = {
            "order_id": 1,
            "status": "FILLED",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "ask_price": "136.12"
        }
        new_open_SL_order = {
            "order_id": 2,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "ask_price": "136.12"
        }
        
        db.insertNewOrderByType("STOP_MARKET", new_filled_SL_order)
        db.insertNewOrderByType("STOP_MARKET", new_open_SL_order)
    def tearDown(self):
        print("teardown running...")
    def test_get_open_SL_orders(self):
        res: dict | None = db.get_latest_open_SL_order()
        expected_keys = {"order_id", "status", 'symbol', "side", 'order_type', 'qty', 'direction', 'ask_price', 'updated_at', 'filled_price','created_at'}
        self.assertEqual(expected_keys, set(res.keys()))
        print(f"✅ Successfully retrieved latest open SL order: {res}")

class TestLatestOpenSLOrderNegativeCase(unittest.TestCase):
    'Tests the negative case where orders DB contains 1 MO and 1SL, both filled'
    def setUp(self):
        print('\n-------------------\n')
        print("Entering test 2: TestLatestOpenSLOrderNegativeCase")
        db.delete_orders()
        new_filled_MO_order = {
            "order_id": 1,
            "status": "FILLED",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "ask_price": "136.12"
        }
        new_open_SL_order = {
            "order_id": 2,
            "status": "FILLED",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "ask_price": "136.12"
        }
        
        db.insertNewOrderByType("STOP_MARKET", new_filled_MO_order)
        db.insertNewOrderByType("STOP_MARKET", new_open_SL_order)
    def tearDown(self):
        db.delete_orders()
    def test_get_open_SL_orders(self):
        res: dict | None = db.get_latest_open_SL_order()
        expected_keys = None
        self.assertEqual(expected_keys, res)
        print(f"✅ When both orders are filled, res returns None")

class TestTwoOpenSLOrdersFound(unittest.TestCase):
    'Tests the negative case where 2 OPEN SL orders found'
    def setUp(self):
        print('\n-------------------\n')
        print("Entering test 3: TestTwoOpenSLOrdersFound")
        db.delete_orders()
        new_open_SL_order = {
            "order_id": 1,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "ask_price": "136.12"
        }
        new_open_SL_order2 = {
            "order_id": 2,
            "status": "NEW",
            "symbol": "SOLUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "qty": "0.04",
            "direction": "LONG",
            "created_at": 1768015698681,
            "ask_price": "136.12"
        }
        
        db.insertNewOrderByType("STOP_MARKET", new_open_SL_order)
        db.insertNewOrderByType("STOP_MARKET", new_open_SL_order2)
    def tearDown(self):
        print("Tearing down...")
        # db.delete_orders()
    def test_get_open_SL_orders(self):
        with self.assertRaises(ValueError) as cm:
            db.get_latest_open_SL_order()

        self.assertIn("More than 1 open SL order", str(cm.exception))
        print(f"✅ When there's 2 open SL orders, db call throws exception: {str(cm.exception)}")

if __name__ == '__main__':
    unittest.main()