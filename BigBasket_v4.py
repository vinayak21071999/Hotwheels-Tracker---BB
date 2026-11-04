import requests
from curl_cffi import requests as cffi_requests
import json
import os
import time

# ---- CONFIG ----
# BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")

#actual
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# #hard code
# BOT_TOKEN = "8795237106:AAGiDvm-l4w8MDmDXzX0XntjFo52OMHo5_0"
# CHAT_ID = "530289659"


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
BB_COOKIES_STR = os.environ["BB_COOKIES"]
# BB_COOKIES_STR = '_bb_locSrc=default; x-channel=web; _bb_vid=MTM1MzM1OTY4MzE1MDI5MTk1MA==; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=lwzZWgIEWUT8jZxm2Lodxctyeipy6SmWy9SYtwx6L9mmnmpDrDO0FgDg3h8oYbhm; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; _is_tobacco_enabled=1; _is_bb1.0_supported=0; is_integrated_sa=1; is_subscribe_sa=0; bb2_enabled=true; bigbasket.com=f97cbec8-d376-471f-b393-02c33cf23944; jarvis-id=963cc806-7091-4109-b978-a84c4e2b7573; ufi=1; is_global=0; _bb_visaddr=; _bb_cid=10; _bb_aid="MzE5Njc2MjE5NA=="; _bb_lat_long="MTIuMzQ0MDQyMjE0MzkwMTZ8NzYuNjEzNjM5OTY1NjUzNDI="; _bb_addressinfo=MTIuMzQ0MDQyMjE0MzkwMTZ8NzYuNjEzNjM5OTY1NjUzNDJ8SGViYmFsIDJuZCBTdGFnZXw1NzAwMTd8TXlzb3JlfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=570017; _bb_sa_ids=21290,38297; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjIxMjkwLDM4Mjk3; _is_now_ec_serviceable=0; _sa_band_cache_key=; _bb_member_class=; _bb_exchange_info=MzE0OTkyNTYxNA==; csurftoken=i443HA.MTM1MzM1OTY4MzE1MDI5MTk1MA==.1793637918132.//cCb3FbWMuP9cPqHJJjYURvcVhMFT6UR6mnf2W7K7M=; bm_sz=26D467A7DB320C886D1C353503D3FD1F~YAAQCozQF3r1iHyhAQAAwKkmnQH0YPg8CHw4zo+OHZIcjENd/JcIh219mzmz9CXz0t+Z/n35D2hhALLz3wlYZWn7rSNGh8vTS5a95bw3iX+C/Ayy7hYZWsbX0XfxpbAX5vrCEmZkH9AGdUhcV6DsyVIyPw9BXcMUNj8XOV0x7+DSOO4joqIUTEBobvpGHxNrHltds/l5gHnlpJH5d1Iiea6u8h0Fo1+rd+VjGq+40x0o2HEKZWXDfttv4y5y/gIB00zBAXRaZr73kqN1DAj1uBNoayZm2orAXjSCdGwZpFJYcda61iFRVsrqeMq7Mlh/w6TeAL8XVVEFtwdlga3wdDR/4NRRROsa0aVAr3WwM11V061RRyzqve+CJcm/3vQ0s37TmAkhAhgeWpemMuZlroxKdcccgTN1Uj+AQCGoJAretQjEvYhszU1DUWFMM7ES~3552067~3487028; _gcl_au=1.1.735758076.1793637924; adb=0; _fbp=fb.1.1793637924852.286775691432793703; _ga=GA1.2.1220988747.1784733730; _gid=GA1.2.1206900404.1793637925; _abck=6E4F9D7685A2D308038324FA38B1E965~0~YAAQCozQFyYEiXyhAQAAMCYnnRA8vBtB1mB6Dck4RZgbc2UKu/OcwyrCA46LJOmefh3VTFZzAQViKZhBK5vSKfjEvNLP9jIhN7J69LdQDTEW6WKdRY9FmardzRXY4xVkJlWo4/HVitYHIm+WqxNgYdxOLh0hqMecppNCYK1QHAM1UkmEFA3VW+UEILutreLEoWGJLvO41kMZZ02wurOzWDpRdsSSpWWGSp6BCK/5l/+rejSqf6JqVV+8u8F7Kbm8+J0shCSExmJDUucNmBJz0FV1eOFNWZ0fsezcpI4AHdCCkztcTPsuUWB+m+DEykSr1PI4dgc9Zbf/9WO2mX5qtmtXOzcIA2nXXJ3XFCyma1Nr+4OPYa5Kk3+WeBjXc8iggK0NMJhQcUReKA1os26SrHWoQdMko+WsETtwyxxdz2RSjOmqena6kDNEoFMD8WoPd4ES/VRx1LY4Ye9bs7atu3j+ABfW0OaqLpLH1DqxSmQLLWZL9P6P5UauCYYM9yO+t/0o9rO86PdTY8WDOzNKXC9hmXO/uWptT7hGzOYIi3TxGcJM2tnko67XQWuG94vmAZ+3s4R4pYTKIx3lmzezwByGQmySrX+ugDOS2VEJ6uTOhUx3CmYzKIdc5MQpHHwi/87EpKPMcDms5ng61+5jevskaqwDVDzwChfWkY/LOWnjWdl31cjrQc4RbA==~-1~-1~1793641519~AAQAAAAG%2f%2f%2f%2f%2fyPqgEbICKKXLnxaY3IJ02niBWR9qEdUfWgRbRqJEwbSU%2fEevZsNZqzR9PDk7iwCucXzqKgLqBeRHkbRilflu8H1VlUJhLZy%2fJI+~-1; ts=2026-11-02%2022:15:55.048; _ga_FRRYG5VKHX=GS2.1.s1793637924$o5$g1$t1793637958$j26$l0$h0; bm_s=YAAQCozQFxCQiXyhAQAAUJornQacadt5QTpZPOoaZeClDOW7VOZAOz6uezVs1YS/YpduH6rTdM7i1oXcncUSTp7r+Q3tn0DysgdT2ae7VgG8rzx5A9OaUj6fODYKm3wGou7Ls0Wl97W/4ZtMcFEYiwsLkQbclKz0HbH5e/Jx5SNkJPjqVraeFqdcRalFfn2DGZBDFRI2+5bWfNavNtmm5h4k3aK1+tCBwr2pUsIHmsMQedZd3FGM1mJG1GcolQonTV8oyEp5IXUo5LnnDd03Q1x8TWpkEpLN0Qp0dO0rKnp+QXKTI+H17/rKjdQoIotl+T5bdh7CLJdpbePVcTt4XtxAysIurc/4irW0aOEFz9w1vOXQnjb7Sc6F0P745m6lEVcBJWpWE4wBza6hPaHIh4wVvZAFK+wYoCJP2bhLYZncsePgHF5xuKJqZrTJIEeQasbRioAL/thL9diFQDEGf8DM3dFJLIUbevkdV3iMTUvp9B8TTA5Mj/j1DQf+d84RhHXiJvKrU1iK6lpyDmANTqPY7Og9LMKFggaLgU+odNbyLoTK2WrP3/J1GyXTRCy2nd9Xi76w8Y9YRD7uTc46CbNPDWo9ZqZlZYSg8jsUK4ofzUqcj4MA0zwnDXy40Dn7wYKXGT1LRBGM0X9GK0VYIwzjvOLLf4b/A1bwtU2D5A3xaFvlCNtdvAOo7hf57evSkrgewnKaSl7MnXPfcf8QPxRmSdhGKbwsTfode1mADFKSCEQPQ+oMnO5e1Pw/HpRZjo3fKAmy7r55XOH2AVu5a5ay2pDpLMGodRM+xmTlrbTQEbXbauf0HjsC09Ab1/C9AF7TmENsjlZpwMSVBz4Plv/5JqpuNNUng/QsvYtJOouNQzexNXFmPM2kobCE3b7yBEYdNuG8idQ1QvgUFSodeqHWWfcIDtR1LoPjMbl+ovrw2sP/Aj+hiU6/tCHmDI5Uk8Mt400Czfty+9u7offORTX++CXT7cIiU4Lcw5Qspb/2Nbnhi4aTw5Dtk0SWYandIUGo6EL7eh4Iajz+b4XwgDYCQZj9UxZA/SmYfXvW8fXOrdjggs/0qN2uc9yulgw0FW/yqNiQiqgVPYmN3YTF45bKK1pq+INxptgs/iVwZPVZsvQHjgQaY5LPXBqnsK9/tUTFkuXGRqGdhUwdRPLeCuICqjI0X0/SkB19GrVlB/uH; bm_so=60D29A568A91B7A880E39A04F72C76CB578E4DEEF57BB8CC6E3681BC995B11A3~YAAQCozQFxKQiXyhAQAAUJornQmRaE88R7goUbYjcYOle3t1+aF0T3AGJ7WV6KlpLOzkT5s4c9Wm3v6kfvzC3sz8xG3eFqf758sivnNRfCzcxWpsc+JZjcX0XeHyJ9Op/4+1g8hylgWhwqusBhzt+UXhLolPG5suHkIJTY7RypoIf2ElTDcHdJ1d5RTweOe04XwXat3s0aWyvMcZyHs2q/WZRooO7theSDFD9S81s4VIUSFyU6MM1q1e/VMbm8O9gCIrAdtjOftTSLZqvKI2cWviZRDbIm0HjK+wyAsA3rQ1okBxCWqYkBawPVVkLT7jrSCvOQS24IkJl2g3TWIlcLQT/w7XKu51tPnXOjr/l2+47hrMCKbywZ7KzGe2t9kSpsDuMDd2TlCt1DJvVSL76PXOi7cTPqMRJSuU6Vd3NduVZrHDhjiCcHzQzX+RCl0uYnLrO/aA79kykbwc6WiDscsCH60jD68jTQddb7d6txJkPKxSvO85ieGh6LVC8AMLzl+CsNQhLA==~2; bm_lso=60D29A568A91B7A880E39A04F72C76CB578E4DEEF57BB8CC6E3681BC995B11A3~YAAQCozQFxKQiXyhAQAAUJornQmRaE88R7goUbYjcYOle3t1+aF0T3AGJ7WV6KlpLOzkT5s4c9Wm3v6kfvzC3sz8xG3eFqf758sivnNRfCzcxWpsc+JZjcX0XeHyJ9Op/4+1g8hylgWhwqusBhzt+UXhLolPG5suHkIJTY7RypoIf2ElTDcHdJ1d5RTweOe04XwXat3s0aWyvMcZyHs2q/WZRooO7theSDFD9S81s4VIUSFyU6MM1q1e/VMbm8O9gCIrAdtjOftTSLZqvKI2cWviZRDbIm0HjK+wyAsA3rQ1okBxCWqYkBawPVVkLT7jrSCvOQS24IkJl2g3TWIlcLQT/w7XKu51tPnXOjr/l2+47hrMCKbywZ7KzGe2t9kSpsDuMDd2TlCt1DJvVSL76PXOi7cTPqMRJSuU6Vd3NduVZrHDhjiCcHzQzX+RCl0uYnLrO/aA79kykbwc6WiDscsCH60jD68jTQddb7d6txJkPKxSvO85ieGh6LVC8AMLzl+CsNQhLA==~2~1793638246084'



