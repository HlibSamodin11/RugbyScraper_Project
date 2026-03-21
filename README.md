<div align="center">
  <img align="left" width="280" height="220" alt="image" src="https://github.com/user-attachments/assets/09d3cb8e-770a-4146-9e3b-497d69fd67f8" />
  <img src="https://github.com/user-attachments/assets/4cf1bc0f-f4fb-4264-a8f1-59e4292b85bf" alt="Center" width="240" height="240">
  <img align="right" src="https://github.com/user-attachments/assets/74b37d89-f0ab-4da1-95fa-938ced99e41c" alt="Right" width="240" height="240">
</div>

<div align="center">

# RugbyScraper 🏉
A terminal app for live rugby scores, standings and fixtures — with animated UI, team stats, and smart result notifications.

[![GitHub](https://img.shields.io/badge/GitHub-HlibSamodin11-black?logo=github)](https://github.com/HlibSamodin11)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/version-2.0-green)

#### 📝 Check out the DevLog!

</div>

---

## Why I made this

At 15, after finishing *Clean Code* by Robert C. Martin, I wanted to build something real to practice better coding. Rugby is my favourite sport, so I built a project I actually care about.

---

## Features

### v1.0
- ✅ Scrapes live rugby standings from ESPN
- ✅ Scrapes recent match results
- ✅ Clean, colourful terminal UI with animations
- ✅ Standings table with colour coded positions
- ✅ Match results display (home vs away with scores)
- ✅ Export standings to CSV
- ✅ SQLite database to store historical data
- ✅ Animated logo, banners and exit sequence
- ✅ Last updated timestamp on standings

### v2.0
- ✅ Auto-scrapes all competitions at startup
- ✅ PF, PA, PD columns — points for, against and difference
- ✅ Form column — last 5 results as coloured dots (● ● ●)
- ✅ Fixture list — upcoming matches with dates and team form
- ✅ Better results screen — winner highlighted in green with dates
- ✅ Animated team stats screen with points comparison bar chart
- ✅ Points trend graph — unlocks with daily scraping
- ✅ New result flash notifications on startup
- ✅ Smart error handling — retries, connection checks, rate limit handling
- ✅ Auto resize for narrow terminals
- ✅ Trophy 🏆 for 1st place, ⬇ for last place

---

## Competitions

|     | Competition               | Status         |
| --- | ------------------------- | -------------- |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿  | Six Nations               | ✅ Live        |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿  | Gallagher Premiership     | ✅ Live        |
| 🇫🇷  | Top 14                    | ✅ Live        |
| 🌍  | United Rugby Championship | ✅ Live        |
| 🌍  | Champions Cup             | ✅ Live        |
| 🌍  | Rugby Championship        | ✅ Live        |
| 🌍  | Rugby World Cup 2027      | 🔜 Coming Soon |

---

## Tech Stack

- Python 3
- `requests` — fetching ESPN pages
- `beautifulsoup4` — parsing HTML
- `rich` — terminal UI, tables, animations
- `sqlite3` — storing standings and match history

---

## Project Structure
```
RugbyScraper/
├── main.py          — entry point, handles user input
├── scraper.py       — fetches and parses ESPN data
├── display.py       — all terminal UI and animations
├── database.py      — SQLite database operations
├── competitions.py  — competition URLs and config
├── exporter.py      — CSV export
├── stats.py         — team history and form data
└── data/
    ├── rugby.db     — SQLite database
    └── exports/     — exported CSV files
```

---

## Clean Code Principles

- `snake_case` for functions and variables
- `CamelCase` for classes
- Small, focused functions with single responsibilities
- DRY — no repeated code
- Clear, meaningful names
- Docstrings on every function
- Graceful error handling throughout

---

## Installation
```bash
pip install requests beautifulsoup4 rich
```

Or with a virtual environment (recommended on Linux):
```bash
python3 -m venv venv
source venv/bin/activate.fish  # fish shell
pip install requests beautifulsoup4 rich
```

## How to Run
```bash
python main.py
```

Then pick a competition from the menu:

- Press `1-7` to select a competition
- Press `r` after standings to see recent results
- Press `f` after standings to see upcoming fixtures
- Press `t` after standings to see team stats and graph
- Press `e` after standings to export to CSV
- Press `a` for about
- Press `q` to quit

---

<div align="center">
<img width="230" height="230" alt="image" src="https://github.com/user-attachments/assets/6bfe34dd-e018-4029-a57e-4237ff70dee9"/>

Made with ❤️ by <a href="https://github.com/HlibSamodin11">HlibSamodin</a>
</div>