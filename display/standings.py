import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from display.animations import animate_banner
from display.constants import (
    COMPETITION_DESCRIPTIONS,
    FORM_SYMBOLS,
    STANDINGS_KEY_FORM,
    STANDINGS_KEY_NARROW,
    STANDINGS_KEY_WIDE,
)
from display.utils import clear_screen, get_terminal_width, is_narrow

console = Console()


# ── formatting helpers ────────────────────────────────────────────────────────


def _format_pd(pd_val: str) -> str:
    if str(pd_val).startswith("+"):
        return f"[bold green]{pd_val}[/bold green]"
    if str(pd_val).startswith("-"):
        return f"[bold red]{pd_val}[/bold red]"
    return str(pd_val)


def _format_position(position: int, total: int) -> str:
    if position == 1:
        return f"🏆 {position}"
    if position == total:
        return f"⬇  {position}"
    return str(position)


def _get_row_style(position: int, total: int) -> str:
    if position == 1:
        return "bold yellow"
    if position <= 3:
        return "bold green"
    if position >= total:
        return "bold red"
    return "white"


def _format_form(form_list: list) -> str:
    return " ".join(FORM_SYMBOLS.get(r, "[dim]·[/dim]") for r in form_list)


# ── table builder ─────────────────────────────────────────────────────────────


def _build_standings_table(standings: list, form_data: dict, narrow: bool) -> Table:
    table = Table(border_style="green", header_style="bold green", show_lines=False)

    table.add_column("Pos", justify="center", width=6)
    table.add_column("Team", width=22)
    table.add_column("GP", justify="center", width=4)
    table.add_column("W", justify="center", width=4)
    table.add_column("D", justify="center", width=4)
    table.add_column("L", justify="center", width=4)

    if not narrow:
        table.add_column("PF", justify="center", width=5)
        table.add_column("PA", justify="center", width=5)
        table.add_column("PD", justify="center", width=6)

    table.add_column("Pts", justify="center", width=5)

    if form_data:
        table.add_column("Form", justify="left", width=16)

    total = len(standings)
    for row in standings:
        cells = [
            _format_position(row["position"], total),
            row["team_name"],
            str(row["played"]),
            str(row["won"]),
            str(row["drawn"]),
            str(row["lost"]),
        ]

        if not narrow:
            cells += [
                str(row.get("points_for", "")),
                str(row.get("points_against", "")),
                _format_pd(row.get("points_diff", "0")),
            ]

        cells.append(str(row["points"]))

        if form_data:
            cells.append(_format_form(form_data.get(row["team_name"], [])))

        table.add_row(*cells, style=_get_row_style(row["position"], total))

    return table


# ── public ────────────────────────────────────────────────────────────────────


def show_standings(
    competition_name: str,
    standings: list,
    competition_key: str = None,
    form_data: dict = None,
) -> str:
    clear_screen()
    narrow = is_narrow()

    if competition_key:
        animate_banner(competition_key)
        time.sleep(0.2)

    if competition_key and competition_key in COMPETITION_DESCRIPTIONS:
        console.print(
            Panel(
                COMPETITION_DESCRIPTIONS[competition_key],
                border_style="dim",
                padding=(0, 2),
                width=min(get_terminal_width() - 4, 62),
            )
        )
        time.sleep(0.1)

    console.print(f"\n  [bold green]{competition_name}[/bold green]\n")
    console.print(_build_standings_table(standings, form_data, narrow))

    key_text = STANDINGS_KEY_NARROW if narrow else STANDINGS_KEY_WIDE
    if form_data:
        key_text += STANDINGS_KEY_FORM

    console.print(
        Panel(
            key_text,
            title="[dim]Key[/dim]",
            border_style="dim",
            width=50,
            padding=(0, 2),
        )
    )
    console.print(f"[dim]  last updated: {time.strftime('%H:%M:%S')}[/dim]")

    print(
        "\n  enter to go back / e export / r results / f fixtures / t team stats > ",
        end="",
        flush=True,
    )
    return input()
