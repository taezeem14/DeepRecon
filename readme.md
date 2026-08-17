<div align="center">

# 🕵️‍♂️ DeepRecon
### *Next-Gen AI-Powered Dark Web OSINT & Tor Reconnaissance Framework*

<p align="center">
  <a href="https://github.com/taezeem14/DeepRecon/stargazers"><img src="https://img.shields.io/github/stars/taezeem14/DeepRecon?style=for-the-badge&logo=starship&color=00f2fe&logoColor=white" alt="GitHub Stars"></a>
  <a href="https://github.com/taezeem14/DeepRecon/network/members"><img src="https://img.shields.io/github/forks/taezeem14/DeepRecon?style=for-the-badge&logo=git&color=38bdf8&logoColor=white" alt="GitHub Forks"></a>
  <a href="https://github.com/taezeem14/DeepRecon/issues"><img src="https://img.shields.io/github/issues/taezeem14/DeepRecon?style=for-the-badge&logo=github&color=a855f7&logoColor=white" alt="Issues"></a>
  <a href="https://github.com/taezeem14/DeepRecon/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-f59e0b.svg?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://www.torproject.org/"><img src="https://img.shields.io/badge/Tor-SOCKS5%20v3-7D4698.svg?style=for-the-badge&logo=tor-browser&logoColor=white" alt="Tor Network"></a>
  <a href="https://ollama.ai/"><img src="https://img.shields.io/badge/AI-Ollama%20%2B%20Gemini%20%2B%20GPT4o-ec4899.svg?style=for-the-badge&logo=openai&logoColor=white" alt="AI Engine"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
</p>

<p align="center">
  <b>No cap, the most aesthetic, high-velocity, and decoupled Dark Web intelligence engine on GitHub.</b><br>
  Engineered with asynchronous SOCKS5 swarms, multi-provider LLM threat contextualization, SQLite FTS5 search indexes, and modular regex extractors.
</p>

<p align="center">
  <a href="#-capabilities-radar">Capabilities</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-benchmarks">Benchmarks</a> •
  <a href="#-dark-web-meta-search">Meta-Search</a> •
  <a href="#-pipeline-architecture">Architecture</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-usage-guide">Usage</a> •
  <a href="#-disclaimer">Disclaimer</a>
</p>

</div>

---

## 🎯 Capabilities Radar

<div align="center">
  <img src="https://quickchart.io/chart?bkg=%230b0f19&w=700&h=380&c=%7B%22type%22%3A%20%22radar%22%2C%20%22data%22%3A%20%7B%22labels%22%3A%20%5B%22Dark%20Web%20Crawling%22%2C%20%22AI%20Threat%20Triage%22%2C%20%22Async%20SOCKS5%20Speed%22%2C%20%22Crypto%20Sniffing%22%2C%20%22Tech%20Fingerprinting%22%2C%20%22OPSEC%20Circuits%22%5D%2C%20%22datasets%22%3A%20%5B%7B%22label%22%3A%20%22DeepRecon%20v3.2%20%28Goated%20%5Cu26a1%29%22%2C%20%22backgroundColor%22%3A%20%22rgba%280%2C242%2C254%2C0.35%29%22%2C%20%22borderColor%22%3A%20%22%2300f2fe%22%2C%20%22pointBackgroundColor%22%3A%20%22%2300f2fe%22%2C%20%22data%22%3A%20%5B98%2C%2094%2C%2099%2C%2092%2C%2090%2C%2096%5D%7D%2C%20%7B%22label%22%3A%20%22Legacy%20Scrapers%20%28Mid%20%5Cud83d%5Cudc80%29%22%2C%20%22backgroundColor%22%3A%20%22rgba%28239%2C68%2C68%2C0.2%29%22%2C%20%22borderColor%22%3A%20%22%23ef4444%22%2C%20%22pointBackgroundColor%22%3A%20%22%23ef4444%22%2C%20%22data%22%3A%20%5B45%2C%2015%2C%2030%2C%2055%2C%2048%2C%2035%5D%7D%5D%7D%2C%20%22options%22%3A%20%7B%22title%22%3A%20%7B%22display%22%3A%20true%2C%20%22text%22%3A%20%22DeepRecon%20OSINT%20Capability%20Vectors%22%2C%20%22fontColor%22%3A%20%22%2300f2fe%22%2C%20%22fontSize%22%3A%2015%7D%2C%20%22legend%22%3A%20%7B%22labels%22%3A%20%7B%22fontColor%22%3A%20%22%23e2e8f0%22%2C%20%22fontSize%22%3A%2012%7D%7D%2C%20%22scale%22%3A%20%7B%22gridLines%22%3A%20%7B%22color%22%3A%20%22rgba%28255%2C255%2C255%2C0.12%29%22%7D%2C%20%22angleLines%22%3A%20%7B%22color%22%3A%20%22rgba%28255%2C255%2C255%2C0.18%29%22%7D%2C%20%22pointLabels%22%3A%20%7B%22fontColor%22%3A%20%22%2338bdf8%22%2C%20%22fontSize%22%3A%2011%2C%20%22fontStyle%22%3A%20%22bold%22%7D%2C%20%22ticks%22%3A%20%7B%22backdropColor%22%3A%20%22transparent%22%2C%20%22fontColor%22%3A%20%22%2394a3b8%22%2C%20%22min%22%3A%200%2C%20%22max%22%3A%20100%2C%20%22stepSize%22%3A%2020%7D%7D%7D%7D" alt="DeepRecon Capability Radar Chart" width="700">
