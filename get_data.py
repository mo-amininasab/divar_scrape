import requests
import time
import csv

from utils import get_data

URL = 'https://divar.ir'

COLUMNS = [
    'url', 'title', 'area', 'construct_date', 'rooms', 'has_elevator',
    'has_parking', 'has_warehouse', 'type', 'city', 'floor', 'price_per_meter',
    'price'
]

with open('./links/divar_apartment_links.txt', 'r', encoding='utf-8') as f:
  links = f.readlines()

print(f'number of links: {len(links)}')

i = 0


def main():
  global i

  with open('data/divar_apartments.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file,
                            fieldnames=COLUMNS,
                            delimiter=',',
                            lineterminator='\n')
    writer.writeheader()

    while True:
      try:
        link = links[i].strip()
        print(f'link {i+1}: {link}')
      except IndexError:
        print('End of links')
        break
      try:
        data = get_data(link)
        print(f'data: {data}')
      except requests.HTTPError as e:
        print('Error: 404 page')
        i += 1
        continue
      except requests.exceptions.ConnectionError as e:
        print('Connection Error:', e)
        time.sleep(5)
        main()

      writer.writerow(data)
      i += 1
      time.sleep(1)
      print(f'link {i} scraped.')


if __name__ == '__main__':
  t1 = time.time()
  main()
  t2 = time.time()
  print(f'Execution Time: {(t2 - t1) / 60} minutes.')