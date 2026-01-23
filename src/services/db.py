
from dotenv import load_dotenv
from src.utils.supabase_client import get_supabase_client
import logging, os
from datetime import datetime

load_dotenv()
supabase = get_supabase_client()
orders_table = "orders"
order_groups_table = "order_groups"
trades_table = "trades"
candles_table = "candles"

def get_latest_open_SL_order():
    """Returns open SL orders with their groups info in 'order_group' field."""
    logging.info("Trying to get open SL orders from DB...")
    try:
        # Step 1: Fetch the only SL
        orders_resp = supabase.table(orders_table) \
            .select("*") \
            .eq("order_type", "STOP_MARKET") \
            .eq("status", "NEW") \
            .execute()
        orders = orders_resp.data or []
        if not orders:
            logging.info("No open SL orders found.")
            return []
        assert len(orders) == 1, f"More than 1 open SL order found, response for orders: {orders_resp}"
        assert orders[0].get("order_id") is not None, f"Issue with fetching latest open orders, no order_id found for response:{orders_resp}"
        order_data = orders[0]

        # Step 2: Fetch the order_group info for that SL order
        SL_order_id = orders[0]['order_id']
        groups_resp = supabase.table(order_groups_table) \
            .select("*") \
            .eq("order_id", SL_order_id) \
            .execute() 
        order_group = groups_resp.data or []
        assert len(order_group) == 1, f"Not exactly 1 order_groups order found, response for orders: {groups_resp}"
        assert order_group[0].get("order_id") is not None, f"Issue with fetching latest group_order for order {SL_order_id} orders, no order_id found for response:{groups_resp}"
        order_group_data = order_group[0]

        # Step 3: Get the candle data for all these SL orders
        candles_resp = supabase.table(candles_table) \
            .select("*") \
            .in_("order_id", SL_order_id) \
            .execute() 
        order_candle = candles_resp.data or []
        assert len(order_candle) == 1, f"Not exactly 1 order_candle found, response for order_candle: {candles_resp}"
        assert order_candle[0].get("order_id") is not None, f"Issue with fetching latest order_candle for order {SL_order_id} orders, no order_id found for response:{candles_resp}"
        order_candle_data = order_candle[0]

        # Step 4: Map and merge
        order_enriched = {
            **order_data,
            "order_group_data": order_group_data,
            "candle_data": order_candle_data
        }

        logging.info(f"Returning enriched order data: {order_enriched}")
        return order_enriched

    except Exception as e:
        logging.exception("Error retrieving open SL orders from Supabase")
        return []

def insertNewCandle(candle_data, new_SL_order_id, group_id, trade_metadata):
    logging.info(f"OrderID: {new_SL_order_id} | Inserting candle data into candles table: {candle_data}")
    logging.info(f"Trade Metadata: {trade_metadata}")

    candle_data = {
        "order_id": new_SL_order_id,
        "group_id": group_id,
        "candle_data": candle_data,
        "trade_metadata": trade_metadata
    }
    
    try:
        res = (
            supabase.table(candles_table)
            .insert(candle_data)
            .execute()
        )
        if res.data:
            logging.info(f"Successfully inserted new entry with order_id {new_SL_order_id} into order_group table.")
        return res
    except Exception as e: 
        print("There's an issue getting supabase table: ", e)