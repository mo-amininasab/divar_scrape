# import re
import requests
from bs4 import BeautifulSoup
import time

URL = 'https://divar.ir/s/karaj'
APARTMENT = 'buy-apartment'
VILLA = 'buy-villa'

QUERY = 'price=-1900000000'


def get_items(url, type, page=1):
  request = requests.get(f'{url}/{type}?{QUERY}&page={page}')
  soup = BeautifulSoup(request.text, 'html.parser')
  items = soup.find_all('div', attrs={
      'class': 'waf972 wbee95 we9d46',
  })

  # return 24 items per page
  return items


i = 1


def main():
  global i
  with open('links/divar_apartment_links.txt', 'w', encoding='utf-8') as links_file:
    try:
      while True:
        items = get_items(URL, APARTMENT, i)

        # 404 page
        if items == []:
          print(f'No items on page {i}')
          break

        for item in items:
          href = item.a['href']

          if href == None:
            print('No href')
            break

          link = f'https://divar.ir{href}'
          links_file.write(f'{link}\n')
          print(f'Page {i} - {link}')

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
  print(f'Execution Time: {(t2 - t1) / 60} minutes.')
