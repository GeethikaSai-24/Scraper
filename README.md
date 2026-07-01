# 🔍 Python Job Scraper

A Python web scraper that fetches real-time job listings from python.org/jobs, 
filters AI/ML related roles, and exports results to JSON and text reports.

## ✨ Features
- Scrapes live job listings from python.org
- Filters AI/ML/Data science roles using keyword matching
- Exports results to JSON for further processing
- Generates human-readable text reports with timestamps
- Handles network errors, timeouts, and HTTP failures gracefully

## 🛠️ Tech Stack
- Python 3.x
- requests — HTTP requests
- BeautifulSoup4 — HTML parsing
- json — data export
- datetime — timestamped output files

## ⚙️ Setup

```bash
git clone https://github.com/GeethikaSai-24/Scraper.git
cd Scraper
pip install requests beautifulsoup4
python scraper.py
```

## 📄 Output
Each run creates two files:
- `jobs_Python_YYYYMMDD_HHMM.json` — structured job data
- `report_Python_YYYYMMDD_HHMM.txt` — human-readable summary

## 👩‍💻 Developer
**Unnam Geethika Sai** — B.Tech CSE, NIT Andhra Pradesh (CGPA: 8.9)  
GitHub: [@GeethikaSai-24](https://github.com/GeethikaSai-24)
