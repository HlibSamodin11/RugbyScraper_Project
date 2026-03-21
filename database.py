import os
import sqlite3
from datetime import datetime

# ── config ────────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "rugby.db")
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# ── table definitions ─────────────────────────────────────────────────────────

CREATE_TEAMS_SQL = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name   TEXT NOT NULL UNIQUE,
        short_name  TEXT,
        country     TEXT,
        league      TEXT
    )
"""

CREATE_COMPETITIONS_SQL = """
    CREATE TABLE IF NOT EXISTS competitions (
        competition_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        competition_name    TEXT NOT NULL,
        competition_type    TEXT,
        season              TEXT
    )
"""

CREATE_STANDINGS_SQL = """
    CREATE TABLE IF NOT EXISTS standings (
        standing_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id         INTEGER NOT NULL,
        competition_id  INTEGER NOT NULL,
        position        INTEGER,
        played          INTEGER,
        won             INTEGER,
        drawn           INTEGER,
        lost            INTEGER,
        points_for      INTEGER,
        points_against  INTEGER,
        points_diff     TEXT,
        points          INTEGER,
        scraped_date    TEXT,
        FOREIGN KEY (team_id)        REFERENCES teams (team_id),
        FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),
        UNIQUE (team_id, competition_id, scraped_date)
    )
"""

CREATE_MATCHES_SQL = """
    CREATE TABLE IF NOT EXISTS matches (
        match_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        competition_id  INTEGER NOT NULL,
        home_team       TEXT NOT NULL,
        away_team       TEXT NOT NULL,
        home_score      INTEGER,
        away_score      INTEGER,
        match_date      TEXT,
        FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),
        UNIQUE (competition_id, home_team, away_team, match_date)
    )
"""

CREATE_SCRAPE_LOG_SQL = """
    CREATE TABLE IF NOT EXISTS scrape_log (
        log_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        scraped_at      TEXT NOT NULL,
        records_found   INTEGER,
        status          TEXT
    )
"""

ALL_TABLES = [
    CREATE_TEAMS_SQL,
    CREATE_COMPETITIONS_SQL,
    CREATE_STANDINGS_SQL,
    CREATE_MATCHES_SQL,
    CREATE_SCRAPE_LOG_SQL,
]

# ── connection ────────────────────────────────────────────────────────────────


def create_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _execute(sql: str, params: tuple = ()) -> None:
    # runs a single write query using a context manager so the connection always closes
    with create_connection() as conn:
        try:
            conn.execute(sql, params)
            conn.commit()
        except sqlite3.Error as e:
            print(f"database error: {e}")


# ── setup ─────────────────────────────────────────────────────────────────────


def initialise_database() -> None:
    for sql in ALL_TABLES:
        _execute(sql)


# ── inserts ───────────────────────────────────────────────────────────────────


def insert_team(team_name: str, short_name, country, league) -> None:
    if not team_name:
        return
    _execute(
        "INSERT OR IGNORE INTO teams (team_name, short_name, country, league) VALUES (?, ?, ?, ?)",
        (team_name, short_name, country, league),
    )


def insert_competition(competition_name: str, competition_type: str, season) -> None:
    if not competition_name:
        return
    _execute(
        "INSERT OR IGNORE INTO competitions (competition_name, competition_type, season) VALUES (?, ?, ?)",
        (competition_name, competition_type, season),
    )


def insert_standing(
    team_id: int,
    competition_id: int,
    position: int,
    played: int,
    won: int,
    drawn: int,
    lost: int,
    points_for: int,
    points_against: int,
    points_diff: str,
    points: int,
    scraped_date: str,
) -> None:
    _execute(
        """
        INSERT OR IGNORE INTO standings
        (team_id, competition_id, position, played, won, drawn, lost,
         points_for, points_against, points_diff, points, scraped_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            team_id,
            competition_id,
            position,
            played,
            won,
            drawn,
            lost,
            points_for,
            points_against,
            points_diff,
            points,
            scraped_date,
        ),
    )


def insert_match(
    competition_id: int,
    home_team: str,
    away_team: str,
    home_score: int,
    away_score: int,
    match_date: str,
) -> None:
    _execute(
        """
        INSERT OR IGNORE INTO matches
        (competition_id, home_team, away_team, home_score, away_score, match_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (competition_id, home_team, away_team, home_score, away_score, match_date),
    )


def log_scrape(records_found: int, status: str) -> None:
    _execute(
        "INSERT INTO scrape_log (scraped_at, records_found, status) VALUES (?, ?, ?)",
        (datetime.now().strftime(TIMESTAMP_FORMAT), records_found, status),
    )


# ── queries ───────────────────────────────────────────────────────────────────


def get_team_id(team_name: str) -> int | None:
    with create_connection() as conn:
        row = conn.execute(
            "SELECT team_id FROM teams WHERE team_name = ?", (team_name,)
        ).fetchone()
    return row[0] if row else None


def get_known_match_ids(competition_id: int) -> set:
    with create_connection() as conn:
        try:
            rows = conn.execute(
                "SELECT home_team, away_team, match_date FROM matches WHERE competition_id = ?",
                (competition_id,),
            ).fetchall()
            return {(r[0], r[1], r[2]) for r in rows}
        except sqlite3.Error as e:
            print(f"error fetching known matches: {e}")
            return set()


def get_match_score(
    competition_id: int, home: str, away: str, match_date: str
) -> tuple:
    with create_connection() as conn:
        row = conn.execute(
            """
            SELECT home_score, away_score FROM matches
            WHERE competition_id = ? AND home_team = ? AND away_team = ? AND match_date = ?
            """,
            (competition_id, home, away, match_date),
        ).fetchone()
    return row if row else (0, 0)


if __name__ == "__main__":
    initialise_database()
    print("database ready!")
