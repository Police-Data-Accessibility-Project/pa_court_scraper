import random
import time

import requests

from SimpleCache import SimpleCache
from insert_into_mongodb import insert_into_mongodb

BASE_URL = "https://services.pacourts.us/public/v1/cases/"


def get_docket_number_info(docket_number):
    url = f"{BASE_URL}{docket_number}"
    # Spoof the user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://pdap.io/",
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def get_docket_numbers() -> list[str]:
    with open("data/docket_numbers_from_yesterday.txt", "r") as f:
        docket_numbers = f.read().splitlines()
        return docket_numbers

if __name__ == "__main__":

    cache = SimpleCache()
    if cache.is_empty():
        docket_numbers = get_docket_numbers()
        for docket_number in docket_numbers:
            cache.set(docket_number, False)

    for key in cache.get_keys():
        if cache.get(key):
            continue

        try:
            print(f"Processing docket number: {key}", flush=True)
            content = get_docket_number_info(key)
            insert_into_mongodb(content)
        except Exception as e:
            cache.save_to_file()
            raise e
        cache.set(key, True)
        random_wait_time = random.randint(5, 15)
        print(f"Sleeping for {random_wait_time} seconds", flush=True)
        time.sleep(random_wait_time)


