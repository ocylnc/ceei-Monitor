import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import yaml

OUTPUT = Path("daily_rg/output/daily_rg.md")
RG_URL = "https://www.resmigazete.gov.tr/eskiler"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def main():
    today = datetime.now().strftime("%d.%m.%Y")

    try:
        r = requests.get(RG_URL, headers=HEADERS, timeout=30)
    except Exception:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete sitesine erişilemedi.",
            encoding="utf-8"
        )
        return

    if today not in r.text:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete henüz bugünün fihristini yayımlamadı.",
            encoding="utf-8"
        )
        return

    soup = BeautifulSoup(r.text, "html.parser")

    titles = []
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if text:
            titles.append(text)