BB_COOKIES = dict(item.split("=", 1) for item in BB_COOKIES_STR.split("; ") if "=" in item)

BB_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "common-client-static-version": "101",
    "content-type": "application/json",
    "osmos-enabled": "true",
    "x-channel": "BB-WEB",
    "x-entry-context": "bbnow",
    "x-entry-context-id": "10",
    "x-integrated-fc-door-visible": "false",
}


def send_telegram(message: str, retries=3) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for attempt in range(retries):
        try:
            r = requests.post(
                url,
                data={"chat_id": CHAT_ID, "text": message, "disable_web_page_preview": True},
                timeout=15,
            )
            if r.status_code == 429:
                wait = r.json().get("parameters", {}).get("retry_after", 5)
                time.sleep(wait + 1)
                continue
            if r.ok:
                return True
            print(f"Telegram error {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"Telegram send failed (attempt {attempt + 1}): {e}")
            time.sleep(3 * (attempt + 1))
    return False

def send_alerts(alerts):
    # Combine alerts into messages under Telegram's 4096-character limit
    chunk = ""
    for a in alerts:
        if len(chunk) + len(a) + 2 > 3900:
            send_telegram(chunk)
            time.sleep(2)
            chunk = ""
        chunk += a + "\n\n"
    if chunk:
        send_telegram(chunk)

def matches_watchlist(name: str) -> bool:
    name_lower = name.lower()
    return any(b in name_lower for b in BRANDS)



def fetch_page_with_retry(url, max_retries=4):
    delay = 5
    for attempt in range(max_retries):
        resp = cffi_requests.get(url, headers=BB_HEADERS, cookies=BB_COOKIES, impersonate="chrome", timeout=15)

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
        url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug=hot%20wheels&page={page}&bucket_id=19"

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
    previous = load_state()
    first_run = len(previous) == 0

    try:
        products = fetch_bigbasket_hotwheels()
    except Exception as e:
        print(f"Error fetching BigBasket results: {e}")
        send_telegram(f"⚠️ Tracker failed: {e}")
        raise SystemExit(1)

    current = {}
    alerts = []

    for p in products:
        pid = p["id"]
        name = p["desc"]
        in_stock = is_in_stock(p)
        url = f"https://www.bigbasket.com{p['absolute_url']}"
        is_watchlist = matches_watchlist(name)

        current[pid] = {"name": name, "in_stock": in_stock}
        prev_entry = previous.get(pid)

        if prev_entry is None:
            tag = "⭐ " if is_watchlist else ""
            stock = "in stock" if in_stock else "out of stock"
            alerts.append(f"🆕 {tag}New listing ({stock}):\n{name}\n{url}")
        elif prev_entry["in_stock"] is False and in_stock is True:
            tag = "⭐ Watchlist item" if is_watchlist else "🔔"
            alerts.append(f"{tag} Back in stock:\n{name}\n{url}")

    # Save state BEFORE sending, so a Telegram failure can't cause a repeat flood
    save_state(current)

    if first_run:
        send_telegram(f"✅ Tracker initialised with {len(products)} products. Alerts start from the next run.")
        return

    if alerts:
        send_alerts(alerts)
    print(f"Checked {len(products)} products, {len(alerts)} alerts.")


if __name__ == "__main__":
    main()
