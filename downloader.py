import os
import asyncio
import aiohttp

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


def get_bearer_token():
  url = 'https://oauth.battle.net/token'

  payload = 'grant_type=client_credentials'
  headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
  auth = HTTPBasicAuth(os.getenv('BLIZZARD_CLIENT_ID'), os.getenv('BLIZZARD_CLIENT_SECRET'))

  response = requests.request('POST', url, headers=headers, data=payload, auth=auth)
  json_response = response.json()

  return json_response['access_token']


def get_battlegrounds_cards(token, query):
  url = 'https://api.blizzard.com/hearthstone/cards'
  headers = { 'Authorization': f'Bearer {token}'}
  params = {
    'gameMode': 'battlegrounds',
    'pageSize': '450',
    'locale': 'en_US',
    'sort': 'tier:asc,name:asc',
    **query
  }

  response = requests.request('GET', url, params=params, headers=headers)
  json_response = response.json()
  return json_response['cards']


async def download_image(session, url, save_path):
  os.makedirs(os.path.dirname(save_path), exist_ok=True)
  async with session.get(url) as response:
    content = await response.read()
    with open(save_path, 'wb') as f:
      f.write(content)


async def download_cards(cards, prefix):
  async with aiohttp.ClientSession() as session:
    tasks = []
    for card in cards:
      card_img_url = card['battlegrounds']['image']
      card_img_name = card['slug']
      tasks.append(download_image(session, card_img_url, f'out/{prefix}/{card_img_name}.jpg'))
    await asyncio.gather(*tasks)


async def fetch_cards(token, query):
  print(f'Downloading {query} cards...')
  prefix = '/'.join(query.values())
  cards = get_battlegrounds_cards(token, query)
  await download_cards(cards, prefix)

async def fetch_all_cards(token):
  queries = [
    { 'bgCardType': 'minion', 'tier': '1' },
    { 'bgCardType': 'minion', 'tier': '2' },
    { 'bgCardType': 'minion', 'tier': '3' },
    { 'bgCardType': 'minion', 'tier': '4' },
    { 'bgCardType': 'minion', 'tier': '5' },
    { 'bgCardType': 'minion', 'tier': '6' },
    { 'bgCardType': 'minion', 'tier': '7' },
    { 'bgCardType': 'trinket', 'spellSchool': 'lesser_trinket' },
    { 'bgCardType': 'trinket', 'spellSchool': 'greater_trinket' },
    { 'bgCardType': 'spell' },
    { 'bgCardType': 'hero' },
    { 'bgCardType': 'quest' },
    { 'bgCardType': 'reward' },
    { 'bgCardType': 'anomaly' },
  ]

  for query in queries:
    await fetch_cards(token, query)


if __name__ == '__main__':
  load_dotenv()
  token = get_bearer_token()

  # query = { 'bgCardType': 'spell' }
  # asyncio.run(fetch_query(token, query))

  asyncio.run(fetch_all_cards(token))
