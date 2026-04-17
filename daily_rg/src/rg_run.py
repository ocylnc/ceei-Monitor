import feedparser
from datetime import datetime
from pathlib import Path
import yaml

OUTPUT = Path("daily_rg/output/daily_rg.md")
RSS_URL = "https://www.resmigazete.gov.tr/rss.xml"

def main():
    today_dt = datetime.now()
    today_str = today_dt.strftime("%d.%m.%Y")

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        OUTPUT.write_text(
            f"📅 {today_str} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete RSS içeriğine erişilemedi.",
            encoding="utf-8"
        )
        return

    # Bugünün kayıtlarını al
    today_entries = []
    for entry in feed.entries:
        published = entry.get("published", "")
        if today_str in published:
            today_entries.append(entry)

    if not today_entries:
        OUTPUT.write_text(
            f"📅 {today_str} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete henüz bugünün içeriğini yayımlamadı.",
            encoding="utf-8"
        )
        return

    # Anahtar kelimeleri yükle
    with open("daily_rg/rules/ceei_keywords.yaml", "r", encoding="utf-8") as f:
        keywords = yaml.safe_load(f)["keywords"]

    titles = [e.title for e in today_entries]

    matches = []
    for title in titles:
        for kw in keywords:
            if kw.lower() in title.lower():
                matches.append(title)
                break

    report = [
        f"📅 {today_str} RESMİ GAZETE RAPORU",
        "",
        "(Durum: Resmi Gazete RSS kaynağı üzerinden doğrulanmıştır.)",
        "",
        "A. GÜNLÜK FİHRİST (RSS)",
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
