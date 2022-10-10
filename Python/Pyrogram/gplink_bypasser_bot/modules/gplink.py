import cloudscraper
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
async def gplinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = {'referer': ref_url}
    res = client.get(url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = {input.get('name'): input.get('value') for input in inputs}

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/', '/')
    except:
        return 'Something went wrong :('

    return res.json()['url'].replace('\/', '/')