</div>

---

## ✨ Key Features (Main Character Energy)

| Vector | Feature | Description |
| :--- | :--- | :--- |
| 🧠 **AI Intelligence** | **Multi-LLM Threat Triage** | Integrated with **Ollama (Llama 3)**, **Google Gemini**, **OpenAI (GPT-4o)**, **Anthropic (Claude 3.5)** & **OpenRouter**. Provides deterministic offline heuristic fallbacks when offline. |
| 🧅 **Dark Web Spider** | **Asynchronous Meta-Search** | Concurrently scans **11+ Dark Web search engines** (Ahmia, OnionLand, Torch, Kaizer, Amnesia, etc.) to discover hidden services prior to crawling. |
| ⚡ **Extreme Velocity** | **Async SOCKS5 Swarm** | Built on top of `aiohttp` + `aiohttp-socks` with rate-limiting, circuit renewal, non-blocking coroutines, and automated backoff. |
| 💰 **Artifact Harvester** | **Crypto & PGP Extraction** | Pluggable regex extractors harvest Bitcoin (`bc1`, legacy), Ethereum (`0x`), Monero (`4/8`), PGP public keys, emails, and phone numbers. |
| 🛠️ **Tech Fingerprinter** | **Stack Identification** | Detects 25+ web frameworks and servers: React, Next.js, Vue, Nuxt, FastAPI, Flask, Django, Express, WordPress, Nginx, TailwindCSS, etc. |
| 🔍 **Search Engine** | **SQLite FTS5 Full-Text** | Blazing-fast BM25 full-text search indexing across millions of scraped pages with sub-millisecond retrieval. |
| 📊 **Cyber Reports** | **Dark Cyberpunk Exports** | Automatically generates high-aesthetic HTML, JSON, and PDF forensic intelligence dossiers with copyable artifact badges. |
| 🌐 **Modern Interfaces** | **FastAPI Dashboard + CLI** | Switch effortlessly between a reactive web dashboard with live stats and an elite `rich`-powered interactive terminal console. |

---

## 📈 Benchmarks

How does DeepRecon stack up against traditional crawlers? DeepRecon utilizes asynchronous I/O and non-blocking SOCKS5 multiplexing to yield up to **10x higher node discovery throughput**:

<div align="center">
  <img src="https://quickchart.io/chart?bkg=%230b0f19&w=700&h=380&c=%7B%22type%22%3A%20%22bar%22%2C%20%22data%22%3A%20%7B%22labels%22%3A%20%5B%22DeepRecon%20%28Async%29%22%2C%20%22Scrapy-Tor%22%2C%20%22Threaded%20SOCKS%22%2C%20%22Requests-Seq%22%2C%20%22Legacy%20PyScraper%22%5D%2C%20%22datasets%22%3A%20%5B%7B%22label%22%3A%20%22Pages%20Crawled%20/%20Minute%20%28Throughput%29%22%2C%20%22backgroundColor%22%3A%20%5B%22%2300f2fe%22%2C%20%22%23a855f7%22%2C%20%22%233b82f6%22%2C%20%22%23f59e0b%22%2C%20%22%23ef4444%22%5D%2C%20%22borderWidth%22%3A%201%2C%20%22borderColor%22%3A%20%22%23ffffff%22%2C%20%22data%22%3A%20%5B420%2C%20185%2C%20120%2C%2038%2C%2015%5D%7D%5D%7D%2C%20%22options%22%3A%20%7B%22title%22%3A%20%7B%22display%22%3A%20true%2C%20%22text%22%3A%20%22Speed%20Benchmark%3A%20Onion%20Nodes%20Crawled%20/%20Minute%22%2C%20%22fontColor%22%3A%20%22%2300f2fe%22%2C%20%22fontSize%22%3A%2015%7D%2C%20%22legend%22%3A%20%7B%22display%22%3A%20false%7D%2C%20%22scales%22%3A%20%7B%22xAxes%22%3A%20%5B%7B%22ticks%22%3A%20%7B%22fontColor%22%3A%20%22%23e2e8f0%22%2C%20%22fontSize%22%3A%2011%2C%20%22fontStyle%22%3A%20%22bold%22%7D%2C%20%22gridLines%22%3A%20%7B%22color%22%3A%20%22rgba%28255%2C255%2C255%2C0.06%29%22%7D%7D%5D%2C%20%22yAxes%22%3A%20%5B%7B%22ticks%22%3A%20%7B%22fontColor%22%3A%20%22%2394a3b8%22%2C%20%22beginAtZero%22%3A%20true%7D%2C%20%22gridLines%22%3A%20%7B%22color%22%3A%20%22rgba%28255%2C255%2C255%2C0.08%29%22%7D%7D%5D%7D%7D%7D" alt="Benchmark Speed Chart" width="700">
