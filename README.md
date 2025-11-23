# GUSCrawler

**GUSCrawler** is a high-performance, multi-agent asynchronous web crawler built in Python.  
Designed for speed, efficiency, and massive scalability — no GPU required.

---

## 🚀 Features

- Multi-agent asynchronous crawling
- Smart URL deduplication
- Dynamic target discovery
- Customizable seed list
- Built-in logging and stats tracking
- Lightweight and resource-friendly

---

## 🧠 Tech Stack

- **Language:** Python 3.x  
- **Core:** `asyncio`, `aiohttp`, `beautifulsoup4`  
- **Logging:** `rich` or `colorama` (optional for styled output)

---

## 📁 Structure

gus_crawler/ <br>
│ <br>
├── main.py # entry point <br>
├── banner.py # GUS banner display <br>
├── agents/ # async crawling agents <br>
├── utils/ # helper modules (parser, URL cleaner, etc.) <br>
└── README.md


---

## ⚙️ Usage

```bash
python main.py --seeds seeds.txt --max-depth 3 --save output.txt
```
Or,
```bash
python main.py
```

## 🧪 Example Output
- [✅] Total URLs saved (including discovered links): 3383


  ## 🐍 License

GNU General Public License v3.0 (GPL-3.0) © 2025 Morse Dev  
Free to use, modify, and distribute under the terms of the GPL-3.0.

