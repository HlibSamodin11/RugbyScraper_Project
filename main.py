from display import (
    animate_logo,
    animate_menu,
    show_standings,
    show_loading_spinner,
    show_about,
    clear_screen,
    animate_exit,
)
from scraper import fetch_espn_page, parse_standings, scrape_and_save
from competitions import COMPETITIONS
from database import initialise_database
from exporter import export_standings_to_csv
from rich.console import Console

console = Console()


def handle_choice(choice):
    if choice not in COMPETITIONS:
        console.print("[red]  invalid choice, try again[/red]")
        return

    comp = COMPETITIONS[choice]

    if comp["url"] is None:
        clear_screen()
        console.print(f"\n[yellow]  {comp['name']} is coming soon![/yellow]")
        console.input("\n[dim]  press enter to go back...[/dim]")
        return

    show_loading_spinner(f"fetching {comp['name']} standings...")
    html = fetch_espn_page(comp["url"])
    standings = parse_standings(html)

    if not standings:
        console.print("[red]  couldn't load standings, try again later[/red]")
        console.input("\n[dim]  press enter to go back...[/dim]")
        return

    scrape_and_save(
        int(choice), comp["url"], comp["name"], comp["type"], comp["season"]
    )

    result = show_standings(f"{comp['name']} {comp['season']}", standings, choice)
    if result == "e":
        path = export_standings_to_csv(int(choice), comp["name"])
        if path:
            console.print(f"\n[green]  exported to {path}[/green]")
        else:
            console.print("\n[red]  nothing to export yet[/red]")
        console.input("\n[dim]  press enter to go back...[/dim]")


def main():
    animate_logo()
    initialise_database()

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