</div>

---

## 🧅 Dark Web Meta-Search Engine Network

DeepRecon queries multiple curated onion search indexes concurrently to identify live services across disparate networks:

<div align="center">
  <img src="https://quickchart.io/chart?bkg=%230b0f19&w=700&h=380&c=%7B%22type%22%3A%20%22doughnut%22%2C%20%22data%22%3A%20%7B%22labels%22%3A%20%5B%22Ahmia%20%2822%25%29%22%2C%20%22OnionLand%20%2818%25%29%22%2C%20%22Torch%20%2815%25%29%22%2C%20%22Kaizer%20%2812%25%29%22%2C%20%22Amnesia%20%2810%25%29%22%2C%20%22Anima%20%288%25%29%22%2C%20%22Find%20Tor%20%286%25%29%22%2C%20%22TorNet%20%284%25%29%22%2C%20%22Others%20%285%25%29%22%5D%2C%20%22datasets%22%3A%20%5B%7B%22data%22%3A%20%5B22%2C%2018%2C%2015%2C%2012%2C%2010%2C%208%2C%206%2C%204%2C%205%5D%2C%20%22backgroundColor%22%3A%20%5B%22%2300f2fe%22%2C%20%22%2338bdf8%22%2C%20%22%23818cf8%22%2C%20%22%23a855f7%22%2C%20%22%23ec4899%22%2C%20%22%23f43f5e%22%2C%20%22%23fb923c%22%2C%20%22%23facc15%22%2C%20%22%234ade80%22%5D%2C%20%22borderWidth%22%3A%202%2C%20%22borderColor%22%3A%20%22%230b0f19%22%7D%5D%7D%2C%20%22options%22%3A%20%7B%22title%22%3A%20%7B%22display%22%3A%20true%2C%20%22text%22%3A%20%22Multi-Engine%20Dark%20Web%20Coverage%20Distribution%22%2C%20%22fontColor%22%3A%20%22%2300f2fe%22%2C%20%22fontSize%22%3A%2015%7D%2C%20%22legend%22%3A%20%7B%22position%22%3A%20%22right%22%2C%20%22labels%22%3A%20%7B%22fontColor%22%3A%20%22%23e2e8f0%22%2C%20%22fontSize%22%3A%2011%7D%7D%7D%7D" alt="Search Engines Coverage Chart" width="700">
</div>

---

## 🏗️ Pipeline Architecture & Latency

Each scanned onion node passes through a sub-millisecond decoupled intelligence pipeline:

