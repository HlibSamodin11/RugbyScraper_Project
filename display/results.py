from rich import box
from rich.console import Console
from rich.table import Table

from display.constants import COMPETITION_COLOURS
from display.utils import clear_screen

console = Console()


def _get_result_styles(home_score: int, away_score: int) -> tuple:
    if home_score > away_score:
        return "bold green", "dim white"
    if away_score > home_score:
        return "dim white", "bold green"
    return "bold yellow", "bold yellow"


def show_results(
    competition_name: str,
    results: list,
    competition_key: str = None,
) -> None:
    colour = COMPETITION_COLOURS.get(competition_key or "", "bold white")
    clear_screen()
    console.print(f"\n[{colour}]  {competition_name} — Recent Results[/{colour}]\n")

    if not results:
        console.print("[dim]  no results found.[/dim]\n")
        input("\n  press enter to go back...")
        return

    table = Table(show_header=True, header_style=colour, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Date", style="dim", justify="left", width=12)
    table.add_column("Home", style="bold white", justify="right")
    table.add_column("Score", style="bold yellow", justify="center")
    table.add_column("Away", style="bold white", justify="left")

    for r in results:
        try:
            home_score = int(r["home_score"])
            away_score = int(r["away_score"])
        except (ValueError, KeyError):
            continue

        home_style, away_style = _get_result_styles(home_score, away_score)
        table.add_row(
            r.get("date", ""),
            f"[{home_style}]{r['home']}[/{home_style}]",
            f"{r['home_score']} - {r['away_score']}",
            f"[{away_style}]{r['away']}[/{away_style}]",
        )

    console.print(table)
    console.print("[dim]  winner shown in green[/dim]")
    input("\n  press enter to go back...")


def show_fixtures(
    competition_name: str,
    fixtures: list,
    competition_key: str = None,
) -> None:
    colour = COMPETITION_COLOURS.get(competition_key or "", "bold white")
    clear_screen()
    console.print(f"\n[{colour}]  {competition_name} — Upcoming Fixtures[/{colour}]\n")

    if not fixtures:
        console.print(
            "[dim]  no upcoming fixtures found — season may be complete.[/dim]\n"
        )
        input("\n  press enter to go back...")
        return

    table = Table(show_header=True, header_style=colour, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Date", style="dim", justify="left", width=14)
    table.add_column("Home", style="bold white", justify="right")
    table.add_column("Form", style="dim", justify="center", width=7)
    table.add_column("vs", style="dim", justify="center", width=4)
    table.add_column("Form", style="dim", justify="center", width=7)
    table.add_column("Away", style="bold white", justify="left")

    for f in fixtures:
        table.add_row(
            f.get("date", "TBC"),
            f["home"],
            f.get("home_form", ""),
            "vs",
            f.get("away_form", ""),
            f["away"],
        )

    console.print(table)
    input("\n  press enter to go back...")
