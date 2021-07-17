import logging
from datetime import datetime
from typing import Optional

import requests

logging.basicConfig(level=logging.INFO)

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

def get_total_count()->Optional[int]:
  url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=1&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false'
  resp = requests.get(url=url, headers=HEADERS)
  if resp.status_code != 200:
    logging.error(f'resp.status_code is not 200')
    return None
  data = resp.json()
  if data['status']['error_code'] != '0':
    logging.error(f'error_code is not 0')
    return None
  return data['data']['totalCount']

def get_all_coins(limit: int = 6000)->Optional[str]:
  # see https://coinmarketcap.com/all/views/all/
  url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={limit}&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false'
  resp = requests.get(url=url, headers=HEADERS)
  if resp.status_code != 200:
    logging.error(f'resp.status_code is not 200')
    return None
  if resp.json()['status']['error_code'] != '0':
    logging.error(f'error_code is not 0')
    return None
  return resp.text

if __name__ == "__main__":
  total_count = get_total_count()
  if total_count:
    txt = get_all_coins(limit=total_count)
    if txt:
      today = datetime.utcnow().isoformat()[:10]
      with open(f'./data/cryptoCurrencyList-{today}.json', "wt") as f:
        f.write(txt + "\n")
