# import re
import requests
from bs4 import BeautifulSoup
import time

URL = 'https://divar.ir/s/karaj'
APARTMENT = 'buy-apartment'
VILLA = 'buy-villa'

QUERY = 'price=-1200000000'

def get_items(url, type, page=1):
  request = requests.get(f'{url}/{type}?{QUERY}&page={page}')
  soup = BeautifulSoup(request.txt, 'html.parser')
  items = soup.find_all('div', attrs={
      'class': 'waf972 wbee95 we9d46',
  })
  
  # return 24 items per page
  return items


i = 1


def main():
  global i
  with open('divar_villa_links.txt', 'w', encoding='utf-8') as links_file:
    try:
      while True:
        items = get_items(URL, VILLA, i)

        # 404 page
        if items == []:
          print(f'No items on page {i}')
          break

        for item in items:
          for div in item.div:
            href = div.get('href')
            links_file.write(f'{href}\n')

        i += 1
        time.sleep(1)
        print(f'Page {i-1} scraped.')
    except requests.exceptions.ConnectionError as e:
      print('Connection Error:', e)
      time.sleep(15)
      main()

if __name__ == '__main__':
  t1 = time.time()
  main()
  t2 = time.time()
  print(f'Execution Time: {t2 - t1}')
