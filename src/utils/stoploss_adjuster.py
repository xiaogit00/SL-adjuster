from src.services import binanceREST
from src.utils.supabase_client_post import log_into_supabase
import logging
import time

def adjust_SL_orders(adjustment_orders):
    order_ids = []
    for order in adjustment_orders:
        logging.info(f"Attempting to adjust SL the following order: {order}")

        order_id = order['order_id']
        order_ids.append(order_id)
        symbol = order['symbol']
        side = order['side']
        trailing_value = order['order_group']['trailing_value']
        trailing_price = order['order_group']['trailing_price']
        next_stoploss_price = order['order_group']['next_stoploss_price']
        qty = order['qty']
        group_id = order['order_group']['group_id']
        binanceREST.cancel_stop_market_orders(symbol, order_id)
        time.sleep(2)
        new_stoploss_order_id = None
        try:
            new_stoploss_order_id = binanceREST.set_stop_loss(symbol, side, next_stoploss_price, qty)
        except:
            logging.error("Attempting to retry set stop loss...")
            new_stoploss_order_id = binanceREST.set_stop_loss(symbol, side, next_stoploss_price, qty)
        if not new_stoploss_order_id:
            logging.error(f"❌ Did not manage to set stop loss for {order_id}, continue to next order.")
            continue
        direction = "LONG" if side == "SELL" else "SHORT"

        # Log new stop loss into Supabase       
        group_order_data = {
            "group_id": group_id,
            "order_id": new_stoploss_order_id,
            "type": "SL",
            "direction": direction,
            "current_stop_loss": next_stoploss_price,
            "trailing_value": trailing_value,
            "next_stoploss_price": (next_stoploss_price + trailing_value) if direction=="LONG" else (next_stoploss_price - trailing_value),
            "trailing_price": (trailing_price + trailing_value) if direction=="LONG" else (trailing_price - trailing_value),
        }
        try:
            log_into_supabase(group_order_data)
            logging.info("✅ NEW SL Order logged to Supabase")
            logging.info(f"✅ Successfully adjusted one SL order: {order_id}")
        except Exception as e:
            logging.error(f"Failed to log NEW STOPLOSS trade to Supabase: {e}")
    logging.info(f"✅ Successfully adjusted all SL orders: {order_ids}")

def check_for_SL_adjustments(open_sl_orders, close_price) -> list: #TO-DO
    logging.info("Checking whether SL orders hit close price with params: ")
    logging.info(f'open_sl_orders: {open_sl_orders}')
    logging.info(f'close_price: {close_price}')
    adjustments = []
    for order in open_sl_orders:
        direction = order['direction']
        if direction == "LONG":
            if close_price > float(order['order_group']['trailing_price']):
                logging.info(f"✅ SL Adjustment will be made.")
                adjustments.append(order)
        elif direction == "SHORT":
            if close_price < float(order['order_group']['trailing_price']):
                logging.info(f"✅ SL Adjustment will be made.")
                adjustments.append(order)
    # If direction is LONG, then 
    if not adjustments:
        logging.info(f"😉 No trades need to be adjusted.")
    return adjustments

'''
SL order at $95
Get SL order 
training_
Current close price is $106
'''