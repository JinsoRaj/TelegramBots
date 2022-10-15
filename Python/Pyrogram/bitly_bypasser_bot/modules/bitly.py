import requests
#bit_ly
async def bit_ly(url):
    payload = {
        "url": url,
    }

    r = requests.post("https://api.bypass.vip/", data=payload)
    data = r.json()
    return data["destination"]
