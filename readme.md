<div align="center">
   <h1>🕵️‍♂️ DeepRecon</h1>
   <a href="https://github.com/taezeem14/DeepRecon"><img alt="Python" src="https://img.shields.io/badge/Python-3.13+-blue.svg"></a>
   <a href="https://github.com/taezeem14/DeepRecon"><img alt="License" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
   <a href="https://github.com/taezeem14/DeepRecon"><img alt="DB" src="https://img.shields.io/badge/Storage-SQLite%20FTS5-cyan.svg"></a>
   <a href="https://github.com/taezeem14/DeepRecon"><img alt="Tor" src="https://img.shields.io/badge/Routing-Tor-purple.svg"></a>

   <p><b>DeepRecon is an advanced, fully asynchronous framework for conducting dark web OSINT investigations on the Tor (.onion) network.</b></p>
   <p>It leverages robust scraping heuristics, auto-scaling crawlers, and automated tech-stack fingerprinting to map and investigate hidden services effortlessly.</p>
   
   <p><a href="#features">Features</a> • <a href="#installation">Installation</a> • <a href="#usage">Usage</a> • <a href="#architecture">Architecture</a> • <a href="#disclaimer">Disclaimer</a></p>
</div>

<br>

> [!NOTE]
> DeepRecon requires a native Tor service to route traffic through the anonymity network safely. Ensure your Tor daemon is active before kicking off crawls.

---

## ✨ Features

- 🏎️ **Ludicrous Speed (Async SOCKS5)** – Built entirely around `aiohttp` and `asyncio`, utilizing non-blocking connection scaling to blitz through nodes.
- ⚙️ **Modular Architecture** – Clean separation between the engine, extraction rules, and storage workflows, allowing instant extensibility.
- 🌐 **Web UI** – A local FastAPI/Tailwind-based interactive dashboard for seamless investigations without terminal clutter.
- 💻 **Elite Terminal CLI** – Beautiful `rich`-powered interactive non-ending loops, live progress spinners, colored data tables, and regex-powered sub-searches natively from the terminal.
- 🔍 **Full-Text Search (FTS5)** – Blazing fast storage utilizing SQLite FTS5 index engines for gigabytes of HTML parsing logic, circumventing Trigger-Corruption.
- 🤖 **Auto-Extraction Plugins** – Dynamically loadable artifact extractors. Ships with out-of-the-box support for:
   - 🪙 `crypto_detector`: Bitcoin (BTC) / Monero (XMR) sniffer.
   - 📩 `email_extractor`: Heavy email standardizer.
   - 🏗️ `fingerprinter`: Detects Tech-Stacks (WordPress, React, Cloudflare, etc.).
   - 🔑 `pgp_harvester`: Automatically pulls PGP keys.
   - 🗺️ `language_detector`: NLP language identification.
- 📝 **Automated Custom Reporting** – Exports investigations to interactive HTML, raw JSON, and beautiful PDF structures instantly.

---

## 🏗️ Architecture

DeepRecon removes monolithic messes. The ecosystem is fully decoupled for instant upgrades:

- **`core/`**: The heavy-lifting crawler and HTML parser logic (`crawler.py`). Features resilient memory caching and Breadth-First Traversal (BFS) duplicate avoidance.
- **`plugins/`**: Extractor engines (`BasePlugin`). Drop a custom script here, and the framework automatically consumes it. No manual configs needed.
- **`storage/`**: Atomic-replacement SQLite engines handling Full-Text Search and relational nodes seamlessly.
- **`web/` & `main.py`**: Fast frontends acting as proxies to the background logic.

---

## ⚠️ Disclaimer

> [!WARNING]
> This tool is intended for **educational and lawful ethical security research purposes only**. Accessing or interacting with certain hidden services on the dark web may be heavily regulated or illegal depending on your jurisdiction. The author and contributors hold no liability for misuse of this tool or the intelligence gathered with it.
>
> We strongly advise enforcing robust OPSEC hygiene, utilizing dedicated sandbox environments alongside proper proxy configurations.
> Use responsibly and at your absolute own risk.

---

## 💾 Installation

DeepRecon packages an auto-installation script that provisions required system binaries, handles Tor network installation, and globally registers the `deeprecon` terminal binary to your path.

### Linux / Debian / Kali

Run the installation script to configure Python virtual environments, pip, and Tor:

```bash
git clone https://github.com/taezeem14/DeepRecon.git
cd DeepRecon
chmod +x install.sh
./install.sh
```

### Windows

Run the batch configuration:

```cmd
git clone https://github.com/taezeem14/DeepRecon.git
cd DeepRecon
install.bat
```

> [!TIP]
> **Windows Users**: You will need to manually download and let the [Tor Expert Bundle](https://www.torproject.org/download/tor/) run in the background on port `9050` before performing reconnaissance.

---

## 🎮 Usage

DeepRecon supports both interactive CLI scraping and a point-and-click browser interface.

### 🌐 Web Interface Mode
Launch the local web dashboard for intuitive intelligence gathering:
```bash
deeprecon --web --port 8000
```
*Navigate to `http://localhost:8000` to start your asynchronous intelligence pipelines.*

### 💻 Elite CLI Mode
Stay native in the terminal. Launch the interactive framework:
```bash
deeprecon --cli
```
*Follow the interactive rich-loops for executing deep-crawls, exporting PDFs, and searching target domains against Regex statements.*

---

## 🤝 Contributing

Contributions are fundamentally vital to open-source OSINT development! Please feel free to submit Pull Requests to improve the engine.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewPlugin`)
3. Commit your Changes (`git commit -m 'Add some NewPlugin'`)
4. Push to the Branch (`git push origin feature/NewPlugin`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.