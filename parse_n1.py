import requests
from bs4 import BeautifulSoup
import re

from models import Apartments


class NoneObject:

    def __init__(self):
        self.text = "Не указано"


def _parse_item(item, *params):
    result = item.find(*params)
    if result is None:
        return NoneObject()
    return result


def parse_floor(line):
    """Парсит строку вида '2 / 4 этажи' в отельные перменные

    :param line: входная строка
    :return (floor, floors): этаж, этажность дома
    """
    try:
        _line = line.replace(" ", "")
        floor, floors = _line.split("/")
        floor = int("".join((re.findall(r'\d+', floor))))
        floors = int("".join((re.findall(r'\d+', floors))))
    except Exception:
        return 0, 0
    return floor, floors


def parse_float_value(line, default=0):
    _line = line.replace(" ", "")
    result = re.findall(r'\d*\.\d+|\d+', _line)
    if not result:
        return default
    return float(result[0])


def parse_addr(line):
    rooms = line[:line.find(",")]
    addr = line[line.find(","):]
    rooms = int("".join((re.findall(r'\d+', rooms))))
    addr = addr.lstrip(",").strip()
    return rooms, addr


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

            rooms, addr = parse_addr(addr.text)

            area = parse_float_value(area.text)
            floor, floors = parse_floor(floor.text)
            price = parse_float_value(price.text)
            sqm = parse_float_value(sqm.text)

            identical_float = list(
                Apartments.select().where((Apartments.city == city.text)
                                          & (Apartments.addr == addr)
                                          & (Apartments.floor == floor)
                                          & (Apartments.rooms == rooms))
            )
            if len(identical_float) > 0:
                print(f"Поропустим {city.text}, {addr}")
                continue

            row = Apartments(
                city=city.text.replace(",", "").strip(),
                district=district.text,
                addr=addr,
                area=area,
                floor=floor,
                number_of_floors=floors,
                material=material.text,
                price=price,
                sqm=sqm,
                rooms=rooms
            )
            row.save()
            print(", ".join(map(str, [city.text, district.text, addr, f"{rooms} комнат"])))
            print(", ".join(map(str, [area, f"{floor} этаж из {floors}", material.text, price, sqm])))

        return bool(items)
    return False


base_url = "https://kazan.n1.ru/kupit/kvartiry/"
is_page = True
param = ""
index_page = 1
while is_page:
    print(f"PAGE: {index_page}")
    is_page = parse_page(url=base_url + param)
    index_page += 1
    param = f"?page={index_page}"

