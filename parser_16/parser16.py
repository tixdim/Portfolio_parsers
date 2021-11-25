#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8, "
              "application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36"
}


def get_articles_urls(url):
    with requests.Session() as session:
        response = session.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('span', class_='navigations').find_all('a')[-1].text)

    articles_urls_list = []

    with requests.Session() as session:
        for page in range(1, pagination_count + 1):
            response = session.get(url=f'https://hi-tech.news/page/{page}/', headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            articles_urls = soup.find_all('a', class_='post-title-a')

            for au in articles_urls:
                art_url = au.get('href')
                articles_urls_list.append(art_url)

            print(f'Обработал {page}/{pagination_count}')

        with open('articles_urls.txt', 'w', encoding="utf-8") as file:
            for url in articles_urls_list:
                file.write(f'{url}\n')

    return 'Работа по сбору ссылок выполнена!'


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]

    urls_count = len(urls_list)
    result_data = []

    with requests.Session() as session:
        # for i, url in enumerate(urls_list[:100]):
        for i, url in enumerate(urls_list):
            response = session.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            article_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
            article_date = soup.find('div', class_='post').find('div', class_='tile-views').text.strip()
            article_img = f"https://hi-tech.news{soup.find('div', class_='post-media-full').find('img').get('src')}"
            article_text = soup.find('div', class_='the-excerpt').text.strip().replace('\n', '')

            result_data.append(
                {
                    'original_url': url,
                    'article_title': article_title,
                    'article_date': article_date,
                    'article_img': article_img,
                    'article_text': article_text
                }
            )
            print(f'Обработал {i + 1}/{urls_count}')

    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    # print(get_articles_urls(url='https://hi-tech.news/'))
    print()
    get_data(file_path='articles_urls.txt')


if __name__ == '__main__':
    main()