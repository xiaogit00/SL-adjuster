
from dotenv import load_dotenv
from src.utils.supabase_client import get_supabase_client
import logging, os
from datetime import datetime

load_dotenv()
supabase = get_supabase_client()
orders_table = "orders"
order_groups_table = "order_groups"
trades_table = "trades"

def get_open_SL_orders():
    """Returns open SL orders with their groups info in 'order_group' field."""
    logging.info("Trying to get open SL orders from DB...")
    try:
        # Step 1: Fetch relevant orders
        orders_resp = supabase.table(orders_table) \
            .select("*") \
            .eq("order_type", "STOP_MARKET") \
            .eq("status", "NEW") \
            .execute()
        orders = orders_resp.data or []
        if not orders:
            logging.info("No open SL orders found.")
            return []

        # Step 2: Append the latest SL order from the order_group into the order data
        order_ids = list({order['order_id'] for order in orders})
        groups_resp = supabase.table(order_groups_table) \
            .select("*") \
            .in_("order_id", order_ids) \
            .eq("type", "SL") \
            .execute() 
        groups = groups_resp.data or []

        # Step 3: Map and merge
        group_map = {g['order_id']: g for g in groups}
        orders_with_groups = [
            {**order, "order_group": group_map[order['order_id']]}
            for order in orders if order['order_id'] in group_map
        ]

        logging.info(f"Retrieved open SL orders: {orders_with_groups}")
        return orders_with_groups

    except Exception as e:
        logging.exception("Error retrieving open SL orders from Supabase")
        return []
