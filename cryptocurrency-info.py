import json
import logging
import os
from datetime import datetime
from typing import List, Optional

import requests

logging.basicConfig(level=logging.INFO)

NUM_ID_MAX = 1000

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

def get_infos(ids: List[int]) -> Optional[str]:
  assert len(ids) <= NUM_ID_MAX
  url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id={",".join( [str(x) for x in ids])}'
  # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id=1,1027,825'
  HEADERS = {
      'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY'],
      'Accept': 'application/json',
      'Accept-Charset': 'utf-8',
      'Accept-Encoding': 'deflate, gzip',
  }
  resp = requests.get(url=url, headers=HEADERS)
  if resp.status_code != 200:
    logging.error(f'resp.status_code is not 200')
    return None
  data = resp.json()
  if data['status']['error_code'] != 0:
    logging.error(f'error_code is not 0')
    return None
  return json.dumps(data, indent=2)

def get_ids() -> List[int]:
  today = datetime.utcnow().isoformat()[:10]
  coin_list_file = f'./data/cryptocurrency-list-{today}.json'
  with open(coin_list_file, 'rt') as f:
    data = json.load(f)
    coin_list = data['data']['cryptoCurrencyList']
    return [x['id'] for x in coin_list]

if __name__ == "__main__":
  today = datetime.utcnow().isoformat()[:10]
  today_file = f'./data/cryptocurrency-info-{today}.json'
  today_obj = {}
  if os.path.exists(today_file):
    with open(today_file, 'rt') as f:
      today_obj = json.load(f)

  ids = get_ids()
  i = 0
  while i < len(ids):
    text = get_infos(ids[i: i+NUM_ID_MAX])
    if text:
      obj = json.loads(text)
      today_obj['status'] = obj['status']
      today_obj['data'].update(obj['data'])
    i += NUM_ID_MAX

  # Sort keys based on the ids list
  sorted_dict = [(str(id), today_obj['data'][str(id)]) for id in ids]
  today_obj['data'] = dict(sorted_dict)
  with open(today_file, 'wt') as f:
    json.dump(today_obj, f, indent=2)
