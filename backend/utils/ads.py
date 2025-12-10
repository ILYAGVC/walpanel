import requests


def get_ads_from_github() -> dict:
    url = "https://raw.githubusercontent.com/primeZdev/whale-panel/Refactor/media/ads.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        ads_data = response.json()
        return ads_data
    except (requests.RequestException, ValueError):
        return {
            "title": "جایگاه آگهی شما",
            "text": "کسب‌وکار خود را به بقیه افراد معرفی کنید! اینجا می‌توانید تبلیغ ویژه خود را قرار دهید",
            "link": "https://t.me/primezdev",
            "button": "رزرو جایگاه آکهی",
        }
