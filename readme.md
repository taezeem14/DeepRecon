<div align="center">

# 🕵️‍♂️ DeepRecon

**The no-cap next-gen Dark Web OSINT engine that runs on literal ✨magic✨.**  
*But seriously, it’s a fully asynchronous, modular, and auto-scaling reconnaissance framework built for security researchers who actually want results without the headache.*

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by sqlite](https://img.shields.io/badge/Powered_by-SQLite%20FTS5-cyan.svg)](https://sqlite.org/)
[![Routing: Tor](https://img.shields.io/badge/Routing-Tor-purple.svg)](https://www.torproject.org/)
[![UI: Rich & FastAPI](https://img.shields.io/badge/UI-Rich_%7C_FastAPI-green.svg)](-)

</div>

---

## 🚀 Wait, What is DeepRecon?

Stop running 5 different scripts manually. DeepRecon is a fully automated engine designed to map, index, and fingerprint target nodes inside the Tor network (`.onion`). 
We're talking: 
- 🏎️ **Ludicrous Speed**: Non-blocking `aiohttp` SOCKS5 connections.
- 🧠 **Smart Crawling**: BFS traversal with duplicate-link avoidance and resilient memory caching.
- 🔍 **Full Text Search (FTS5)**: Finding what you need across gigabytes of indexed content instantly. 
- 🤖 **Auto-Extraction**: Regular Expressions? Nah, we dynamically scrape PGP keys, Cryptocoin Wallets (BTC, XMR), emails, tech-stack footprints (`fingerprinter`), and language data effortlessly.
- 💅 **Web & CLI Drip**: An interactive Rich-powered CLI or a sleek FastAPI-driven Dashboard. You pick.

Security Pros: It’s the modular Swiss Army Knife you wish you had yesterday.

---

## ✨ Features Array (No Cap)

We packed this framework with everything you need for passive recon:

- 🕸️ **Local Web Dashboard**: A dark-mode FastAPI + TailwindCSS frontend. Trigger async background scans and explore FTS5 databases without ever touching the terminal.
- 💻 **Elite Terminal CLI**: Built with `rich`. Features continuous interactive loops, live progress spinners, colored data tables, and regex-powered sub-searches.
- 🧅 **Native Tor Integration**: Built-in SOCKS5 proxy handling, automatic Tor IP identity renewal, and connection validation (`tor_manager.py`).
- 💿 **Bulletproof Storage Engine**: Upgraded SQLite architecture utilizing Full-Text Search (FTS5). Features atomic delete-and-reinsert page updates to prevent the infamous "database malformed" trigger corruption.
- 🧩 **Auto-loading Plugin Extractor**: Drop scripts in `/plugins` and it automatically runs them on scraped HTML. Ships out-of-the-box with:
  - `crypto_detector.py`: Sniffs out Bitcoin (BTC) and Monero (XMR) addresses.
  - `email_extractor.py`: Aggressively parses and standardizes email artifacts.
  - `fingerprinter.py`: Regex-based tech stack fingerprinting (WordPress, React, PHP, Nginx, Apache, MySQL, etc.).
  - `pgp_harvester.py`: Automatically unearths hidden PGP Public Keys.
  - `language_detector.py`: Uses NLP to detect the primary language of hidden service content.
- 🕷️ **Asynchronous Spider**: `aiohttp` non-blocking architecture natively doing Breadth-First Search (BFS) with strict duplicate avoidance.
- 📊 **Automated Reporting**: Export entire reconnaissance sessions to HTML, JSON, and PDF (powered by WeasyPrint).
- ⚡ **Global Binary Setup**: `install.bat` and `install.sh` don't just pip install; they provision Tor and bind `deeprecon` to your global `PATH`.

---

## ⚙️ The "It Just Works" Installation

We built scripts because configuring environments shouldn't be a hurdle. **It auto-installs Tor, Python dependencies, and virtual environments.**

### 🐧 Linux/Debian/Kali user?
```bash
./install.sh
```

### 🪟 Windows?
```cmd
install.bat
```

> **Expert mode unlocked:** During install, we bind `deeprecon` directly to your path so you can call it locally from anywhere. 

*(Manual path)*
```bash
pip install -r requirements.txt
# Ensure Tor daemon is running!
```

---

## 🎮 How to Wield It

Run the framework. Period.

### 🌐 Web Interface Mode
Launch the local web dashboard for point-and-click intelligence gathering:
```bash
deeprecon --web --port 8000
```
Open `http://localhost:8000` to start scanning and exploring your database.

### 💻 Elite CLI Mode
Stay in the terminal with our non-ending interactive loops:
```bash
deeprecon --cli
```
*What happens next?* The loop walks you through adding targets, kicking off asynchronous spiders, or searching your datasets on the fly. 

---

## 🏗️ Architecture & Extensibility

We hate monolithic messes. Inside, you'll find:

- **`core/`**: The asynchronous heart pumping bytes (`crawler.py`, `parser.py`).
- **`plugins/`**: Drop a new `.py` file inheriting `BasePlugin` here, and DeepRecon auto-detects it. Boom, new feature deployed.
- **`storage/`**: Safe, trigger-bypassing FTS5 SQLite row-replacement that refuses to corrupt.
- **`web/` & `main.py`**: The dynamic frontends masking the sheer complexity behind the scenes.

**Need a custom parser?** Just copy `plugins/fingerprinter.py`, adjust the signatures, and you're parsing new artifacts.

---

## 🔒 OpSec Warning

This tool is built for **Ethical Security Research**. Interacting with `.onion` addresses inherently carries risk. DeepRecon masks user-agents and dynamically routes traffic, but it relies on your configured OPSEC rules. **Never operate without Tor running correctly.** Stay safe, fam. 

---

## 📝 License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.