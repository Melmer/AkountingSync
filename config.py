import os
from dotenv import load_dotenv

load_dotenv()

ETSY_API_KEY = os.getenv("ETSY_API_KEY")
ETSY_ACCESS_TOKEN = os.getenv("ETSY_ACCESS_TOKEN")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID")

AKAUNTING_URL = os.getenv("AKAUNTING_URL")
AKAUNTING_EMAIL = os.getenv("AKAUNTING_EMAIL")
AKAUNTING_PASSWORD = os.getenv("AKAUNTING_PASSWORD")
AKAUNTING_COMPANY_ID = int(os.getenv("AKAUNTING_COMPANY_ID", 1))