import json
import requests
from bs4 import BeautifulSoup as BS

users, data_dict = [
    ["tixdim.on1@gmail.com", "B7W2ax33)"],
    ["nikitasofarov@gmail.com", "test123"]
], []

for i in range(len(users)):
    with requests.Session() as s:
        # get CSRF
        auth_html = s.get("https://smartprogress.do/")
        auth_bs = BS(auth_html.content, "html.parser")
        csrf = auth_bs.select("input[name=YII_CSRF_TOKEN]")[0]["value"]

    # do login
    payload = {
        "YII_CSRF_TOKEN": csrf,
        "returnUrl": "/",
        "UserLoginForm[email]": users[i][0],
        "UserLoginForm[password]": users[i][1],
        "UserLoginForm[rememberMe]": 0
    }

    answer = s.post("https://smartprogress.do/user/login/", data=payload)
    answer_bs = BS(answer.content, "html.parser")

    name, lvl, exp = answer_bs.select(".user-menu__name")[0].text.strip(), \
                     answer_bs.select(".user-menu__info-text--lvl")[0].text.strip(), \
                     answer_bs.select(".user-menu__info-text--exp")[0].text.strip()

    lvl, exp = int(lvl[:lvl.index(" ")]), exp[:exp.index(" ")]

    data = {
        'Name': name,
        'Lvl': lvl,
        'Exp': exp
    }

    data_dict.append(data)
    print(f'#{i + 1}: {answer_bs.select(".user-menu__name")[0].text.strip()} is done!')

    with open('data.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)