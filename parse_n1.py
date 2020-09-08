import requests
from bs4 import BeautifulSoup


response = requests.get("https://kopeysk.n1.ru/kupit/kvartiry/")

if response.status_code == 200:
    html_doc = BeautifulSoup(response.text, features='html.parser')
    items = html_doc.find_all('div', {'class': 'living-search-item', 'data-test': 'offers-list-item'})

    for item in items:
        city = item.find('span', {'class': 'living-list-card-city-with-estate__item'})
        district = item.find('div', {'class': 'search-item-district'})
        addr = item.find('span', {'class': 'link-text'})
        area = item.find('div', {'class': 'living-list-card__area'})
        floor = item.find('span', {'class': 'living-list-card-floor__item'})
        material = item.find('div', {'class': 'living-list-card__material'})
        price = item.find('div', {'class': 'living-list-card-price__item _object'})
        sqm = item.find('div', {'class': 'living-list-card-price__item _per-sqm'})
        print(", ".join([city.text, district.text, addr.text]))
        print(", ".join([area.text, floor.text, material.text, price.text, sqm.text]))







