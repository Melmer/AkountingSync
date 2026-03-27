import requests
from config import ETSY_API_KEY, ETSY_ACCESS_TOKEN, ETSY_SHOP_ID

BASE = "https://openapi.etsy.com/v3/application"

def _headers():
    return {
        "x-api-key": ETSY_API_KEY,
        "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}",
    }

def get_orders(limit=25, offset=0):
    """Get all payed orders."""
    url = f"{BASE}/shops/{ETSY_SHOP_ID}/receipts"
    params = {
        "limit": limit,
        "offset": offset,
        "was_paid": "true",
        "was_shipped": "false",  # pas aan naar wens
    }
    r = requests.get(url, headers=_headers(), params=params)
    r.raise_for_status()
    return r.json().get("results", [])

def get_order_transactions(receipt_id):
    """Get transations from orders."""
    url = f"{BASE}/shops/{ETSY_SHOP_ID}/receipts/{receipt_id}/transactions"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json().get("results", [])