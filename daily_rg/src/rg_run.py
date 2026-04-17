import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import yaml

# Çıktı dosyası
OUTPUT = Path("daily_rg/output/daily_rg.md")

# Legalbank Resmi Gazete fihristi
FIHRIST_URL = "https://legalbank.net/belgebank/resmi-gazete-fihristi"

# Tarayıcı gibi görünmek için header
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def main():
    today_dt = datetime.now()
    today_numeric = today_dt.strftime("%d.%m.%Y")

    aylar = {
        "01": "Ocak",
        "02": "Şubat",
        "03": "Mart",
        "04": "Nisan",
        "05": "Mayıs",
        "06": "Haziran",
        "07": "Temmuz",
        "08": "Ağustos",
        "09": "Eylül",
        "10": "Ekim",
        "11": "Kasım",
        "12": "Aralık",
    }

    today_tr = f"{today_dt.strftime('%d')} {aylar[today_dt.strftime('%m')]} {today_dt.strftime('%Y')}"

    # Legalbank fihristine eriş
    try:
        response = requests.get(FIHRIST_URL, headers=HEADERS, timeout=30)
    except Exception:
        OUTPUT.write_text(
            f"📅 {today_numeric} RESMİ GAZETE RAPORU\n\n"
            "Legalbank fihristine erişilemedi.",
            encoding="utf-8"
        )
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Sayfanın tamamında bugünkü tarihi ara
    page_text = soup.get_text(separator=" ", strip=True)

    if today_numeric not in page_text and today_tr not in page_text:
        OUTPUT.write_text(
            f"📅 {today_numeric} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete henüz bugünün fihristini yayımlamadı.",
            encoding="utf-8"
        )
        return

    # Fihrist başlıklarını al
    titles = []
    for li in soup.select("ul li"):
        text = li.get_text(strip=True)
        if text:
            titles.append(text)

    # Anahtar kelimeleri yükle
    with open("daily_rg/rules/ceei_keywords.yaml", "r", encoding="utf-8") as f:
        keywords = yaml.safe_load(f)["keywords"]

    matches = []
    for title in titles:
        for kw in keywords:
            if kw.lower() in title.lower():
                matches.append(title)
                break

    # Raporu oluştur
    report = [
        f"📅 {today_numeric} RESMİ GAZETE RAPORU",
        "",
        "(Durum: Legalbank Resmi Gazete fihristi üzerinden doğrulanmıştır.)",
        "",
        "A. GÜNLÜK FİHRİST (TAM LİSTE)",
        ""
    ]

    for t in titles:
        report.append(f"* {t}")

    report.append("")
    report.append("B. ÇEEİ KAPSAMINDA TESPİTLER")
