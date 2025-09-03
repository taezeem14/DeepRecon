import json

def save_report(data):
    # JSON Report
    with open("reports/results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Markdown Report
    with open("reports/report.md", "w", encoding="utf-8") as f:
        f.write("# DeepRecon Report\n\n")
        for item in data:
            f.write(f"## {item['url']}\n")
            f.write(f"- Emails: {', '.join(item['emails'])}\n")
            f.write(f"- BTC: {', '.join(item['btc'])}\n")
            f.write(f"- PGP Keys: {len(item['pgp'])}\n\n")
