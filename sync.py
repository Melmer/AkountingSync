import logging
from db import init_db, is_synced, mark_synced
from etsy_client import get_orders, get_order_transactions
from akaunting_client import find_or_create_customer, create_invoice

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("sync.log"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger(__name__)

def sync():
    init_db()
    orders = get_orders()
    log.info(f"{len(orders)} orders fetched from Etsy")

    for order in orders:
        order_id = str(order["receipt_id"])

        if is_synced(order_id):
            log.info(f"Order {order_id} already synced, skipped")
            continue

        try:
            # Klant
            name = order["name"]
            email = order["buyer_email"]
            customer_id = find_or_create_customer(name, email)

            # Items
            items = get_order_transactions(order_id)

            # Factuur
            invoice = create_invoice(customer_id, order, items)
            mark_synced(order_id)
            log.info(f"Order {order_id} → Akaunting invoice #{invoice['document_number']}")

        except Exception as e:
            log.error(f"Error with order {order_id}: {e}")

if __name__ == "__main__":
    sync()