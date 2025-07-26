import requests, os
import time
from dotenv import load_dotenv
supabase_url = os.getenv("SUPABASE_URL")
supbase_api_key = os.getenv("SUPABASE_API_KEY")
supabase_jwt = os.getenv("SUPABASE_JWT")
import logging

load_dotenv()
orders_table = "orders" if int(os.getenv("STRATEGY_ENV")) == 1 else "orders2"
order_groups_table = "order_groups" if int(os.getenv("STRATEGY_ENV")) == 1 else "order_groups2"
trades_table = "trades" if int(os.getenv("STRATEGY_ENV")) == 1 else "trades2"

def log_into_supabase(data, table_name=order_groups_table):
    logging.info(f"Attempting to add entry into order_groups with params: {data}")
    url = f"{supabase_url}/rest/v1/{table_name}"
    headers = {
        "apikey": supbase_api_key,
        "Authorization": f"Bearer {supabase_jwt}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code in (200, 201):
        logging.info("✅ Successfully logged data:", response.json())
        return response.json()
    else:
        logging.exception(f"❌ Failed to log data ({response.status_code}): {response.text}")
        return {"error": response.text, "status_code": response.status_code}

