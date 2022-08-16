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
  request.raise_for_status()
  soup = BeautifulSoup(request.text, 'html.parser')
  # with open('test.html', 'w', encoding='utf-8') as f:
  #   f.write(soup.prettify())

  # with open('test.html', 'r', encoding='utf-8') as f:
  #   soup = BeautifulSoup(f.read(), 'html.parser')
  # with open('test2.html', 'w', encoding='utf-8') as f:
  title = soup.find(
      'div',
      attrs={
          'class':
          'kt-page-title__title kt-page-title__title--responsive-sized'
      }).text

  # finding area, construct_date, rooms
  list1 = soup.find_all('div', attrs={'class': 'kt-group-row-item kt-group-row-item--info-row'})
  area = p2e(list1[0].contents[1].text.strip())
  construct_date = p2e(list1[1].contents[1].text.strip())
  rooms = list1[2].contents[1].text.strip()
  rooms = 0 if 'بدون اتاق' in rooms else  p2e(rooms)

  # finding has_elevator, has_parking, has_warehouse
  list2 = soup.find_all('span', attrs={'class': 'kt-group-row-item__value kt-body kt-body--stable'})
  has_elevator = list2[0].text.strip()
  has_parking = list2[1].text.strip()
  has_warehouse = list2[2].text.strip()


  # finding area, construct_date, rooms, has_elevator, has_parking, has_warehouse
  # list1 = soup.find_all('span', attrs={'class': 'kt-group-row-item__value'})
  # area = (list1[0].text)
  # area = p2e(area)
  # construct_date = (list1[1].text)
  # construct_date = p2e(construct_date)
  # rooms = (list1[2].text)
  # rooms = p2e(rooms)
  # has_elevator = (list1[3].text)
  # has_parking = (list1[4].text)
  # has_warehouse = (list1[5].text)

  # finding price, price_per_meter, floor
  list3 = soup.find_all('div', attrs={'class': 'kt-base-row kt-base-row--large kt-unexpandable-row'})
  price = None
  price_per_meter = None
  floor = None
  for item in list3:
    if 'قیمت کل' in item.contents[0].text:
      price = p2e(item.contents[1].text.split(' ')[0].strip())
    if 'قیمت هر متر' in item.contents[0].text:
      price_per_meter = p2e(item.contents[1].text.split(' ')[0].strip())
    if 'طبقه' in item.contents[0].text:
      if 'همکف' in item.contents[1].text:
        floor = 0
      else:
        floor = p2e(item.contents[1].text.split(' ')[0].strip())

  
  # with open('test2.html', 'w', encoding='utf-8') as f:
  #   print(price, price_per_meter, floor)



  # list3 = soup.find_all('p', attrs={'class': 'kt-unexpandable-row__value'})
  # price = list3[0].contents[0].split('تومان')[0].strip()
  # price = p2e(price)
  # price_per_meter = list3[1].contents[0].split('تومان')[0].strip()
  # price_per_meter = p2e(price_per_meter)
  # floor = list3[3].contents[0].split(' ')[0].strip()
  # floor = p2e(floor)


  type = soup.find_all('a', attrs={'class': 'kt-breadcrumbs__link'})[2].text
  city = soup.find(
      'div',
      attrs={
          'class':
          'kt-page-title__subtitle kt-page-title__subtitle--responsive-sized'
      }).text,
  city = city[0].split('|')[0].split('،')[1].strip()

  data = {
      'url': url,

      'title': title,
      'area': area,
      'construct_date': construct_date,
      'rooms': rooms,
      'price': price,
      'price_per_meter': price_per_meter,
      'floor': floor,
      'has_elevator': False if 'ندارد' in has_elevator else True,
      'has_parking': False if 'ندارد' in has_parking else True,
      'has_warehouse': False if 'ندارد' in has_warehouse else True,
      'type': type,
      'city': city,
  }

  return data
