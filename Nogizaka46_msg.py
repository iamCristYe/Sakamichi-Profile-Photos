import requests
import os
import json
import time
import datetime

TELEGRAM_CHAT_ID = "-"
TELEGRAM_BOT_TOKEN = ":"


def send_telegram_photo(caption, img_url):
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "document": img_url,
                "caption": caption,
            }

            response = requests.post(url, json=payload)
            response_body = response.json()
            if "error_code" not in response_body:
                time.sleep(0)
                return
        except Exception as e:
            print(e)
            time.sleep(5)
            pass


headers = {

}

for group_num in range(0, 101):
    group_id = f"{group_num:02d}"
    url = f"https://api.message.nogizaka46.com/v2/groups/{group_id}/members"
    
    try:
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch group {group_id}: {response.status_code}")
            continue
        
        members = response.json()
        if not members:
            print(f"No members in group {group_id}")
            continue
        
        for member in members:
            member_id = member["id"]
            name = member["name"]
            birthday = member["birthday"]
            
            # Check if today is birthday (month and day)
            today = datetime.date.today()
            bday = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
            is_birthday = (today.month, today.day) == (bday.month, bday.day)
            
            if is_birthday:
                print(f"Sending images for {name} (ID: {member_id}) - Birthday today!")
            else:
                print(f"Sending images for {name} (ID: {member_id})")
            
            # Thumbnail
            thumbnail_url = member["thumbnail"]
            caption_thumb = f"{name} (ID: {member_id})\nBirthday: {birthday}\nThumbnail"
            if is_birthday:
                caption_thumb += f"\n🎉 Happy Birthday! 🎉"
            send_telegram_photo(caption_thumb, thumbnail_url)
            
            # Phone Image
            phone_url = member["phone_image"]
            caption_phone = f"{name} (ID: {member_id})\nBirthday: {birthday}\nPhone Image"
            if is_birthday:
                caption_phone += f"\n🎉 Happy Birthday! 🎉"
            send_telegram_photo(caption_phone, phone_url)
            
            time.sleep(1)  # Short delay between sends
        
        time.sleep(1)  # Delay between groups
    except Exception as e:
        print(f"Error processing group {group_id}: {e}")
        time.sleep(5)