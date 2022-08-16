# import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

URL = 'https://divar.ir/s/karaj'
APARTMENT = 'buy-apartment'
VILLA = 'buy-villa'

def get_items(url, type, page=1):
  request = requests.get(f'{url}/{type}?price=-1200000000&page={page}')
  soup = BeautifulSoup(request.txt, 'html.parser')
  items = soup.find_all('div', attrs={
      'class': 'waf972 wbee95 we9d46',
  })
  return items


i = 1


def main():
  global i
  with open('divar_villas.txt', 'w', encoding='utf-8') as f:
    try:
      while True:
        items = get_items(URL, VILLA, i)
        if items == []:
          print(f'No items on page {i}')
          break

        for item in items:
          for div in item.div:
            href = div.get('href')
            f.write(f'{href}\n')

        i += 1
        sleep = random.uniform(1, 3)
        time.sleep(sleep)
        print(f'Page {i-1} scraped. sleeping for {sleep} seconds')
    except requests.exceptions.ConnectionError as e:
      print('Error:', e)
      time.sleep(15)
      main()

if __name__ == '__main__':
  main()
