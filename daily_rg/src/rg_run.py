import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import yaml

OUTPUT = Path("daily_rg/output/daily_rg.md")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def get_rg_url(today):
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%Y%m%d")
    return f"https://www.resmigazete.gov.tr/eskiler/{year}/{month}/{day}.htm"
    
def main():
    today_dt = datetime.now()
    today = today_dt.strftime("%d.%m.%Y")
    rg_url = get_rg_url(today_dt)

    try:
        r = requests.get(rg_url, headers=HEADERS, timeout=30)
    except Exception:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete sitesine erişilemedi.",
            encoding="utf-8"
        )
        return

    if r.status_code != 200:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Bugünün Resmi Gazetesi henüz yayımlanmamıştır.",
            encoding="utf-8"
        )
        return


    soup = BeautifulSoup(r.text, "html.parser")

    titles = []
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if text:
            titles.append(text)

