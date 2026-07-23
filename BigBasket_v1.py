import requests
import json
import os
from datetime import datetime

# ---- CONFIG ----
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")

BRANDS = [
    "abarth", "acura", "alfa romeo", "aston martin", "audi", "bentley",
    "bmw", "bugatti", "buick", "cadillac", "chevrolet", "chrysler",
    "citroën", "citroen", "dodge", "ferrari", "fiat", "ford", "genesis",
    "gmc", "honda", "hummer", "hyundai", "infiniti", "isuzu", "jaguar",
    "jeep", "kia", "koenigsegg", "lamborghini", "lancia", "land rover",
    "lexus", "lincoln", "lotus", "lucid", "maserati", "mazda", "mclaren",
    "mercedes", "mercedes-benz", "mg", "mini", "mitsubishi", "nissan",
    "opel", "pagani", "peugeot", "plymouth", "pontiac", "porsche", "ram",
    "renault", "rivian", "rolls-royce", "rolls royce", "saab", "shelby",
    "subaru", "suzuki", "tesla", "toyota", "volkswagen", "volvo"
]

BB_COOKIES = {
    "_bb_locSrc": "default",
    "_bb_nhid": "7427",
    "_bb_dsid": "7427",
    "_bb_dsevid": "7427",
    "csrftoken": "REPLACE_WITH_FRESH_VALUE",
    "isintegratedsa": "true",
    "jentrycontextid": "10",
    "xentrycontextid": "10",
    "xentrycontext": "bbnow",
    "_bb_bb2.0": "1",
    "_is_tobacco_enabled": "1",
    "_is_bb1.0_supported": "0",
    "is_integrated_sa": "1",
    "is_subscribe_sa": "0",
    "bb2_enabled": "true",
    "_bb_lat_long": '"MTIuMzMwNzczOXw3Ni42MDM3MjIxOTk5OTk5OQ=="',
    "_bb_cid": "10",
    "is_global": "0",
    "_bb_addressinfo": "MTIuMzMwNzczOXw3Ni42MDM3MjIxOTk5OTk5OXxIaW5rYWx8NTcwMDE3fEh1dGFnYWxsaXwxfGZhbHNlfHRydWV8dHJ1ZXxCaWdiYXNrZXRlZXI=",
    "_bb_pin_code": "570017",
    "_bb_sa_ids": "21290",
    "_bb_cda_sa_info": "djIuY2RhX3NhLjEwLjIxMjkw",
}

BB_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "common-client-static-version": "101",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-channel": "BB-WEB",
    "x-entry-context": "bbnow",
    "x-entry-context-id": "10",
}

STATE_FILE = "bb_state.json"


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def matches_watchlist(name: str) -> bool:
    name_lower = name.lower()
    return any(b in name_lower for b in BRANDS)


def fetch_bigbasket_hotwheels(page=1):
    url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug=hot%20wheels&page={page}&bucket_id=6"
    resp = requests.get(url, headers=BB_HEADERS, cookies=BB_COOKIES, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data["tabs"][0]["product_info"]["products"]


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_in_stock(product) -> bool:
    avail = product.get("availability", {})
    return avail.get("button") == "Add" and not avail.get("not_for_sale", False)


def main():
    previous = load_state()
    current = {}

    try:
        products = fetch_bigbasket_hotwheels(page=1)
    except Exception as e:
        print(f"Error fetching BigBasket results: {e}")
        return

    for p in products:
        pid = p["id"]
        name = p["desc"]
        in_stock = is_in_stock(p)
        url = f"https://www.bigbasket.com{p['absolute_url']}"

        current[pid] = {"name": name, "in_stock": in_stock}
        prev_entry = previous.get(pid)

        # Trigger 1: new item never seen before
        if prev_entry is None:
            send_telegram(f"🆕 New Hot Wheels listing:\n{name}\n{url}")
            if in_stock and matches_watchlist(name):
                send_telegram(f"⭐ New + in stock + matches watchlist:\n{name}\n{url}")

        # Trigger 2: restock (was out of stock, now in stock)
        elif prev_entry["in_stock"] is False and in_stock is True:
            send_telegram(f"🔔 Back in stock:\n{name}\n{url}")

        # Trigger 3: watchlist match currently in stock (catch on every run, not just transitions)
        if in_stock and matches_watchlist(name) and prev_entry is not None:
            # only alert once per stock period, not every run — reuse restock logic above covers the transition case
            pass

    save_state(current)
    print(f"Checked {len(products)} products. State saved.")


if __name__ == "__main__":
    main()