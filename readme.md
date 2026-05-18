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

Stop running 5 different scripts manually. DeepRecon is a fully automated engine designed to map, index, and fingerprint target nodes inside the Tor network (.onion). 
We're talking: 
- 🏎️ **Ludicrous Speed**: Non-blocking iohttp SOCKS5 connections.
- 🧠 **Smart Crawling**: BFS traversal with duplicate-link avoidance and resilient memory caching.
- 🔍 **Full Text Search (FTS5)**: Finding what you need across gigabytes of indexed content instantly. 
- 🤖 **Auto-Extraction**: Regular Expressions? Nah, we dynamically scrape PGP keys, Cryptocoin Wallets (BTC, XMR), emails, tech-stack footprints (ingerprinter), and language data effortlessly.
- 💅 **Web & CLI Drip**: An interactive Rich-powered CLI or a sleek FastAPI-driven Dashboard. You pick.

Security Pros: It’s the modular Swiss Army Knife you wish you had yesterday.

---

## ⚙️ The "It Just Works" Installation

We built scripts because configuring environments shouldn't be a hurdle. **It auto-installs Tor, Python dependencies, and virtual environments.**

### 🐧 Linux/Debian/Kali user?
`ash
./install.sh
`

### 🪟 Windows?
`cmd
install.bat
`

> **Expert mode unlocked:** During install, we bind deeprecon directly to your path so you can call it locally from anywhere. 

*(Manual path)*
`ash
pip install -r requirements.txt
# Ensure Tor daemon is running!
`

---

## 🎮 How to Wield It

Run the framework. Period.

### 🌐 Web Interface Mode
Launch the local web dashboard for point-and-click intelligence gathering:
`ash
deeprecon --web --port 8000
`
Open http://localhost:8000 to start scanning and exploring your database.

### 💻 Elite CLI Mode
Stay in the terminal with our non-ending interactive loops:
`ash
deeprecon --cli
`
*What happens next?* The loop walks you through adding targets, kicking off asynchronous spiders, or searching your datasets on the fly. 

---

## 🏗️ Architecture & Extensibility

We hate monolithic messes. Inside, you'll find:

- **core/**: The asynchronous heart pumping bytes (crawler.py, parser.py).
- **plugins/**: Drop a new .py file inheriting BasePlugin here, and DeepRecon auto-detects it. Boom, new feature deployed.
- **storage/**: Safe, trigger-bypassing FTS5 SQLite row-replacement that refuses to corrupt.
- **web/ & main.py**: The dynamic frontends masking the sheer complexity behind the scenes.

**Need a custom parser?** Just copy plugins/fingerprinter.py, adjust the signatures, and you're parsing new artifacts.

---

## 🔒 OpSec Warning

This tool is built for **Ethical Security Research**. Interacting with .onion addresses inherently carries risk. DeepRecon masks user-agents and dynamically routes traffic, but it relies on your configured OPSEC rules. **Never operate without Tor running correctly.** Stay safe, fam. 

---

## 📝 License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.
