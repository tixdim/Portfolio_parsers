import requests
from bs4 import BeautifulSoup
import json
import datetime

page, count, data_dict = 1, 0, []
now = datetime.datetime.now()

while True:
    r = requests.get(f"https://stopgame.ru/review/new/izumitelno/p{page}")
    html = BeautifulSoup(r.content, "html.parser")
    items = html.select(".items > .article-summary")

    if len(items):
        for el in items:
            title = el.select(".caption > a")[0].text.replace(": Обзор", "")
            title = title.replace("ö", "o")

            comm = el.select(".info > .info-item > a")[0].text.replace("\n", "")

            if el.select(".info > span")[0].text.strip()[-1] == ".":
                date_comm = el.select(".info > span")[0].text
            else:
                date_comm = el.select(".info > span")[0].text + " " + str(now.year) + "."

            href = "https://stopgame.ru" + el.select(".caption > a")[0].get("href")

            data = {
                'title': title,
                'href': href,
                'date_comm': date_comm,
                'comm': comm
            }
            count += 1
            print(f'#{count}: {title} is done!')

            data_dict.append(data)

            with open('data.json', 'w') as json_file:
                json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

        page += 1
    else:
        break