import requests
from config import AKAUNTING_URL, AKAUNTING_EMAIL, AKAUNTING_PASSWORD, AKAUNTING_COMPANY_ID

def _auth():
    return (AKAUNTING_EMAIL, AKAUNTING_PASSWORD)

def _headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

def _params():
    return {"company_id": AKAUNTING_COMPANY_ID}

def find_or_create_customer(name: str, email: str) -> int:
    url = f"{AKAUNTING_URL}/api/contacts"
    r = requests.get(url, headers=_headers(), auth=_auth(),
                     params={**_params(), "search": email})
    r.raise_for_status()
    results = r.json().get("data", [])
    for c in results:
        if c.get("email") == email:
            return c["id"]

    payload = {
        "type": "customer",
        "name": name,
        "email": email,
        "company_id": AKAUNTING_COMPANY_ID,
        "enabled": True,
    }
    r = requests.post(url, headers=_headers(), auth=_auth(),
                      params=_params(), json=payload)
    r.raise_for_status()
    return r.json()["data"]["id"]

def create_invoice(customer_id: int, order: dict, items: list) -> dict:
    from datetime import datetime

    issued_at = datetime.utcfromtimestamp(order["created_timestamp"]).strftime("%Y-%m-%d")

    invoice_items = []
    for item in items:
        price = item["price"]["amount"] / item["price"]["divisor"]
        invoice_items.append({
            "name": item["title"],
            "quantity": item["quantity"],
            "price": price,
        })

    payload = {
        "type": "invoice",
        "company_id": AKAUNTING_COMPANY_ID,
        "contact_id": customer_id,
        "issued_at": issued_at,
        "due_at": issued_at,
        "currency_code": order["total_price"]["currency_code"],
        "items": invoice_items,
        "notes": f"Etsy order #{order['receipt_id']}",
    }

    url = f"{AKAUNTING_URL}/api/invoices"
    r = requests.post(url, headers=_headers(), auth=_auth(),
                      params=_params(), json=payload)
    r.raise_for_status()
    return r.json()["data"]