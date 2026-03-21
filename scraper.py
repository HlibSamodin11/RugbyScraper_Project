import time
from datetime import date

import requests
from bs4 import BeautifulSoup

from database import (
    get_team_id,
    initialise_database,
    insert_competition,
    insert_match,
    insert_standing,
    insert_team,
    log_scrape,
)

# ── network config ────────────────────────────────────────────────────────────

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

MAX_RETRIES = 3
RETRY_DELAY = 2
REQUEST_TIMEOUT = 10
CONNECTIVITY_TIMEOUT = 5
ESPN_BASE_URL = "https://www.espn.com"

# ── ESPN HTML selectors ───────────────────────────────────────────────────────

CLASS_FIXED_LEFT_TABLE = "Table--fixed-left"
CLASS_STATS_TABLE = "Table--align-right"
CLASS_TEAM_POSITION = "team-position"
CLASS_TEAM_NAME_HIDDEN = "hide-mobile"
CLASS_STAT_CELL = "stat-cell"
CLASS_SCOREBOARD = "Scoreboard"
CLASS_SCORE_ITEM = "ScoreboardScoreCell__Item"
CLASS_HOME_ITEM = "ScoreboardScoreCell__Item--home"
CLASS_AWAY_ITEM = "ScoreboardScoreCell__Item--away"
CLASS_TEAM_NAME = "ScoreCell__TeamName"
CLASS_SCORE = "ScoreCell__Score"
CLASS_TIME = "ScoreCell__Time"
CLASS_DATE_FALLBACK = "ScoreboardScoreCell__Date"
CLASS_TIME_FALLBACK = "ScoreboardScoreCell__Time"
CLASS_FORM = "clr-gray-04"

# ── stat cell indices ─────────────────────────────────────────────────────────

STAT_PLAYED = 0
STAT_WON = 1
STAT_DRAWN = 2
STAT_LOST = 3
STAT_POINTS_FOR = 5
STAT_POINTS_AGAINST = 6
STAT_POINTS_DIFF = 12
STAT_POINTS = 13
MIN_STAT_CELLS = 14

# ── HTTP status handling ──────────────────────────────────────────────────────

# maps status code → (message, sleep_seconds, should_retry)
STATUS_HANDLERS = {
    404: ("  page not found (404): {url}", None, False),
    403: ("  access denied (403) — ESPN may be blocking scrapers", None, False),
    429: ("  rate limited (429) — waiting before retry...", 5, True),
}

# ── connectivity ──────────────────────────────────────────────────────────────


def is_espn_reachable() -> bool:
    try:
        r = requests.get(
            ESPN_BASE_URL, headers=REQUEST_HEADERS, timeout=CONNECTIVITY_TIMEOUT
        )
        return r.status_code < 500
    except Exception:
        return False


# ── fetching ──────────────────────────────────────────────────────────────────


def fetch_espn_page(url: str) -> str | None:
    if not url:
        return None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.text

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else None
            _handle_http_error(status, url, attempt)
            if not _should_retry(status):
                return None

        except requests.exceptions.ConnectionError:
            print(f"  no internet connection — attempt {attempt}/{MAX_RETRIES}")

        except requests.exceptions.Timeout:
            print(f"  request timed out — attempt {attempt}/{MAX_RETRIES}")

        except requests.exceptions.RequestException as e:
            print(f"  unexpected error: {e}")
            return None

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    print(f"  failed after {MAX_RETRIES} attempts: {url}")
    return None


def _handle_http_error(status: int, url: str, attempt: int) -> None:
    msg, delay, _ = STATUS_HANDLERS.get(
        status,
        (
            f"  ESPN server error ({status}), attempt {attempt}/{MAX_RETRIES}",
            None,
            True,
        ),
    )
    print(msg.format(url=url) if "{url}" in msg else msg)
    if delay:
        time.sleep(delay)


def _should_retry(status: int) -> bool:
    _, _, retry = STATUS_HANDLERS.get(status, (None, None, True))
    return retry


