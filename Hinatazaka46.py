import requests
import bs4
import time
import re
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


html = requests.get("https://hinatazaka46.com/s/official/search/artist").content
soup = bs4.BeautifulSoup(html, features="lxml")
li_list = soup.find_all("div", class_="sort-default")[0].find_all("li")
for i in range(len(li_list)):
    img = li_list[i].find_all("img")[0]
    print(img)
    link = img["src"]
    link = "/".join(link.split("/")[:-1]) + ".jpg"
    # Assuming li_list[i].text is a string
    text = li_list[i].text

    # Split the text into lines, remove empty lines, and strip whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Replace multiple spaces with a single space in each line
    cleaned_lines = [re.sub(r"\s+", " ", line) for line in lines]

    # Join the cleaned lines back into a single string
    cleaned_text = "\n".join(cleaned_lines)
    print(cleaned_text)
    # Now cleaned_text contains the desired output
    # send_telegram_photo(
    #     f"{i+1}/{len(li_list)}" + "\n" + cleaned_text + "\n" + link,
    #     link,
    # )
    send_telegram_file_link(
        f'<a href="{link}">{i+1}/{len(li_list)}</a>' + "\n" + cleaned_text + "\n",
        link,
    )
