import csv
import os
from datetime import date

from database import create_connection

# ── constants ─────────────────────────────────────────────────────────────────

CSV_HEADERS = ["Team", "Position", "GP", "W", "D", "L", "PF", "PA", "PD", "Pts", "Date"]
EXPORTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "exports"
)

# ── helpers ───────────────────────────────────────────────────────────────────


def _fetch_latest_standings(competition_id: int) -> list:
    with create_connection() as conn:
        rows = conn.execute(
            """
            SELECT t.team_name, s.position, s.played, s.won, s.drawn, s.lost,
                   s.points_for, s.points_against, s.points_diff, s.points, s.scraped_date
            FROM standings s
            JOIN teams t ON s.team_id = t.team_id
            WHERE s.competition_id = ?
            AND s.scraped_date = (
                SELECT MAX(scraped_date) FROM standings WHERE competition_id = ?
            )
            ORDER BY s.position
            """,
            (competition_id, competition_id),
        ).fetchall()
    return rows


def _build_export_path(competition_name: str) -> str:
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    filename = (
        f"{competition_name.lower().replace(' ', '_')}_{date.today().isoformat()}.csv"
    )
    return os.path.join(EXPORTS_DIR, filename)


# ── public ────────────────────────────────────────────────────────────────────


def export_standings_to_csv(competition_id: int, competition_name: str) -> str | None:
    rows = _fetch_latest_standings(competition_id)

    if not rows:
        print(f"no standings found for {competition_name}")
        return None

    filepath = _build_export_path(competition_name)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        writer.writerows(rows)

    return filepath
