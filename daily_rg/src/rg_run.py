import requests
from datetime import datetime
from pathlib import Path

# Çıktı dosyası
OUTPUT = Path("daily_rg/output/daily_rg.md")

# Resmi Gazete ana sayfası
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

    OUTPUT.write_text(
        f"📅 {today} RESMİ GAZETE RAPORU\n\n"
        "Bugünün Resmi Gazetesi yayımlanmıştır.\n"
        "(Detaylı fihrist bir sonraki adımda eklenecektir.)",
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
