import requests
from bs4 import BeautifulSoup

from models import Apartments


class NoneObject:

    def __init__(self):
        text = "Не указано"


def _parse_item(item, *params):
    result = item.find(*params)
    if result is None:
        return NoneObject()
    return result


def parse_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_doc = BeautifulSoup(response.text, features='html.parser')
        items = html_doc.find_all('div', {'class': 'living-search-item', 'data-test': 'offers-list-item'})

        for item in items:
            city = _parse_item(item, 'span', {'class': 'living-list-card-city-with-estate__item'})
            district = _parse_item(item, 'div', {'class': 'search-item-district'})
            addr = _parse_item(item, 'span', {'class': 'link-text'})
            area = _parse_item(item, 'div', {'class': 'living-list-card__area'})
            floor = _parse_item(item, 'span', {'class': 'living-list-card-floor__item'})
            material = _parse_item(item, 'div', {'class': 'living-list-card__material'})
            price = _parse_item(item, 'div', {'class': 'living-list-card-price__item _object'})
            sqm = _parse_item(item, 'div', {'class': 'living-list-card-price__item _per-sqm'})
            print(", ".join([city.text, district.text, addr.text]))
            print(", ".join([area.text, floor.text, material.text, price.text, sqm.text]))
            # TODO - Числовые значения спарсить как числа, а не текст
            # row = Apartments(
            #     city=city,
            #     district=district,
            #     addr=addr,
            #     area=area,
            #     floor=floor,
            #     material=material,
            #     price=price,
            #     sqm=sqm
            # )
            # row.save()
        return True
    return False


base_url = "https://kopeysk.n1.ru/kupit/kvartiry/"
is_page = True
param = ""
index_page = 1
while is_page:
    print(f"PAGE: {index_page}")
    is_page = parse_page(url=base_url + param)
    index_page += 1
    param = "?" + str(index_page)

