#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import requests
from bs4 import BeautifulSoup
import csv
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
           'accept': '*/*'}

session = requests.Session()
HOST = 'http://mir-priaji.ru/'
r = session.get(HOST, headers=HEADERS)


def get_html(url, params=None):
    t = session.get(url, headers=HEADERS, params=params)
    return t


def get_html2(url, params=None):
    d = session.get(url, headers=HEADERS, params=params)
    return d


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        paginationTo = max(list(map(int, soup.find('div', class_='nums').text.split())))
    except Exception:
        paginationTo = 1
    return paginationTo


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item_block col-4 col-md-3 col-sm-6 col-xs-6')
    catalog = []

    for item in items:
        title = item.find('a', class_='dark_link').get_text(strip=True)
        kategory = soup.find('h1', id='pagetitle').get_text(strip=True)

        PageImageHref = str(HOST) + str(item.find('a').get('href'))

        html2 = get_html2(PageImageHref)
        soup2 = BeautifulSoup(html2.text, 'html.parser')

        try:
            items2 = soup2.find('li', class_='current')
            bb = HOST + str(items2.find('link').get('href'))[1:]
            if not bb:
                bb = ""
        except Exception:
            bb = ""

        items3, text = soup2.find('div', class_='detail_text'), ""

        if items3:
            try:
                text = str(items3.get_text).split("\n")

                for i in range(len(text)):
                    text[i] = text[i].replace('<bound method Tag.get_text of <div class="detail_text">', "")\
                        .replace('<br/>', "").replace('</div>>', "")\
                        .replace('<bound method PageElement.get_text of <div class="detail_text">', "")\
                        .replace('\xa0', "")
                text = " ".join(text)

            except UnicodeEncodeError:
                print("Oops, an unexpected error has occurred..")

        elif items3 is None:
            text = ""
        else:
            text = ''

        catalog.append({
            'title': title,
            'kategory': kategory,
            'image': bb,
            'kol-vo': item.find('span', class_='value').get_text(strip=True),
            'text': text
        })
    return catalog


def save_file(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Категории', 'Имя', 'Изображения', 'Описание'])
        for item in items:
            writer.writerow([item['kategory'], item['title'], item['image'], item['text']])


def parse():
    for URL in [
        'https://mir-priaji.ru/personal/'
    ]:
        html = get_html(URL)
        if html.status_code == 200:
            catalog = []
            soup = BeautifulSoup(html.text, "html.parser")
            item_url = HOST + soup.find_all("a", text=re.compile("НАБОРЫ ДЛЯ ВЫШИВАНИЯ"))[-1].get('href')

            html = get_html(item_url)

            pages_count = get_pages_count(html.text)

            for page in range(1, pages_count + 1):
                print(f'Парсинг страницы {page} {pages_count} {f"https://mir-priaji.ru/catalog/vyshivanie_1/nabory_dlya_vyshivaniya/?PAGEN_1={page}"}')
                html = get_html(item_url, params={'PAGEN_1': page})
                catalog.extend(get_content(html.text))
                time.sleep(1)

            FILE = 'All_sets.csv'
            save_file(catalog, FILE)

            print(f'Получено {len(catalog)} товаров')
        else:
            print('Error')


if __name__ == "__main__":
    parse()