import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers)

    with open("index.html", "w") as file:
        file.write(r.text)

    data_dict, count = [], 0

    for i in range(0, 90, 30):
        # get hotels urls
        r = requests.get("https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most&hotel_link=/hotel/id/%HOTEL_ID%&r=705114833&s={i}", headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        hotels_cards = soup.find_all("div", class_="hotel_card_dv")

        for hotel_url in hotels_cards:
            hotel_url = "https://www.tury.ru" + hotel_url.find("a").get("href")
            data_dict.append(hotel_url)
            count += 1
            print(f"#{count}: {hotel_url} is done!")

    with open("hrefs.txt", "w") as file:
        for line in data_dict:
            file.write(line + '\n')


def main():
    get_data("https://www.tury.ru/hotel/most_luxe.php")


if __name__ == '__main__':
    main()