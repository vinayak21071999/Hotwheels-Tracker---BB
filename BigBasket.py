import requests

url = 'https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug=hot%20wheels&page=1&bucket_id=6'

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'common-client-static-version': '101',
    'content-type': 'application/json',
    'osmos-enabled': 'true',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'x-channel': 'BB-WEB',
    'x-entry-context': 'bbnow',
    'x-entry-context-id': '10',
    'x-integrated-fc-door-visible': 'false',
    'x-tracker': '1ccd36cf-1c4a-4bb2-a936-9181511cf48c',
}

cookies_str = '_bb_locSrc=default; x-channel=web; _bb_vid=MTM1NDI1MjQyMjY3NjcyNDIwNg==; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=Io7uw7ZujUitJrmSfIp19eMA56J9gAPmXk9VyjDxBOwIYYaEy7qHdLVfGqwTtICk; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; _is_tobacco_enabled=1; _is_bb1.0_supported=0; is_integrated_sa=1; is_subscribe_sa=0; bb2_enabled=true; csurftoken=P98Xnw.MTM1NDI1MjQyMjY3NjcyNDIwNg==.1784786937453.SnmLRAjrr+ej/u958qd0fsq/fD6mFmD3/ZCG1ShKFJI=; bigbasket.com=1b32f553-6b96-49ee-8982-de28b22bb786; ufi=1; jarvis-id=9ea21de7-ef23-4f5a-8164-9d327eba6eac; _bb_lat_long="MTIuMzMwNzczOXw3Ni42MDM3MjIxOTk5OTk5OQ=="; _bb_cid=10; _bb_aid="MzE5Njc2MjE5NA=="; is_global=0; _bb_addressinfo=MTIuMzMwNzczOXw3Ni42MDM3MjIxOTk5OTk5OXxIaW5rYWx8NTcwMDE3fEh1dGFnYWxsaXwxfGZhbHNlfHRydWV8dHJ1ZXxCaWdiYXNrZXRlZXI=; _bb_pin_code=570017; _bb_sa_ids=21290; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjIxMjkw'

cookies = dict(item.split("=", 1) for item in cookies_str.split("; "))

resp = requests.get(url, headers=headers, cookies=cookies)

print("Status code:", resp.status_code)
print(resp.text[:1500])