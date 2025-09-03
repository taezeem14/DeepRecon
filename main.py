from utils.banner import banner
from utils.opsec import opsec_warning
from core.crawler import crawl_recursive
from core.tor_manager import renew_ip
from core.extractor import extract_emails, extract_btc, extract_pgp, search_keyword
from core.report_generator import save_report
from storage.database import init_db, save_result
from config import CRAWL_DEPTH
from colorama import Fore, Style

banner()
opsec_warning()
init_db()

data_report = []

while True:
    print(Fore.GREEN + "\n[1] Crawl Onion Site")
    print("[2] Keyword Search")
    print("[3] Renew Tor IP")
    print("[4] Generate Report")
    print("[5] Exit" + Style.RESET_ALL)
    
    choice = input("> ")

    if choice == "1":
        target = input("Enter .onion URL: ")
        links = crawl_recursive(target, depth=CRAWL_DEPTH)
        print(f"[+] Crawled {len(links)} links")

        emails, btc, pgp = [], [], []

        for link in links:
            html = ""  # Fetch content here if needed
            emails.extend(extract_emails(link))
            btc.extend(extract_btc(link))
            pgp.extend(extract_pgp(link))

        save_result(target, emails, btc, pgp)
        data_report.append({"url": target, "emails": emails, "btc": btc, "pgp": pgp})
        print(Fore.CYAN + "[✔] Data saved" + Style.RESET_ALL)

    elif choice == "2":
        keyword = input("Enter keyword: ")
        for item in data_report:
            if any(search_keyword(e, keyword) for e in item['emails']):
                print(Fore.YELLOW + f"[Match in {item['url']}]" + Style.RESET_ALL)

    elif choice == "3":
        renew_ip()
        print(Fore.MAGENTA + "[✔] New Tor identity requested" + Style.RESET_ALL)

    elif choice == "4":
        save_report(data_report)
        print(Fore.GREEN + "[✔] Report generated in reports/" + Style.RESET_ALL)

    elif choice == "5":
        print("Exiting...")
        break