# ── parsing helpers ───────────────────────────────────────────────────────────


def _find_stats_table(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        classes = table.get("class") or []
        if CLASS_STATS_TABLE in classes and CLASS_FIXED_LEFT_TABLE not in classes:
            return table
    return None


def _parse_team_row(team_row, index: int) -> tuple:
    position_tag = team_row.find("span", class_=CLASS_TEAM_POSITION)
    position = int(position_tag.text.strip()) if position_tag else index + 1

    name_tag = team_row.find("span", class_=CLASS_TEAM_NAME_HIDDEN)
    team_name = name_tag.text.strip() if name_tag else "unknown"

    return position, team_name


def _parse_stat_row(stat_row) -> dict | None:
    cells = stat_row.find_all("span", class_=CLASS_STAT_CELL)
    if len(cells) < MIN_STAT_CELLS:
        return None

    return {
        "played": int(cells[STAT_PLAYED].text.strip()),
        "won": int(cells[STAT_WON].text.strip()),
        "drawn": int(cells[STAT_DRAWN].text.strip()),
        "lost": int(cells[STAT_LOST].text.strip()),
        "points_for": int(cells[STAT_POINTS_FOR].text.strip()),
        "points_against": int(cells[STAT_POINTS_AGAINST].text.strip()),
        "points_diff": cells[STAT_POINTS_DIFF].text.strip(),
        "points": int(cells[STAT_POINTS].text.strip()),
    }


def _extract_home_away(match) -> tuple | None:
    teams = match.find_all("li", class_=CLASS_SCORE_ITEM)
    if len(teams) < 2:
        return None

    home_li = away_li = None
    for t in teams:
        classes = t.get("class") or []
        if CLASS_HOME_ITEM in classes:
            home_li = t
        elif CLASS_AWAY_ITEM in classes:
            away_li = t

    return (home_li, away_li) if home_li and away_li else None


def _extract_match_date(match) -> str:
    date_tag = match.find("div", class_=CLASS_TIME)
    if not date_tag:
        date_tag = match.find("span", class_=CLASS_DATE_FALLBACK)
    return (
        date_tag.text.strip()
        if date_tag and date_tag.text.strip()
        else date.today().isoformat()
    )


def _extract_fixture_date(match) -> str:
    date_tag = match.find("div", class_=CLASS_TIME)
    if not date_tag:
        date_tag = match.find("div", class_=CLASS_TIME_FALLBACK)
    return date_tag.text.strip() if date_tag and date_tag.text.strip() else "TBC"


# ── parsers ───────────────────────────────────────────────────────────────────


def parse_standings(html: str) -> list:
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    left_table = soup.find("table", class_=CLASS_FIXED_LEFT_TABLE)
    if not left_table or not left_table.find("tbody"):
        return []

    right_table = _find_stats_table(soup)
    if not right_table or not right_table.find("tbody"):
        return []

    team_rows = left_table.find("tbody").find_all("tr")
    stat_rows = right_table.find("tbody").find_all("tr")

    standings = []
    for i, (team_row, stat_row) in enumerate(zip(team_rows, stat_rows)):
        position, team_name = _parse_team_row(team_row, i)
        stats = _parse_stat_row(stat_row)
        if stats:
            standings.append({"position": position, "team_name": team_name, **stats})

    return standings


def parse_results(html: str) -> list:
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []

    for match in soup.find_all("section", class_=CLASS_SCOREBOARD):
        try:
            sides = _extract_home_away(match)
            if not sides:
                continue

            home_li, away_li = sides
            home_name = home_li.find("div", class_=CLASS_TEAM_NAME)
            away_name = away_li.find("div", class_=CLASS_TEAM_NAME)
            home_score = home_li.find("div", class_=CLASS_SCORE)
            away_score = away_li.find("div", class_=CLASS_SCORE)

            if not all([home_name, away_name, home_score, away_score]):
                continue

            home_score_text = home_score.text.strip()
            away_score_text = away_score.text.strip()

            # skip unplayed matches
            if not home_score_text.isdigit() or not away_score_text.isdigit():
                continue

            results.append(
                {
                    "home": home_name.text.strip(),
                    "away": away_name.text.strip(),
                    "home_score": home_score_text,
                    "away_score": away_score_text,
                    "date": _extract_match_date(match),
                }
            )

        except Exception:
            continue

    return results


def parse_fixtures(html: str) -> list:
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    fixtures = []

    for match in soup.find_all("section", class_=CLASS_SCOREBOARD):
        try:
            sides = _extract_home_away(match)
            if not sides:
                continue

            home_li, away_li = sides
            home_name = home_li.find("div", class_=CLASS_TEAM_NAME)
            away_name = away_li.find("div", class_=CLASS_TEAM_NAME)

            if not home_name or not away_name:
                continue

            home_score = home_li.find("div", class_=CLASS_SCORE)
            away_score = away_li.find("div", class_=CLASS_SCORE)
            home_score_text = home_score.text.strip() if home_score else ""
            away_score_text = away_score.text.strip() if away_score else ""

            # skip already played matches
            if home_score_text.isdigit() and away_score_text.isdigit():
                continue

            home_form_tag = home_li.find("span", class_=CLASS_FORM)
            away_form_tag = away_li.find("span", class_=CLASS_FORM)

            fixtures.append(
                {
                    "home": home_name.text.strip(),
                    "away": away_name.text.strip(),
                    "date": _extract_fixture_date(match),
                    "home_form": home_form_tag.text.strip().strip("()")
                    if home_form_tag
                    else "",
                    "away_form": away_form_tag.text.strip().strip("()")
                    if away_form_tag
                    else "",
                }
            )

        except Exception:
            continue

    return fixtures


# ── saving ────────────────────────────────────────────────────────────────────


def _save_standings(standings: list, competition_id: int) -> None:
    for row in standings:
        insert_team(row["team_name"], None, None, None)
        team_id = get_team_id(row["team_name"])
        if not team_id:
            continue
        insert_standing(
            team_id,
            competition_id,
            row["position"],
            row["played"],
            row["won"],
            row["drawn"],
            row["lost"],
            row["points_for"],
            row["points_against"],
            row["points_diff"],
            row["points"],
            date.today().isoformat(),
        )


def save_results(competition_id: int, results: list) -> None:
    for r in results:
        try:
            insert_match(
                competition_id,
                r["home"],
                r["away"],
                int(r["home_score"]),
                int(r["away_score"]),
                r.get("date", date.today().isoformat()),
            )
        except ValueError:
            continue


def scrape_and_save(
    competition_id: int,
    url: str,
    competition_name: str,
    competition_type: str,
    season,
) -> bool:
    initialise_database()
    insert_competition(competition_name, competition_type, season)

    html = fetch_espn_page(url)
    standings = parse_standings(html)

    if not standings:
        log_scrape(0, "failed")
        return False

    _save_standings(standings, competition_id)
    log_scrape(len(standings), "success")
    return True


def auto_scrape_all(competitions: dict) -> dict:
    results = {}
    for key, comp in competitions.items():
        if not comp["url"]:
            results[key] = {"success": False, "reason": "coming soon"}
            continue

        success = scrape_and_save(
            int(key), comp["url"], comp["name"], comp["type"], comp["season"]
        )
        results[key] = {"success": success, "name": comp["name"]}

        if comp["results_url"]:
            html = fetch_espn_page(comp["results_url"])
            if html:
                save_results(int(key), parse_results(html))

    return results


if __name__ == "__main__":
    html = fetch_espn_page("https://www.espn.com/rugby/scoreboard/_/league/180659")
    if html:
        results = parse_results(html)
        print(f"found {len(results)} matches")
        for r in results:
            print(f"  {r['home']} {r['home_score']} - {r['away_score']} {r['away']}")
    else:
        print("failed to fetch")
