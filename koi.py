import requests
import os
from urllib.parse import urlparse

# Base URL pattern from the provided link
base_url = "https://prd-content.static.game.nogikoi.jp/assets/img/card/l/"
start_id = 17113620  # Starting ID from your URL
end_id = start_id - 1000  # Adjust this to go further back (e.g., start_id - 5000 for more)

# Chrome-like User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Create a downloads folder if it doesn't exist
os.makedirs("nogikoi_cards", exist_ok=True)

def download_card(id_num):
    url = f"{base_url}{id_num}.jpg"
    filename = f"nogikoi_cards/card_{id_num:08d}.jpg"  # Padded to 8 digits for consistency
    
    try:
        # Quick HEAD request to check existence, with UA
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            # Full GET to download if it exists, with UA
            img_response = requests.get(url, headers=headers, timeout=10)
            if img_response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded: {url} -> {filename}")
                return True
            else:
                print(f"Failed to download (status {img_response.status_code}): {url}")
        else:
            print(f"Skipped (not found, status {response.status_code}): {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking/downloading {url}: {e}")
    return False

# Download in descending order
for card_id in range(start_id, end_id - 1, -1):
    download_card(card_id)

print("Download attempt complete!")