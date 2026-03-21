import time

from rich.console import Console

from display.animations import print_animated_header
from display.constants import NOTIFICATION_BAR_LEN
from display.utils import clear_screen

console = Console()


def _determine_result_styles(home_score: int, away_score: int) -> tuple:
    if home_score > away_score:
        return "bold green", "dim white", "▶"
    if away_score > home_score:
        return "dim white", "bold green", "◀"
    return "bold yellow", "bold yellow", "═"


def _flash_header(header: str, border: str) -> None:
    for _ in range(2):
        clear_screen()
        time.sleep(0.06)
        console.print()
        for char in border:
            console.print(char, style="bold yellow", end="")
        console.print()
        for char in header:
            console.print(char, style="bold yellow", end="")
        console.print()
        for char in border:
            console.print(char, style="bold yellow", end="")
        console.print("\n")
        time.sleep(0.06)


def _print_result_row(
    r: dict, home_style: str, away_style: str, result_char: str
) -> None:
    home_score = int(r["home_score"])
    away_score = int(r["away_score"])
    console.print(f"  [dim]{r.get('competition', '')}[/dim]")
    console.print()
    console.print(
        f"  [{home_style}]{r['home']:>22}[/{home_style}]  "
        f"[bold yellow]{home_score:>2} {result_char} {away_score:<2}[/bold yellow]  "
        f"[{away_style}]{r['away']}[/{away_style}]"
    )
    console.print()


def _animate_result_bar() -> None:
    bar = ""
    for _ in range(NOTIFICATION_BAR_LEN):
        bar += "━"
        console.print(f"  [dim]{bar}[/dim]", end="\r")
        time.sleep(0.01)
    console.print()


def show_new_results_notification(new_results: list) -> None:
    if not new_results:
        return

    clear_screen()
    time.sleep(0.2)

    header = "  ★  NEW RESULTS  ★"
    border = "  " + "═" * (len(header) - 2)

    print_animated_header(header, border)
    console.print("\n")
    time.sleep(0.3)

    for r in new_results:
        home_score = int(r["home_score"])
        away_score = int(r["away_score"])
        home_style, away_style, result_char = _determine_result_styles(
            home_score, away_score
        )
        _flash_header(header, border)
        _print_result_row(r, home_style, away_style, result_char)
        _animate_result_bar()
        time.sleep(0.4)

    count = len(new_results)
    console.print(
        f"\n  [dim]{count} new result{'s' if count != 1 else ''} since last run[/dim]"
    )
    time.sleep(0.5)
    input("\n  press enter to continue...")
