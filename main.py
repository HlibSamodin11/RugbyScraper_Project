import os
import time

os.environ["TERM"] = "xterm"

from rich.console import Console

from competitions import COMPETITIONS
from database import get_known_match_ids, get_match_score, initialise_database
from display import (
    animate_exit,
    animate_logo,
    animate_menu,
    clear_screen,
    show_about,
    show_fixtures,
    show_loading_spinner,
    show_new_results_notification,
    show_results,
    show_standings,
    show_team_graph,
    show_team_picker,
)
from exporter import export_standings_to_csv
from scraper import (
    auto_scrape_all,
    fetch_espn_page,
    is_espn_reachable,
    parse_fixtures,
    parse_results,
    parse_standings,
    scrape_and_save,
)
from stats import build_form_data, get_team_history

console = Console()


# ── startup ───────────────────────────────────────────────────────────────────


def _snapshot_known_matches() -> dict:
    return {
        key: get_known_match_ids(int(key))
        for key, comp in COMPETITIONS.items()
        if comp["results_url"]
    }


def _find_new_results(known_before: dict) -> list:
    new_results = []
    for key, comp in COMPETITIONS.items():
        if not comp["results_url"]:
            continue
        known_after = get_known_match_ids(int(key))
        for home, away, match_date in known_after - known_before.get(key, set()):
            home_score, away_score = get_match_score(int(key), home, away, match_date)
            new_results.append(
                {
                    "competition": comp["name"],
                    "home": home,
                    "away": away,
                    "home_score": home_score,
                    "away_score": away_score,
                }
            )
    return new_results


def _run_startup_scrape() -> None:
    console.print("[dim green]  auto-scraping all competitions...[/dim green]")
    known_before = _snapshot_known_matches()
    scrape_results = auto_scrape_all(COMPETITIONS)
    success_count = sum(1 for v in scrape_results.values() if v.get("success"))
    console.print(
        f"[dim green]  scraped {success_count} competitions successfully[/dim green]"
    )
    new_results = _find_new_results(known_before)
    if new_results:
        show_new_results_notification(new_results)


# ── competition actions ───────────────────────────────────────────────────────


def _fetch_standings_and_form(comp: dict) -> tuple:
    show_loading_spinner(f"fetching {comp['name']} standings...")
    html = fetch_espn_page(comp["url"])
    standings = parse_standings(html)

    if not standings:
        return None, {}, []

    results = []
    form_data = {}
    if comp["results_url"]:
        show_loading_spinner(f"fetching {comp['name']} form...")
        results_html = fetch_espn_page(comp["results_url"])
        results = parse_results(results_html)
        form_data = build_form_data(standings, results)

    return standings, form_data, results


def _handle_export(choice: str, comp: dict) -> None:
    path = export_standings_to_csv(int(choice), comp["name"])
    if path:
        console.print(f"\n[green]  exported to {path}[/green]")
    else:
        console.print("\n[red]  nothing to export yet[/red]")
    console.input("\n[dim]  press enter to go back...[/dim]")


def _handle_results(comp: dict, choice: str, results: list) -> None:
    if not comp["results_url"]:
        clear_screen()
        console.print(
            f"\n[yellow]  no results available for {comp['name']} yet[/yellow]"
        )
        console.input("\n[dim]  press enter to go back...[/dim]")
        return
    if not results:
        results = parse_results(fetch_espn_page(comp["results_url"]))
    show_results(f"{comp['name']} {comp['season']}", results, choice)


def _handle_fixtures(comp: dict, choice: str) -> None:
    if not comp["results_url"]:
        clear_screen()
        console.print(
            f"\n[yellow]  no fixtures available for {comp['name']} yet[/yellow]"
        )
        console.input("\n[dim]  press enter to go back...[/dim]")
        return
    show_loading_spinner(f"fetching {comp['name']} fixtures...")
    fixtures = parse_fixtures(fetch_espn_page(comp["results_url"]))
    show_fixtures(f"{comp['name']} {comp['season']}", fixtures, choice)


def _handle_team_stats(standings: list, choice: str) -> None:
    team_name = show_team_picker(standings)
    if team_name:
        show_loading_spinner(f"loading {team_name} stats...")
        history = get_team_history(team_name, int(choice))
        show_team_graph(team_name, history, standings)


def handle_choice(choice: str) -> None:
    if choice not in COMPETITIONS:
        console.print("[red]  invalid choice, try again[/red]")
        return

    comp = COMPETITIONS[choice]

    if not comp["url"]:
        clear_screen()
        console.print(f"\n[yellow]  {comp['name']} is coming soon![/yellow]")
        console.input("\n[dim]  press enter to go back...[/dim]")
        return

    standings, form_data, results = _fetch_standings_and_form(comp)

    if not standings:
        console.print("[red]  couldn't load standings, try again later[/red]")
        console.input("\n[dim]  press enter to go back...[/dim]")
        return

    scrape_and_save(
        int(choice), comp["url"], comp["name"], comp["type"], comp["season"]
    )

    action = show_standings(
        f"{comp['name']} {comp['season']}", standings, choice, form_data
    )

    if action == "e":
        _handle_export(choice, comp)
    elif action == "r":
        _handle_results(comp, choice, results)
    elif action == "f":
        _handle_fixtures(comp, choice)
    elif action == "t":
        _handle_team_stats(standings, choice)


# ── entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    animate_logo()
    initialise_database()

    console.print("[dim]  checking connection...[/dim]")
    if not is_espn_reachable():
        console.print(
            "[red]  warning: ESPN appears to be unreachable. data may be outdated.[/red]"
        )
        time.sleep(2)
    else:
        _run_startup_scrape()

    while True:
        choice = animate_menu()
        if choice == "q":
            animate_exit()
            break
        elif choice == "a":
            show_about()
        else:
            handle_choice(choice)


if __name__ == "__main__":
    main()
