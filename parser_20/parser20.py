#!/usr/bin/python
# -*- coding: utf8 -*-

import csv
from bs4 import BeautifulSoup
import requests


def save(comp):
    with open("pars_info.txt", "a", encoding="utf-8") as file:
        file.write(f"{comp['title']} -> Price: {comp['price']} -> Link: {comp['link']}\n")


def parse():
    URL = "https://www.olx.kz/elektronika/kompyutery-i-komplektuyuschie/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8, "
                  "application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36"
    }

    responce = requests.get(URL, headers=headers)
    soup = BeautifulSoup(responce.content, "html.parser")
    items = soup.findAll("div", class_="offer-wrapper")
    comps = []

    with open("pars_info.csv", 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Название', 'Цена', 'Ссылка'])

    for item in items:
        if item.find("a", class_="thumb vtop inlblk rel tdnone linkWithHash linkWithHashPromoted scale4 detailsLink"):
            comps.append({
                "title": item.find("a", class_="thumb vtop inlblk rel tdnone linkWithHash linkWithHashPromoted scale4 detailsLink").find("img").get("alt"),
                "price": item.find("p", class_="price").get_text(strip=True),
                "link": item.find("a", class_="thumb vtop inlblk rel tdnone linkWithHash linkWithHashPromoted scale4 detailsLink").get("href")
            })
        else:
            comps.append({
                "title": item.find("a", class_="marginright5 link linkWithHash detailsLink").get_text(strip=True),
                "price": item.find("p", class_="price").get_text(strip=True),
                "link": item.find("a", class_="marginright5 link linkWithHash detailsLink").get("href")
            })

        for comp in comps:
            save(comp)

        with open("pars_info.csv", 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=',')
            for item in comps:
                writer.writerow([item['title'], item['price'], item['link']])


if __name__ == "__main__":
    parse()