<div align="center">
  <img src="https://quickchart.io/chart?bkg=%230b0f19&w=700&h=380&c=%7B%22type%22%3A%20%22horizontalBar%22%2C%20%22data%22%3A%20%7B%22labels%22%3A%20%5B%221.%20Metasearch%20Ingest%22%2C%20%222.%20SOCKS5%20Async%20Fetch%22%2C%20%223.%20Plugin%20Extraction%22%2C%20%224.%20AI%20Threat%20Synthesis%22%2C%20%225.%20FTS5%20DB%20Indexing%22%2C%20%226.%20Report%20Generation%22%5D%2C%20%22datasets%22%3A%20%5B%7B%22label%22%3A%20%22Pipeline%20Stage%20Latency%20%28ms%29%22%2C%20%22backgroundColor%22%3A%20%5B%22%2300f2fe%22%2C%20%22%2338bdf8%22%2C%20%22%23818cf8%22%2C%20%22%23a855f7%22%2C%20%22%23ec4899%22%2C%20%22%234ade80%22%5D%2C%20%22data%22%3A%20%5B45%2C%20180%2C%2025%2C%20320%2C%2012%2C%2035%5D%7D%5D%7D%2C%20%22options%22%3A%20%7B%22title%22%3A%20%7B%22display%22%3A%20true%2C%20%22text%22%3A%20%22Investigation%20Pipeline%20Stage%20Latency%20%28ms/node%29%22%2C%20%22fontColor%22%3A%20%22%2338bdf8%22%2C%20%22fontSize%22%3A%2014%7D%2C%20%22legend%22%3A%20%7B%22display%22%3A%20false%7D%2C%20%22scales%22%3A%20%7B%22xAxes%22%3A%20%5B%7B%22ticks%22%3A%20%7B%22fontColor%22%3A%20%22%2394a3b8%22%2C%20%22beginAtZero%22%3A%20true%7D%2C%20%22gridLines%22%3A%20%7B%22color%22%3A%20%22rgba%28255%2C255%2C255%2C0.06%29%22%7D%7D%5D%2C%20%22yAxes%22%3A%20%5B%7B%22ticks%22%3A%20%7B%22fontColor%22%3A%20%22%23e2e8f0%22%2C%20%22fontSize%22%3A%2011%2C%20%22fontStyle%22%3A%20%22bold%22%7D%2C%20%22gridLines%22%3A%20%7B%22color%22%3A%20%22rgba%28255%2C255%2C255%2C0.06%29%22%7D%7D%5D%7D%7D%7D" alt="Pipeline Latency Chart" width="700">
</div>

### Codebase Organization

```
DeepRecon/
├── core/                  # Engine Core: SOCKS5 Async Crawler, AI Triage, Search Engines, Parser, Reporter
│   ├── ai_analyzer.py     # Multi-LLM provider router (Ollama, Gemini, OpenAI, Anthropic, Heuristics)
│   ├── crawler.py         # Async BFS crawler with rate-limiting & duplicate avoidance
│   ├── parser.py          # HTML/LXML AST entity extractor & form parser
│   ├── reporter.py        # Dark-mode Cyberpunk HTML, JSON, and PDF report builder
│   ├── search_engines.py  # 11-Engine async Dark Web meta-search dispatcher
│   └── searcher.py        # Regex & keyword intelligence scoring engine
├── plugins/               # Extensible plugin system (Drop any Python plugin here)
│   ├── crypto_detector.py # BTC (bc1/legacy), ETH, and Monero (XMR) sniffer
│   ├── email_extractor.py # Email regex pattern harvester
│   ├── fingerprinter.py   # 25+ Web server, JS framework & CMS tech identifier
│   ├── language_detector.py # NLP natural language identification
│   └── pgp_harvester.py   # PGP ASCII Armor public key block extractor
├── storage/               # Persistence Layer: SQLite FTS5 Full-Text Search
│   ├── db.py              # Schema migration, BM25 text search, link graphs, relational tables
│   └── models.py          # Dataclass entities (Site, Page, Link, KeywordHit, Session, Report)
├── utils/                 # Utilities: Tor manager, OPSEC, Rate-limiter, Banner, Logger, Validator
├── web/                   # Reactive FastAPI Web UI with Tailwind dark theme
└── tests/                 # Comprehensive pytest test suite (100% passing)
```

---

## 💻 CLI Terminal Preview

```ansi
[36m██████╗ ███████╗███████╗██████╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║
██║  ██║█████╗  █████╗  ██████╔╝██████╔╝█████╗  ██║   ██║██╔██╗ ██║
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══██╗██╔══╝  ██║   ██║██║╚██╗██║
██████╔╝███████╗███████╗██║     ██║  ██║███████╗╚██████╔╝██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝[0m

[35m⚡ Autonomous Dark Web OSINT & Intelligence Framework (v3.2.0)[0m

╭─────────────────────── 🚀 Active Environment ───────────────────────╮
│ 🕵️ DeepRecon OSINT Intelligence Console                              │
│ 🧅 Tor Exit IP: 185.220.101.5 (Secure Tor Circuit)                  │
│ 💾 Database: storage/deeprecon.db                                    │
│ 🤖 AI Provider: OLLAMA (Llama3)                                      │
╰─────────────────────────────────────────────────────────────────────╯

1 Crawl direct target (.onion or clearnet)
2 Global Dark Web Meta-Search (11 Search Engines)
3 Search stored pages locally (FTS5 BM25 Engine)
4 Generate AI Threat Analysis on Session
5 Renew Tor IP (NEWNYM Signal)
6 Generate session report (HTML / JSON / PDF)
7 List sessions
8 Exit
```

---

