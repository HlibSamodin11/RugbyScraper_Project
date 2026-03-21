import time

from rich.console import Console

from display.animations import print_animated_header
from display.constants import (
    BAR_CHART_WIDTH,
    TEAM_NAME_DISPLAY_LENGTH,
    TREND_GRAPH_HEIGHT,
)
from display.utils import clear_screen

console = Console()


def show_team_picker(standings: list) -> str | None:
    clear_screen()
    console.print("\n[bold green]  Select a team:[/bold green]\n")
    for i, row in enumerate(standings, 1):
        console.print(f"  [dim]{i}.[/dim]  {row['team_name']}")
    console.print("\n  [dim]0.  Cancel[/dim]")
    print("\n  > ", end="", flush=True)

    try:
        idx = int(input())
        if idx == 0:
            return None
        if 1 <= idx <= len(standings):
            return standings[idx - 1]["team_name"]
    except ValueError:
        pass
    return None


def _print_stats_card(team_data: dict) -> None:
    pd_val = team_data.get("points_diff", "0")
    pd_colour = "bold green" if str(pd_val).startswith("+") else "bold red"

    stats = [
        ("  Position", f"[bold yellow]{team_data['position']}[/bold yellow]", ""),
        ("  Played  ", str(team_data["played"]), ""),
        (
            "  Won     ",
            f"[bold green]{team_data['won']}[/bold green]",
            "█" * team_data["won"],
        ),
        (
            "  Drawn   ",
            f"[bold yellow]{team_data['drawn']}[/bold yellow]",
            "█" * team_data["drawn"],
        ),
        (
            "  Lost    ",
            f"[bold red]{team_data['lost']}[/bold red]",
            "█" * team_data["lost"],
        ),
        ("  PF      ", str(team_data.get("points_for", "N/A")), ""),
        ("  PA      ", str(team_data.get("points_against", "N/A")), ""),
        ("  PD      ", f"[{pd_colour}]{pd_val}[/{pd_colour}]", ""),
        ("  Points  ", f"[bold yellow]{team_data['points']}[/bold yellow]", ""),
    ]

    for label, value, bar in stats:
        console.print(f"[dim]{label}[/dim]  :  {value}  [green]{bar}[/green]")
        time.sleep(0.08)


def _print_comparison_chart(team_name: str, standings: list) -> None:
    console.print("\n  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
    console.print("  [bold green]  Points comparison — all teams[/bold green]")
    console.print("  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")
    time.sleep(0.2)

    max_pts = max(r["points"] for r in standings) if standings else 1

    for row in standings:
        is_selected = row["team_name"] == team_name
        is_first = row["position"] == 1
        is_last = row["position"] == len(standings)

        filled = int((row["points"] / max_pts) * BAR_CHART_WIDTH)
        empty = BAR_CHART_WIDTH - filled

        if is_selected:
            bar_colour, prefix = "bold yellow", "▶ "
        elif is_first:
            bar_colour, prefix = "bold green", "🏆"
        elif is_last:
            bar_colour, prefix = "bold red", "⬇ "
        else:
            bar_colour, prefix = "green", "  "

        name_padded = row["team_name"][:TEAM_NAME_DISPLAY_LENGTH].ljust(
            TEAM_NAME_DISPLAY_LENGTH
        )
        console.print(f"  {prefix} [bold]{name_padded}[/bold] ", end="")

        for _ in range(filled):
            console.print(f"[{bar_colour}]█[/{bar_colour}]", end="")
            time.sleep(0.01)

        console.print(f"[dim]{'░' * empty}[/dim] [bold]{row['points']}[/bold]")


def _print_trend_graph(history: list) -> None:
    console.print("\n  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
    console.print("  [bold green]  Points trend over time[/bold green]")
    console.print("  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")

    dates = [h["date"] for h in history]
    points = [h["points"] for h in history]
    positions = [h["position"] for h in history]
    max_pts = max(points)

    for row in range(TREND_GRAPH_HEIGHT, 0, -1):
        threshold = (row / TREND_GRAPH_HEIGHT) * max_pts
        line = f"  {int(threshold):>3} │"
        for pt in points:
            line += (
                " [bold green]█[/bold green] "
                if (pt / max_pts) * TREND_GRAPH_HEIGHT >= row
                else "   "
            )
        console.print(line)
        time.sleep(0.05)

    console.print("      └" + "───" * len(points))
    console.print(f"[dim]       {''.join(d[-5:] + ' ' for d in dates)}[/dim]")

    console.print("\n  [dim]Position trend:[/dim]  ", end="")
    for i in range(1, len(positions)):
        diff = positions[i - 1] - positions[i]
        if diff > 0:
            console.print("[bold green]▲[/bold green] ", end="")
        elif diff < 0:
            console.print("[bold red]▼[/bold red] ", end="")
        else:
            console.print("[dim]─[/dim] ", end="")
        time.sleep(0.1)
    console.print()


def show_team_graph(team_name: str, history: list, standings: list) -> None:
    clear_screen()

    team_data = next((r for r in standings if r["team_name"] == team_name), None)
    if not team_data:
        console.print("[red]  team not found[/red]")
        input("\n  press enter to go back...")
        return

    header = f"  ★  {team_name.upper()}  ★"
    border = "  " + "═" * (len(header) - 2)
    print_animated_header(header, border)
    console.print("\n")
    time.sleep(0.2)

    _print_stats_card(team_data)
    time.sleep(0.3)
    _print_comparison_chart(team_name, standings)

    if len(history) >= 2:
        time.sleep(0.3)
        _print_trend_graph(history)
    else:
        console.print(
            "\n  [dim]  run the scraper daily to unlock the points trend graph![/dim]"
        )

    console.print()
    input("  press enter to go back...")
