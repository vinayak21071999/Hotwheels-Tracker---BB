import requests
import json
import os
import time

# ---- CONFIG ----
# BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")

BOT_TOKEN = "8795237106:AAGiDvm-l4w8MDmDXzX0XntjFo52OMHo5_0"
CHAT_ID = "530289659"

STATE_FILE = "bb_state.json"

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
    "subaru", "suzuki", "tesla", "toyota", "volkswagen", "volvo", "Wagons"
]

# --- Paste your FRESH cookie string here (from an incognito capture) ---
BB_COOKIES_STR = '_bb_locSrc=default; x-channel=web; _bb_vid=MTM1NDI1MjQyMjY3NjcyNDIwNg==; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=Io7uw7ZujUitJrmSfIp19eMA56J9gAPmXk9VyjDxBOwIYYaEy7qHdLVfGqwTtICk; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; _is_tobacco_enabled=1; _is_bb1.0_supported=0; is_integrated_sa=1; is_subscribe_sa=0; bb2_enabled=true; csurftoken=P98Xnw.MTM1NDI1MjQyMjY3NjcyNDIwNg==.1784786937453.SnmLRAjrr+ej/u958qd0fsq/fD6mFmD3/ZCG1ShKFJI=; bigbasket.com=1b32f553-6b96-49ee-8982-de28b22bb786; ufi=1; jarvis-id=9ea21de7-ef23-4f5a-8164-9d327eba6eac; _bb_lat_long="MTIuMzMwNzczOXw3Ni42MDM3MjIxOTk5OTk5OQ=="; _bb_cid=10; _bb_aid="MzE5Njc2MjE5NA=="; is_global=0; _bb_addressinfo=MTIuMzMwNzczOXw3Ni42MDM3MjIxOTk5OTk5OXxIaW5rYWx8NTcwMDE3fEh1dGFnYWxsaXwxfGZhbHNlfHRydWV8dHJ1ZXxCaWdiYXNrZXRlZXI=; _bb_pin_code=570017; _bb_sa_ids=21290; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjIxMjkw'

BB_COOKIES = dict(item.split("=", 1) for item in BB_COOKIES_STR.split("; "))

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


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def matches_watchlist(name: str) -> bool:
    name_lower = name.lower()
    return any(b in name_lower for b in BRANDS)



def fetch_page_with_retry(url, max_retries=4):
    delay = 5
    for attempt in range(max_retries):
        resp = requests.get(url, headers=BB_HEADERS, cookies=BB_COOKIES, timeout=15)

        if resp.status_code == 429:
            print(f"Rate limited (attempt {attempt + 1}/{max_retries}), waiting {delay}s...")
            time.sleep(delay)
            delay *= 2  # exponential backoff: 5s, 10s, 20s, 40s
            continue

        resp.raise_for_status()
        return resp.json()

    raise Exception(f"Failed after {max_retries} retries due to repeated rate limiting")


def fetch_bigbasket_hotwheels():
    all_products = []
    page = 1
    while True:
        url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug=hot%20wheels&page={page}&bucket_id=6"

        data = fetch_page_with_retry(url)
        products = data["tabs"][0]["product_info"]["products"]

        if not products:
            break

        all_products.extend(products)
        print(f"Page {page}: {len(products)} products")

        if len(products) < 20:
            break

        page += 1
        if page > 20:
            print("Hit safety page cap (20) - stopping pagination")
            break

        time.sleep(4)  # increased pacing between pages

    return all_products


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
    send_telegram("✅ Test message - tracker is alive")
    previous = load_state()
    current = {}

    try:
        products = fetch_bigbasket_hotwheels()
    except Exception as e:
        print(f"Error fetching BigBasket results: {e}")
        return

    for p in products:
        pid = p["id"]
        name = p["desc"]
        in_stock = is_in_stock(p)
        url = f"https://www.bigbasket.com{p['absolute_url']}"
        is_watchlist = matches_watchlist(name)

        current[pid] = {"name": name, "in_stock": in_stock}
        prev_entry = previous.get(pid)

        # Trigger 1: brand new listing never seen before
        if prev_entry is None:
            tag = " ⭐ (matches your watchlist)" if is_watchlist else ""
            send_telegram(f"🆕 New Hot Wheels listing{tag}:\n{name}\n{url}")

        # Trigger 2 & 3: was out of stock, now in stock
        elif prev_entry["in_stock"] is False and in_stock is True:
            if is_watchlist:
                send_telegram(f"⭐ Watchlist item back in stock:\n{name}\n{url}")
            else:
                send_telegram(f"🔔 Back in stock:\n{name}\n{url}")

    save_state(current)
    print(f"Checked {len(products)} products. State saved.")


if __name__ == "__main__":
    main()