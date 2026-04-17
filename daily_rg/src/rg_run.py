import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

OUTPUT = Path("daily_rg/output/daily_rg.md")
RG_URL = "https://www.resmigazete.gov.tr/eskiler"

def main():
    today = datetime.now().strftime("%d.%m.%Y")

    try:
        r = requests.get(RG_URL, timeout=30)
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

    # Fihrist başlıklarını çek
    titles = []
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if text:
            titles.append(text)

    report = [
        f"📅 {today} RESMİ GAZETE RAPORU",
        "",
        "(Durum: Bugünün Resmi Gazetesi yayımlanmıştır.)",
        "",
        "A. GÜNLÜK FİHRİST (TAM LİSTE)",
        ""
    ]

    for t in titles:
        report.append(f"* {t}")

    OUTPUT.write_text("\n".join(report), encoding="utf-8")

if __name__ == "__main__":
    main()
