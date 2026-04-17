import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import yaml

OUTPUT = Path("daily_rg/output/daily_rg.md")
FİHRİST_URL = "https://legalbank.net/belgebank/resmi-gazete-fihristi"

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
        r = requests.get(FİHRİST_URL, headers=HEADERS, timeout=30)
    except Exception:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Legalbank fihristine erişilemedi.",
            encoding="utf-8"
        )
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # Sayfanın üst kısmındaki tarihi al
    header = soup.find("h3")
    if not header:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Fihrist tarihi tespit edilemedi.",
            encoding="utf-8"
        )
        return

    fihrist_date = header.get_text(strip=True)

    if today not in fihrist_date:
        OUTPUT.write_text(
            f"📅 {today} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete henüz bugünün fihristini yayımlamadı.",
            encoding="utf-8"
        )
        return

    # Fihrist maddelerini al
    titles = []
    for li in soup.select("ul li"):
        text = li.get_text(strip=True)
        if text:
            titles.append(text)

    # Anahtar kelimeleri yükle
    with open("daily_rg/rules/ceei_keywords.yaml", "r", encoding="utf-8") as f:
        keywords = yaml.safe_load(f)["keywords"]

    matches = []
    for t in titles:
        for kw in keywords:
            if kw.lower() in t.lower():
                matches.append(t)
                break

    report = [
        f"📅 {today} RESMİ GAZETE RAPORU",
        "",
        "(Durum: Legalbank fihristi üzerinden doğrulanmıştır.)",
        "",
        "A. GÜNLÜK FİHRİST (TAM LİSTE)",
        ""
    ]

    for t in titles:
        report.append(f"* {t}")

    report.append("")
    report.append("B. ÇEEİ KAPSAMINDA TESPİTLER")
    report.append("")

    if not matches:
        report.append("• ÇEEİ kapsamında anahtar kelime eşleşmesi bulunmamıştır.")
    else:
        for m in matches:
            report.append(f"* {m}")

    OUTPUT.write_text("\n".join(report), encoding="utf-8")

if __name__ == "__main__":
    main()
