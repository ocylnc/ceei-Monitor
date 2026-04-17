import feedparser
from datetime import datetime, date
from pathlib import Path
import yaml

OUTPUT = Path("daily_rg/output/daily_rg.md")
RSS_URL = "https://www.resmigazete.gov.tr/rss.xml"

def main():
    today = date.today()
    today_str = today.strftime("%d.%m.%Y")

    feed = feedparser.parse(RSS_URL)

    # GERÇEK KRİTER: entry var mı?
    if not feed.entries:
        OUTPUT.write_text(
            f"📅 {today_str} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete RSS içeriği alınamadı (boş feed).",
            encoding="utf-8"
        )
        return

    today_entries = []

    for entry in feed.entries:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            pub_date = date(
                entry.published_parsed.tm_year,
                entry.published_parsed.tm_mon,
                entry.published_parsed.tm_mday,
            )
            if pub_date == today:
                today_entries.append(entry)

    if not today_entries:
        OUTPUT.write_text(
            f"📅 {today_str} RESMİ GAZETE RAPORU\n\n"
            "Resmi Gazete henüz bugünün içeriğini yayımlamadı.",
            encoding="utf-8"
        )
        return

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
``
