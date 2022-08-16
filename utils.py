from bs4 import BeautifulSoup
import requests

P2E_map = {
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',
    '۰': '0',
    '٬': ''
}


def p2e(text):
  for key, value in P2E_map.items():
    text = text.replace(key, value)
  return int(text)


def get_data(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  # with open('test.html', 'w', encoding='utf-8') as f:
  #   f.write(soup.prettify())

  # with open('test.html', 'r', encoding='utf-8') as f:
  #   soup = BeautifulSoup(f.read(), 'html.parser')
  # with open('test2.html', 'w', encoding='utf-8') as f:
  title = soup.find('div', attrs={'class': 'kt-page-title__title kt-page-title__title--responsive-sized'}).text
  shit = soup.find_all('span', attrs={'class': 'kt-group-row-item__value'})
  area = (shit[0].contents[0])
  area = p2e(area)
  construct_date = (shit[1].contents[0])
  construct_date = p2e(construct_date)
  rooms = (shit[2].contents[0])
  rooms = p2e(rooms)
  has_elevator = (shit[3].contents[0])
  has_parking = (shit[4].contents[0])
  has_warehouse = (shit[5].contents[0])

  shit2 = soup.find_all('p', attrs={'class': 'kt-unexpandable-row__value'})
  price = shit2[0].contents[0].split('تومان')[0].strip()
  price = p2e(price)
  price_per_meter = shit2[1].contents[0].split('تومان')[0].strip()
  price_per_meter = p2e(price_per_meter)
  floor = shit2[3].contents[0].split(' ')[0]
  floor = p2e(floor)

  type = soup.find_all('a', attrs={'class': 'kt-breadcrumbs__link'})[2].text
  city = soup.find('div', attrs={'class': 'kt-page-title__subtitle kt-page-title__subtitle--responsive-sized'}).text,
  city = city[0].split('|')[0].split('،')[1]

  data = {
    'title': title,
    'area': area,
    'construct_date': construct_date,
    'rooms': rooms,

    'price': price,
    'price_per_meter': price_per_meter,
    'floor': floor,

    'has_elevator': False if 'ندارد' in has_elevator else True,
    'has_parking': False if 'ندارد' in  has_parking else True,
    'has_warehouse': False if 'ندارد' in  has_warehouse else True,

    'type': type,
    'city': city,

    'url': url
  }

  return data
