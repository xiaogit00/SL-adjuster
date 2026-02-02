from src.services import binanceREST
from src.services import db
from src.utils.logger import init_logger
import unittest
import asyncio


class TestDB(unittest.TestCase):
    def setUp(self):
        init_logger()
    def test_bianance(self):
        res = binanceREST.execute_stop_loss_algo_order('SOLUSDT', "SELL", 93.10033, 5.04)
        print(res)


if __name__ == '__main__':
    asyncio.run(unittest.main())