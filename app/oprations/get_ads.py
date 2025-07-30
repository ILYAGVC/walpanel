import requests
from datetime import datetime, timedelta


ADS_URL = "https://raw.githubusercontent.com/primeZdev/walpanel/master/media/ads.json"

ads_cache = {
    "data": None,
    "updated_at": datetime.min
}

async def get_ads():
    now = datetime.now()

    if now - ads_cache["updated_at"] > timedelta(minutes=60):
        res = requests.get(url=ADS_URL)

        if res.status_code == 200:
            ads_cache["data"] = res.json()
            ads_cache["updated_at"] = now
        else:
            ads_cache["data"] = {
            "title": "جایگاه آگهی شما",
            "text": "کسب‌وکار خود را به بقیه افراد معرفی کنید! اینجا می‌توانید تبلیغ ویژه خود را قرار دهید",
            "link": "https://t.me/primezdev",
            "button": "رزرو جایگاه"
        }
    return ads_cache["data"]