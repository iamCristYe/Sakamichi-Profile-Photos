import requests
import os

TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


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


def send_telegram_file(caption, file_name):
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            files = {"document": open(file_name, "rb")}
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption,
            }

            response = requests.post(url, data=payload, files=files)
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


# Example usage
# send_telegram_photo("Test Caption", "https://example.com/image.jpg")

import time
import subprocess
import json
import datetime

src = (
    requests.get("https://www.nogizaka46.com/s/n46/api/list/member")
    .text.replace("res(", "")
    .replace(");", "")
)
with open("member.json", "w") as f:
    result = json.loads(src)
    json.dump(result, f, ensure_ascii=False, indent=2)
send_telegram_file("", "member.json")
with open("member.json") as t:
    a = json.load(t)
    current_members = []
    for i in range(len(a["data"])):
        member = a["data"][i]
        if member["graduation"] == "NO" and member["name"] != "乃木坂46":
            current_members.append(member)

    for i in range(len(current_members)):
        member = current_members[i]
        caption = (
            f'<a href="{member["img"]}">{i+1}/{len(current_members)}</a>'
            + "\n"
            + member["name"]
            + "\n"
            + member["english_name"].upper()
            + "\n"
            + member["kana"]
        )
        print(caption, member["img"])

        if member["graduation"] == "NO":
            # send_telegram_photo(
            #     caption,
            #     member["img"] + "?" + str(datetime.datetime.now()),
            # )
            send_telegram_file_link(
                caption,
                member["img"] + "?" + str(datetime.datetime.now()),
            )
