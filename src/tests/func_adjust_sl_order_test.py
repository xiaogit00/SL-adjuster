from src.services import db
import unittest
import asyncio
import logging
from src.services import binanceREST 
from src.utils import stoploss_adjuster
import json
import time

logger = logging.getLogger()
logger.level = logging.INFO

# class RefreshDB(unittest.TestCase):
#     def test_refresh_db(self):
#         binanceREST.cancel_algo_orders("SOLUSDT")
#         db.delete_candles()
#         db.delete_order_groups()
#         db.delete_orders()
class TestAdjustSL(unittest.TestCase):
    def setUp(self):
        # binanceREST.cancel_algo_orders("SOLUSDT")
        # db.delete_candles()
        # db.delete_order_groups()
        # db.delete_orders()
        print('\n-------------------\n')
        print("Entering test 1: TestLatestOpenSLOrder")
        res = binanceREST.execute_stop_loss_algo_order("SOLUSDT", "SELL", 110, 0.04)
        order_id = res['algoId']
        candle_data=json.dumps({
            "open": "100",
            "high": "100",
            "low": "100",
            "close": "100",
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
        db.insertNewCandle(candle_data, order_id, 1, trade_metadata)

    def tearDown(self):
        print("teardown running...")
    def test_adjust_SL(self):
        time.sleep(10)
        order: dict | None = db.get_latest_open_SL_order()
        enriched_order = db.enrich_order(order)
        candle_price = {
            "open": "105",
            "high": "105",
            "low": "105",
            "close": "105",
        }
        stoploss_adjuster.adjust_SL_order(enriched_order, candle_price)
        print(f"✅ Successfully retrieved latest open SL order: ")

if __name__ == '__main__':
    unittest.main()