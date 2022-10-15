#linkvertise bypass
import requests
async def lv_bypass(url):
    payload = {
        "url": url,
    }

    r = requests.post("https://api.bypass.vip/", data=payload)
    data = r.json()
    return data["destination"]

