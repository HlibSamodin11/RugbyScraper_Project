<div align="center">
  <!-- Left image -->
<img align="left" width="280" height="220" alt="image" src="https://github.com/user-attachments/assets/09d3cb8e-770a-4146-9e3b-497d69fd67f8" />
<!-- Center image -->
<img src="https://github.com/user-attachments/assets/4cf1bc0f-f4fb-4264-a8f1-59e4292b85bf" alt="Center" width="240" height="240">
<!-- Right image -->
<img align="right" src="https://github.com/user-attachments/assets/74b37d89-f0ab-4da1-95fa-938ced99e41c" alt="Right" width="240" height="240">
</div>

<div align="center">

# RugbyScraper 🏉

A terminal app for live rugby scores and standings, with a focus on clean, readable code. Built to look great in the terminal, easy to use, and fun for rugby fans!

[![GitHub](https://img.shields.io/badge/GitHub-HlibSamodin11-black?logo=github)](https://github.com/HlibSamodin11)

#### 📝 Btw there is a DevLog so check it out!!

</div>

---

## Why I made this

At 15, after finishing "Clean Code" by Robert C. Martin, I wanted to build something real to practice better coding. Rugby is my favourite sport, so I made a project I actually care about.

---

## Features

- ✅ Scrapes live rugby standings from ESPN
- ✅ Scrapes recent match results
- ✅ Clean, colourful terminal UI with animations
- ✅ Standings table with colour coded positions
- ✅ Match results display (home vs away with scores)
- ✅ Export standings to CSV
- ✅ SQLite database to store historical data
- ✅ Animated logo, banners and exit sequence
- ✅ Last updated timestamp on standings

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
- `sqlite3` — storing standings history

---

## Clean Code Principles

- `snake_case` for functions and variables
- `CamelCase` for classes
- Small, focused functions
- DRY (no repeated code)
- Clear, meaningful names
- Good error handling

---

## Installation

```bash
pip install requests beautifulsoup4 rich
```

## How to Run

```bash
python main.py
```

Then pick a competition from the menu:

- Press `1-7` to select a competition
- Press `r` after standings to see recent results
- Press `e` after standings to export to CSV
- Press `a` for about
- Press `q` to quit

---

<div align="center">
<img width="230" height="230" alt="image" src="https://github.com/user-attachments/assets/03bf1d2e-a5e7-4781-9a46-9294fe24b421"/>

Made with ❤️ by <a href="https://github.com/HlibSamodin11">HlibSamodin</a>

</div>
