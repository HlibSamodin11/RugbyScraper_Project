import os
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

console = Console()

LOGO = """
██████╗ ██╗   ██╗ ██████╗ ██████╗ ██╗   ██╗
██╔══██╗██║   ██║██╔════╝ ██╔══██╗╚██╗ ██╔╝
██████╔╝██║   ██║██║  ███╗██████╔╝ ╚████╔╝ 
██╔══██╗██║   ██║██║   ██║██╔══██╗  ╚██╔╝  
██║  ██║╚██████╔╝╚██████╔╝██████╔╝   ██║   
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝   ╚═╝   
███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
╚════██║██║     ██╔══██╗██╔══██╗██╔═══╝ ██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
"""

TAGLINE = "                                        by norvienne 🏉"

ABOUT_TEXT = """
╔════════════════════════════════════════════════════════╗
║                  ABOUT RUGBYSCRAPER                    ║
╚════════════════════════════════════════════════════════╝

  Built by norvienne — a 15 year old rugby fan who read
  Clean Code by Robert C. Martin and wanted to build
  something real to practice better coding.

  Rugby is my favourite sport so I built something I
  actually care about. This project scrapes live rugby
  data from ESPN and displays it in a clean terminal UI.

  github.com/norvienne
"""

# each entry: (menu key, region tag, display name)
COMPETITIONS = [
    ("1", "[EU]", "Six Nations"),
    ("2", "[GB]", "Premiership"),
    ("3", "[FR]", "Top 14"),
    ("4", "[WR]", "United Rugby Championship"),
    ("5", "[EU]", "Champions Cup"),
    ("6", "[WR]", "Rugby Championship"),
    ("7", "[WR]", "Rugby World Cup 2027  [soon]"),
]

# short description for each competition
COMPETITION_DESCRIPTIONS = {
    "1": "Annual competition between England, France, Ireland, Italy,\n"
    "  Scotland and Wales. One of rugby's oldest and most prestigious\n"
    "  tournaments, founded in 1883.",
    "2": "Top tier of English club rugby. The best clubs in England\n"
    "  compete across the season for the Premiership title.",
    "3": "The top professional rugby league in France, featuring\n"
    "  14 clubs competing for the Bouclier de Brennus since 1892.",
    "4": "Cross-border competition featuring clubs from Ireland, Italy,\n"
    "  Scotland, South Africa, Wales and Argentina. Formed in 2021.",
    "5": "Elite European club rugby competition. The top clubs from\n"
    "  across Europe compete for the most prestigious club trophy.",
    "6": "Annual southern hemisphere international competition between\n"
    "  Argentina, Australia, New Zealand and South Africa. Since 1996.",
    "7": "The biggest event in rugby union, held every 4 years.\n"
    "  The 2027 edition will be hosted in Australia.",
}

# colour per competition banner
COMPETITION_COLOURS = {
    "1": "bold cyan",
    "2": "bold red",
    "3": "bold blue",
    "4": "bold magenta",
    "5": "bold yellow",
    "6": "bold green",
    "7": "bold white",
}

