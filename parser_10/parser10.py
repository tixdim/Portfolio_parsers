#!/usr/bin/python
# -*- coding: utf8 -*-

import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv


start_time = time.time()


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Наличие на складе"
            )
        )

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36"
    }

    url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

    books_data = []
    for page in range(1, pages_count + 1):
        url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
                if book_title == "":
                    book_title = "Нет названия книги"
            except:
                book_title = "Нет названия книги"

            try:
                book_author = book_data[1].text.strip()
                if book_author == "":
                    book_author = "Нет автора"
            except:
                book_author = "Нет автора"

            try:
                book_publishing = book_data[2].find_all("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
                if book_publishing == "":
                    book_publishing = "Нет издательства"
            except:
                book_publishing = "Нет издательства"

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
                if book_new_price == "":
                    book_new_price = "Нет нового прайс"
            except:
                book_new_price = "Нет нового прайса"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
                if book_old_price == "":
                    book_old_price = "Нет старого прайса"
            except:
                book_old_price = "Нет старого прайса"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
                if book_sale == "":
                    book_sale = "Нет скидки"
            except:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text.strip()
                if book_status == "":
                    book_status = "Нет статуса"
            except:
                book_status = "Нет статуса"

            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )

            with open(f"labirint_{cur_time}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )

        print(f"Обработана {page}/{pages_count}")
        time.sleep(1)

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == '__main__':
    main()