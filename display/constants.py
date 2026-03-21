# ── logo and branding ─────────────────────────────────────────────────────────

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

TAGLINE = "                                        by HlibSamodin 🏉"

ABOUT_TEXT = """
╔════════════════════════════════════════════════════════╗
║                  ABOUT RUGBYSCRAPER                    ║
╚════════════════════════════════════════════════════════╝

  Built by HlibSamodin — a 15 year old rugby fan who read
  Clean Code by Robert C. Martin and wanted to build
  something real to practice better coding.

  Rugby is my favourite sport so I built something I
  actually care about. This project scrapes live rugby
  data from ESPN and displays it in a clean terminal UI.

  github.com/HlibSamodin11
"""

GLITCH_CHARS = "▓▒░█▄▀■□▪▫╔╗╚╝║═╠╣╦╩╬░▒▓"

# ── timing ────────────────────────────────────────────────────────────────────

LOGO_LINE_DELAY = 0.1
MENU_LINE_DELAY = 0.07
BANNER_LINE_DELAY = 0.08
ABOUT_LINE_DELAY = 0.05
LOADING_DELAY = 2

# ── animation ─────────────────────────────────────────────────────────────────

GLITCH_FRAMES = 10
GLITCH_LOGO_FRAMES = 6
GLITCH_LINE_LENGTH = 56
GLITCH_CHAR_PROBABILITY = 0.3
GLITCH_SHOW_PROBABILITY = 0.4
NOTIFICATION_BAR_LEN = 40
SPINNER_REFRESH_RATE = 10

# ── layout ────────────────────────────────────────────────────────────────────

NARROW_TERMINAL_WIDTH = 100
DEFAULT_TERMINAL_WIDTH = 80
BAR_CHART_WIDTH = 35
TREND_GRAPH_HEIGHT = 8
TEAM_NAME_DISPLAY_LENGTH = 18

# ── menu ──────────────────────────────────────────────────────────────────────

MENU_COMPETITIONS = [
    ("1", "[EU]", "Six Nations"),
    ("2", "[GB]", "Premiership"),
    ("3", "[FR]", "Top 14"),
    ("4", "[WR]", "United Rugby Championship"),
    ("5", "[EU]", "Champions Cup"),
    ("6", "[WR]", "Rugby Championship"),
    ("7", "[WR]", "Rugby World Cup 2027"),
]

# ── competition info ──────────────────────────────────────────────────────────

COMPETITION_DESCRIPTIONS = {
    "1": "Annual competition between England, France, Ireland, Italy, Scotland and Wales.\nOne of rugby's oldest tournaments, founded in 1883.",
    "2": "Top tier of English club rugby. The best clubs in England\ncompete across the season for the Premiership title.",
    "3": "The top professional rugby league in France, featuring\n14 clubs competing for the Bouclier de Brennus since 1892.",
    "4": "Cross-border competition featuring clubs from Ireland, Italy,\nScotland, South Africa, Wales and Argentina. Formed in 2021.",
    "5": "Elite European club rugby competition. The top clubs from\nacross Europe compete for the most prestigious club trophy.",
    "6": "Annual southern hemisphere international competition between\nArgentina, Australia, New Zealand and South Africa. Since 1996.",
    "7": "The biggest event in rugby union, held every 4 years.\nThe 2027 edition will be hosted in Australia.",
}

COMPETITION_COLOURS = {
    "1": "bold cyan",
    "2": "bold red",
    "3": "bold blue",
    "4": "bold magenta",
    "5": "bold yellow",
    "6": "bold green",
    "7": "bold white",
}

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

# ── standings display ─────────────────────────────────────────────────────────

FORM_SYMBOLS = {
    "W": "[bold green]●[/bold green]",
    "L": "[bold red]●[/bold red]",
    "D": "[bold yellow]●[/bold yellow]",
}

STANDINGS_KEY_NARROW = (
    "[dim]GP[/dim] Played  [dim]W[/dim] Won  [dim]D[/dim] Drawn  "
    "[dim]L[/dim] Lost  [dim]Pts[/dim] Points"
)

STANDINGS_KEY_WIDE = (
    "[dim]GP[/dim] Played    [dim]PF[/dim] Points For\n"
    "[dim]W[/dim]  Won       [dim]PA[/dim] Points Against\n"
    "[dim]D[/dim]  Drawn     [dim]PD[/dim] Points Difference\n"
    "[dim]L[/dim]  Lost      [dim]Pts[/dim] League Points"
)

STANDINGS_KEY_FORM = (
    "\n[bold green]●[/bold green] Win  "
    "[bold red]●[/bold red] Loss  "
    "[bold yellow]●[/bold yellow] Draw"
)
