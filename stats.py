from database import create_connection

FORM_RESULTS_LIMIT = 5


def get_team_history(team_name: str, competition_id: int) -> list:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT s.position, s.points, s.scraped_date
            FROM standings s
            JOIN teams t ON s.team_id = t.team_id
            WHERE t.team_name = ?
            AND s.competition_id = ?
            ORDER BY s.scraped_date ASC
            """,
            (team_name, competition_id),
        )
        rows = cursor.fetchall()
    return [{"position": row[0], "points": row[1], "date": row[2]} for row in rows]


def _get_result_for_team(team_name: str, match: dict) -> str | None:
    # returns W, L, or D for a team in a single match — None if scores are invalid
    try:
        home_score = int(match["home_score"])
        away_score = int(match["away_score"])
    except ValueError:
        return None

    if match["home"] == team_name:
        if home_score > away_score:
            return "W"
        if home_score < away_score:
            return "L"
        return "D"

    if match["away"] == team_name:
        if away_score > home_score:
            return "W"
        if away_score < home_score:
            return "L"
        return "D"

    return None


def get_team_form(team_name: str, results: list) -> list:
    # returns last 5 results for a team as a list of W/L/D strings
    form = []
    for match in results:
        result = _get_result_for_team(team_name, match)
        if result:
            form.append(result)
    return form[-FORM_RESULTS_LIMIT:]


def build_form_data(standings: list, results: list) -> dict:
    # builds a dict mapping each team name to their form list
    return {
        row["team_name"]: get_team_form(row["team_name"], results) for row in standings
    }