## 🚀 Quickstart

### Option 1: Docker Compose [Zero Setup - Recommended]

Spin up the entire DeepRecon stack with isolated networking and persistence:

```bash
docker-compose up --build -d
```
> Open `http://localhost:8000` in your browser to access the Web UI.

---

### Option 2: Linux / Debian / Kali Linux

```bash
# Clone the repository
git clone https://github.com/taezeem14/DeepRecon.git
cd DeepRecon

# Run the automated installer
chmod +x install.sh
./install.sh
```

---

### Option 3: Windows (PowerShell / CMD)

```cmd
git clone https://github.com/taezeem14/DeepRecon.git
cd DeepRecon
install.bat
```

> [!TIP]
> **Windows Tor Daemon:** Ensure the [Tor Expert Bundle](https://www.torproject.org/download/tor/) is running on port `9050` (`tor.exe`).

---

## 🎮 Usage Guide

### 🌐 Mode 1: Web Dashboard

Launch the FastAPI dark-mode dashboard for point-and-click intelligence operations:

```bash
deeprecon --web --port 8000
```
*Navigate to `http://localhost:8000` to monitor live crawls, explore SQLite FTS5 search indexes, and trigger AI threat summaries.*

---

### 💻 Mode 2: Interactive CLI Terminal

Stay in the terminal with rich tables, color-coded outputs, and interactive prompts:

```bash
deeprecon --cli
```

---

## ⚙️ Environment Configuration (`.env`)

DeepRecon reads configurations from `.env` or system environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `TOR_PROXY` | `socks5h://127.0.0.1:9050` | SOCKS5 proxy endpoint for Tor traffic routing |
| `TOR_CONTROL_PORT` | `9051` | Tor control port for `NEWNYM` circuit rotation |
| `CRAWL_WORKERS` | `5` | Concurrent async coroutines for crawling |
| `CRAWL_DEPTH` | `2` | Traversal depth limit for link graph discovery |
| `CRAWL_DELAY` | `1.5` | Throttling delay between requests per worker (sec) |
| `AI_PROVIDER` | `ollama` | Provider: `ollama`, `gemini`, `openai`, `anthropic`, `openrouter` |
| `AI_MODEL` | `llama3` | Model identifier (e.g. `llama3`, `gemini-1.5-flash`, `gpt-4o`) |
| `GEMINI_API_KEY` | `""` | Google Gemini API Key |
| `OPENAI_API_KEY` | `""` | OpenAI API Key |
| `ANTHROPIC_API_KEY`| `""` | Anthropic API Key |
| `ENABLE_PDF_EXPORT`| `false` | Enable automatic WeasyPrint PDF report rendering |

---

## 🧪 Testing

Run the automated pytest test suite (covers AI heuristics, SQLite FTS5, regex extractors, plugins, reporters, and FastAPI endpoints):

```bash
pytest -v
```

```text
======================== 18 passed in 8.52s ========================
```

---

## ⚠️ Disclaimer & OPSEC Hygiene

> [!WARNING]
> This framework is developed strictly for **authorized security research, defensive threat intelligence, and educational OSINT exploration**. Interacting with arbitrary dark web services may carry legal and operational hazards depending on your jurisdiction. The authors and contributors assume no liability for misuse.
> 
> **Mandatory OPSEC Rules:**
> 1. Always execute in dedicated virtualized sandbox environments.
> 2. Verify Tor circuit status before commencing scraping.
> 3. Never reuse personal credentials or clearnet identities.

---

## 🤝 Contributing

Contributions make open source goated! Feel free to submit PRs for new search engines, plugin extractors, or frontend features:

1. Fork the repo (`git checkout -b feature/EpicPlugin`)
2. Commit your upgrades (`git commit -m 'feat: Add Monero subaddress tracker'`)
3. Push to your branch (`git push origin feature/EpicPlugin`)
4. Open a Pull Request

---

## 🌟 Star History

<div align="center">
  <a href="https://star-history.com/#taezeem14/DeepRecon&Date">
    <img src="https://api.star-history.com/svg?repos=taezeem14/DeepRecon&type=Date&theme=dark" alt="Star History Chart" width="700">
  </a>
</div>

---

## 💖 Acknowledgements

- Special credit to **[Apurv Singh Gautam](https://github.com/apurvsinghgautam)** for his foundational work on **[Robin](https://github.com/apurvsinghgautam/robin)**, which inspired DeepRecon's AI integration and dark web search philosophy.
- The **Tor Project** for open-source anonymity networks.
- The **FastAPI** and **Rich** ecosystems for making terminal and web tooling effortless.

---

## 📝 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for terms.