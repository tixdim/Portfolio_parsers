import json
import random
import re
from time import sleep
from bs4 import BeautifulSoup
import requests
import csv

url = "http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)

with open("index.html", "r", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

all_categories_dict = {}
for i in all_products_hrefs:
    i_text = i.text
    i_href = "http://health-diet.ru" + i.get("href")
    # print(f"{i_text}: {i_href}")

    all_categories_dict[i_text] = i_href

with open("all_categories_dict.json", "w", encoding="utf-8") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False) # indent - отступ, ensure_ascii - кодирует

with open("all_categories_dict.json", encoding="utf-8") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():
    rep = [" ", ",", "-", "'"]
    for i in rep:
        if i in category_name:
            category_name = category_name.replace(i, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # собираем заголовки таблицы
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # собираем данные продуктов
    product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []

    for i in product_data:
        product_tds = i.find_all("td")

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[1].text
        fats = product_tds[1].text
        carbohydrates = product_tds[1].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Итерация {count}. {category_name} записан...")
    iteration_count -= 1

    if iteration_count == 0:
        print("Работа закончена")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2, 4))