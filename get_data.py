import time
import csv

from utils import get_data

URL = 'https://divar.ir'

COLUMNS = [
    'url', 'title', 'area', 'construct_date', 'rooms', 'has_elevator',
    'has_parking', 'has_warehouse', 'type', 'city', 'floor', 'price_per_meter',
    'price'
]

with open('divar_apartments.txt', 'r', encoding='utf-8') as f:
  links = f.readlines()
print(f'number of links: {len(links)}')

i = 0


def main():
  global i

  with open('divar_apartments.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file,
                            fieldnames=COLUMNS,
                            delimiter=',',
                            lineterminator='\n')
    writer.writeheader()

    for link in links:
      print(f'i = {i}')
      link = link.strip()
      data = get_data(f'{URL}{link}')

      writer.writerow(data)

      time.sleep(1)
      print(f'{link} scraped.')

      i += 1


if __name__ == '__main__':
  t1 = time.time()
  main()
  t2 = time.time()
  print(f'Execution Time: {t2 - t1}')