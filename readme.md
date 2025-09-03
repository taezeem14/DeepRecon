# 🕵️ DeepRecon - Dark Web OSINT & Recon Tool

&#x20;&#x20;

DeepRecon is a **Dark Web OSINT framework** that allows security researchers to crawl `.onion` websites via the Tor network, perform keyword-based searches, collect intelligence, and generate reports.
It is designed for **ethical hacking, threat intelligence, and research purposes**.

---

## 📌 Features

✔ Crawl `.onion` websites through **Tor proxy**
✔ Perform **keyword searches** in crawled data
✔ **Auto-renew Tor IP** for anonymity
✔ Generate **HTML-based reports**
✔ Works on **Windows, Linux, and Kali Live USB**
✔ Modular structure for easy expansion

---

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/DeepRecon.git
cd DeepRecon
```

### 2. Install Dependencies

**Linux / Kali:**

```bash
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**

```powershell
install.bat
```

Or manually:

```bash
pip install -r requirements.txt
```

---

## ▶ Usage

Run the tool:

```bash
python main.py
```

### **Menu Options**

```
[1] Crawl Onion Site   → Crawl and extract links from a .onion site
[2] Keyword Search     → Search for keywords in crawled data
[3] Renew Tor IP       → Change Tor circuit for anonymity
[4] Generate Report    → Export results as an HTML report
[5] Exit               → Quit the tool
```

---

## 📂 Project Structure

```
DeepRecon/
├── core/            # Core logic (crawlers, parsers)
├── storage/         # Stores crawled data and reports
├── utils/           # Helper functions (e.g., Tor IP renew)
├── config.py        # Configuration (Tor settings, proxies)
├── main.py          # Entry point
├── requirements.txt # Dependencies
├── install.sh       # Linux/Kali auto installer
├── install.bat      # Windows installer
└── README.md
```

---

## ⚡ Example Commands

```bash
# Crawl a .onion site
python main.py
# Choose option 1 and enter .onion URL

# Search for keyword
python main.py
# Choose option 2 and enter keyword
```

---

## ⚠ Disclaimer

This tool is intended for **educational and research purposes only**.

The author is **not responsible for any misuse** of this tool.