# banners stored as lists of lines so we can animate them
COMPETITION_BANNERS = {
    "1": [
        "╔════════════════════════════════════════════════════════╗",
        "║             ★ ★ ★   SIX NATIONS   ★ ★ ★                ║",
        "║                EUROPE  •  SINCE 1883                   ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "2": [
        "╔════════════════════════════════════════════════════════╗",
        "║                   PREMIERSHIP RUGBY                    ║",
        "║                   ENGLAND  •  TIER 1                   ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "3": [
        "╔════════════════════════════════════════════════════════╗",
        "║                         TOP 14                         ║",
        "║                    FRANCE  •  TIER 1                   ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "4": [
        "╔════════════════════════════════════════════════════════╗",
        "║                UNITED RUGBY CHAMPIONSHIP               ║",
        "║                EUROPE & AFRICA  •  TIER 1              ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "5": [
        "╔════════════════════════════════════════════════════════╗",
        "║                 ★   CHAMPIONS CUP   ★                  ║",
        "║                   EUROPE  •  ELITE                     ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "6": [
        "╔════════════════════════════════════════════════════════╗",
        "║                 RUGBY CHAMPIONSHIP                     ║",
        "║             S.HEMISPHERE  •  SINCE 1996                ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "7": [
        "╔════════════════════════════════════════════════════════╗",
        "║              ★   RUGBY WORLD CUP 2027   ★              ║",
        "║               AUSTRALIA  •  COMING SOON                ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
}

GLITCH_CHARS = "▓▒░█▄▀■□▪▫╔╗╚╝║═╠╣╦╩╬░▒▓"


def clear_screen():
    os.system("clear")


def animate_logo():
    # types the logo line by line then clears before menu
    clear_screen()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
        time.sleep(0.1)
    console.print(TAGLINE, style="dim green")
    time.sleep(1.2)
    clear_screen()


def flicker():
    # CRT monitor turning on effect
    for _ in range(4):
        clear_screen()
        time.sleep(0.05)
        console.print("█" * 50, style="bold green")
        time.sleep(0.05)
    clear_screen()


def animate_exit():
    # mega glitch exit animation
    clear_screen()
    console.print("\n\n  [bold green]Thanks for visiting RugbyScraper 🏉[/bold green]")
    console.print("  [dim green]See you next time, norvienne![/dim green]\n")
    time.sleep(1.0)

    # glitch phase - random chars flood the screen
    for _ in range(10):
        clear_screen()
        lines = []
        for _ in range(12):
            line = "".join(random.choice(GLITCH_CHARS) for _ in range(56))
            lines.append(line)
        console.print(
            "\n".join(lines),
            style=f"bold {'green' if random.random() > 0.3 else 'red'}",
        )
        time.sleep(0.07)

    # logo flickers back in broken pieces
    logo_lines = [l for l in LOGO.splitlines() if l.strip()]
    for i in range(6):
        clear_screen()
        for j, line in enumerate(logo_lines):
            if random.random() > 0.4:
                glitched = "".join(
                    c if random.random() > 0.3 else random.choice(GLITCH_CHARS)
                    for c in line
                )
                console.print(glitched, style="bold green")
            else:
                console.print(" " * len(line))
        time.sleep(0.1)

    # final clean logo flash
    clear_screen()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
    console.print(TAGLINE, style="dim green")
    time.sleep(0.5)

    # fade out line by line
    logo_lines_full = LOGO.splitlines()
    for i in range(len(logo_lines_full)):
        clear_screen()
        for j, line in enumerate(logo_lines_full):
            if j < len(logo_lines_full) - i:
                console.print(line, style="dim green")
        time.sleep(0.04)

    clear_screen()


def animate_menu():
    # flicker then slide menu items in one by one
    flicker()
    time.sleep(0.1)

    menu_lines = []
    for key, flag, name in COMPETITIONS:
        menu_lines.append(f"  {key}.  {flag}  {name}")
    menu_lines.append("")
    menu_lines.append("  a.  About")
    menu_lines.append("  q.  Quit")

    printed = []
    for line in menu_lines:
        printed.append(line)
        clear_screen()
        console.print(
            Panel(
                "\n".join(printed),
                title="[bold green]Select Competition[/bold green]",
                border_style="green",
                padding=(1, 2),
                width=60,
            )
        )
        time.sleep(0.07)

    return console.input("\n[bold green]  >[/bold green] ")


def get_row_style(position, total_teams):
    # gold for 1st, green for top 3, red for last, white for middle
    if position == 1:
        return "bold yellow"
    elif position <= 3:
        return "bold green"
    elif position >= total_teams:
        return "bold red"
    else:
        return "white"


def animate_banner(competition_key):
    # typewriter effect with competition-specific colour
    if competition_key not in COMPETITION_BANNERS:
        return
    colour = COMPETITION_COLOURS.get(competition_key, "bold white")
    for line in COMPETITION_BANNERS[competition_key]:
        console.print(line, style=colour)
        time.sleep(0.08)


def show_about():
    # displays info about the project and author
    clear_screen()
    for line in ABOUT_TEXT.splitlines():
        console.print(line, style="bold green")
        time.sleep(0.05)
    console.input("\n[dim]  press enter to go back...[/dim]")


def show_standings(competition_name, standings, competition_key=None):
    # builds and prints the standings table with colour coded rows
    clear_screen()

    if competition_key:
        animate_banner(competition_key)
        time.sleep(0.2)

    # show competition description
    if competition_key and competition_key in COMPETITION_DESCRIPTIONS:
        console.print(
            Panel(
                f"  {COMPETITION_DESCRIPTIONS[competition_key]}",
                border_style="dim",
                padding=(0, 2),
                width=60,
            )
        )
        time.sleep(0.1)

    table = Table(
        title=f"[bold green]{competition_name}[/bold green]",
        border_style="green",
        header_style="bold green",
        show_lines=False,
    )

    table.add_column("Pos", justify="center", width=5)
    table.add_column("Team", width=20)
    table.add_column("GP", justify="center", width=5)
    table.add_column("W", justify="center", width=5)
    table.add_column("D", justify="center", width=5)
    table.add_column("L", justify="center", width=5)
    table.add_column("Pts", justify="center", width=5)

    total = len(standings)
    for row in standings:
        style = get_row_style(row["position"], total)
        table.add_row(
            str(row["position"]),
            row["team_name"],
            str(row["played"]),
            str(row["won"]),
            str(row["drawn"]),
            str(row["lost"]),
            str(row["points"]),
            style=style,
        )

    console.print(table)
    console.print(
        Panel(
            "[dim]GP[/dim]  Games Played\n"
            "[dim]W[/dim]   Won\n"
            "[dim]D[/dim]   Drawn\n"
            "[dim]L[/dim]   Lost\n"
            "[dim]Pts[/dim] Points",
            title="[dim]Note[/dim]",
            border_style="dim",
            width=30,
            padding=(0, 2),
        )
    )

    # returns "e" if user wants to export, anything else goes back
    return console.input(
        "\n[dim]  press enter to go back / e to export to csv...[/dim] "
    )


def show_loading_spinner(message="fetching data..."):
    # shows a spinner while fetching from ESPN
    with Live(Spinner("dots", text=f"[green]{message}[/green]"), refresh_per_second=10):
        time.sleep(2)
