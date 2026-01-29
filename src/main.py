import logging, asyncio
from src.services import db
from src.services import binanceWebsocket 
from src.utils.logger import init_logger
from src.utils import stoploss_adjuster
from src.utils.type_defs import ExecutionStatus

async def main():
    init_logger()
    binance_price_queue = asyncio.Queue()
    asyncio.create_task(binanceWebsocket.websocket_binance_price_listener(binance_price_queue)) # Creates a background task. 
    while True:
        new_price = await binance_price_queue.get()
        logging.info("🔴 Awaiting next event in queue from Binance event websocket...")
        logging.info(f"😱 Received new Binance event! Event: {new_price}")
        candle_price = {
            "close": float(new_price['c']),
            "open": float(new_price['o']),
            "low": float(new_price['l']),
            "high": float(new_price['h']),
        }
        order: dict | None = db.get_latest_open_SL_order() # Ref response in sample_api
        if order == None: 
            logging.info("No open orders found, continuing to next loop.")
            continue
        enriched_order = db.enrich_order(order)
        should_adjust = stoploss_adjuster.check_for_SL_adjustment(enriched_order, candle_price['close'])
        if should_adjust:
            stoploss_adjuster.adjust_SL_order(enriched_order, candle_price)
        logging.info("🔚 Exiting one cycle of candle price check.")
 

asyncio.run(main())

