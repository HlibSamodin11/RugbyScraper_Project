import time

from rich.console import Console
from rich.panel import Panel

from display.animations import flicker
from display.constants import MENU_COMPETITIONS, MENU_LINE_DELAY
from display.utils import clear_screen

console = Console()


def animate_menu() -> str:
    flicker()
    time.sleep(0.1)

    menu_lines = [f"  {key}.  {flag}  {name}" for key, flag, name in MENU_COMPETITIONS]
    menu_lines += ["", "  a.  About", "  q.  Quit"]

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
        time.sleep(MENU_LINE_DELAY)

    print("\n  > ", end="", flush=True)
    return input()
