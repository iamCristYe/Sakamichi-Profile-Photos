from bs4 import BeautifulSoup
import requests
import os

TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 解析HTML
def parse_html():
    headers = {
        "User-Agent": "curl/8.5.0",
    }
    members_html = requests.get(
        "https://sp.nogizaka46.com/p/members", headers=headers
    ).text
    with open("members.html", "w", encoding="utf-8") as f:
        f.write(members_html)
    # print(members_html)
    # class has to be exactly the same!

    soup = BeautifulSoup(members_html, "lxml").find_all(
        "div", class_="w-contents-main mt-32 2xl:mt-12"
    )[0]
    # print(soup)
    members = []
    for li in soup.find_all("li"):
        member = {}
        a_tag = li.find("a")
        if a_tag:
            member["href"] = a_tag.get("href")
            article = a_tag.find("article")
            if article:
                img_tag = article.find("img")
                if img_tag:
                    member["img_src"] = img_tag.get("src")
                h1_tag = article.find("h1")
                if h1_tag:
                    member["name"] = h1_tag.text.strip()
                span_tag = article.find("span")
                if span_tag:
                    member["nickname"] = span_tag.text.strip()
        members.append(member)
    print(members)
    return members


import time


def send_telegram_photo(caption, img_url):
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "photo": img_url,
                "caption": caption,
            }

            response = requests.post(url, json=payload)
            response_body = response.json()
            if "error_code" not in response_body:
                time.sleep(5)
                return
        except Exception as e:
            print(e)
            time.sleep(5)
            pass


def send_telegram_file_link(caption, file_link):
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption,
                "document": file_link,
                "parse_mode": "HTML",
            }

            file_link = [file_link]
            response = requests.post(url, data=payload)
            response_body = response.json()
            if "error_code" not in response_body:
                time.sleep(5)
                return
        except Exception as e:
            print(e)
            time.sleep(5)
            pass



members = parse_html()
import datetime

for i in range(len(members)):
    member = members[i]
    print(
        f"Name: {member['name']} {member['nickname']}, Image URL: {member['img_src']}, Profile Link: {member['href']}"
    )
    send_telegram_file_link(
        f"<a href=\"{member['img_src']}\">{i+1}/{len(members)}</a>\n{member['name']}\n{member['nickname']}",
        member["img_src"] + f"?{str(datetime.datetime.now())}",
    )
