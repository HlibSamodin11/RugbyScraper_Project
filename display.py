import time
from rich.console import Console
from rich.text import Text

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


def animate_logo():
    console.clear()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
        time.sleep(0.1)
    console.print(TAGLINE, style="dim green")
    time.sleep(1.2)


if __name__ == "__main__":
    animate_logo()
