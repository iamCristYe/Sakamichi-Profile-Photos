import requests
import bs4
import time
import os

TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


def send_telegram_photo(caption, img_url):
    while True:
        try:
            print(caption)
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


html = requests.get("https://sakurazaka46.com/s/s46/search/artist").content
soup = bs4.BeautifulSoup(html, features="lxml")
for i in range(len(soup.find("main").find_all("img"))):
    img = soup.find("main").find_all("img")[i]
    print(img)
    if not img["src"]:
        continue 
    link = "https://www.sakurazaka46.com" + img["src"]
    link = "/".join(link.split("/")[:-1]) + ".jpg"
    print(img["alt"])
    # send_telegram_photo(
    #     f'{i+1}/{len(soup.find("main").find_all("img"))}'
    #     + "\n"
    #     + img["alt"]
    #     + "\n"
    #     + link,
    #     link,
    # )
    send_telegram_file_link(
        f'<a href="{link}">{i+1}/{len(soup.find("main").find_all("img"))}</a>'
        + "\n"
        + img["alt"],
        link,
    )
