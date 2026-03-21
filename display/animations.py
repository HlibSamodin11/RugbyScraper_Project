import random
import time

from rich.console import Console

from display.constants import (
    ABOUT_LINE_DELAY,
    ABOUT_TEXT,
    BANNER_LINE_DELAY,
    COMPETITION_BANNERS,
    COMPETITION_COLOURS,
    GLITCH_CHAR_PROBABILITY,
    GLITCH_CHARS,
    GLITCH_FRAMES,
    GLITCH_LINE_LENGTH,
    GLITCH_LOGO_FRAMES,
    GLITCH_SHOW_PROBABILITY,
    LOGO,
    LOGO_LINE_DELAY,
    TAGLINE,
)
from display.utils import clear_screen

console = Console()


def _print_char_by_char(text: str, style: str, delay: float) -> None:
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print()


def print_animated_header(header: str, border: str) -> None:
    _print_char_by_char(border, "bold yellow", 0.01)
    _print_char_by_char(header, "bold yellow", 0.02)
    _print_char_by_char(border, "bold yellow", 0.01)


def _generate_glitch_frame() -> str:
    lines = [
        "".join(random.choice(GLITCH_CHARS) for _ in range(GLITCH_LINE_LENGTH))
        for _ in range(12)
    ]
    return "\n".join(lines)


def _glitch_logo_line(line: str) -> str:
    return "".join(
        c if random.random() > GLITCH_CHAR_PROBABILITY else random.choice(GLITCH_CHARS)
        for c in line
    )


def animate_logo() -> None:
    clear_screen()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
        time.sleep(LOGO_LINE_DELAY)
    console.print(TAGLINE, style="dim green")
    time.sleep(1.2)
    clear_screen()


def flicker() -> None:
    for _ in range(4):
        clear_screen()
        time.sleep(0.05)
        console.print("█" * 50, style="bold green")
        time.sleep(0.05)
    clear_screen()


def animate_exit() -> None:
    clear_screen()
    console.print("\n\n  [bold green]Thanks for visiting RugbyScraper 🏉[/bold green]")
    console.print("  [dim green]See you next time, HlibSamodin![/dim green]\n")
    time.sleep(1.0)

    for _ in range(GLITCH_FRAMES):
        clear_screen()
        colour = "green" if random.random() > GLITCH_CHAR_PROBABILITY else "red"
        console.print(_generate_glitch_frame(), style=f"bold {colour}")
        time.sleep(0.07)

    logo_lines = [line for line in LOGO.splitlines() if line.strip()]
    for _ in range(GLITCH_LOGO_FRAMES):
        clear_screen()
        for line in logo_lines:
            if random.random() > GLITCH_SHOW_PROBABILITY:
                console.print(_glitch_logo_line(line), style="bold green")
            else:
                console.print(" " * len(line))
        time.sleep(0.1)

    clear_screen()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
    console.print(TAGLINE, style="dim green")
    time.sleep(0.5)

    all_lines = LOGO.splitlines()
    for i in range(len(all_lines)):
        clear_screen()
        for line in all_lines[: len(all_lines) - i]:
            console.print(line, style="dim green")
        time.sleep(0.04)

    clear_screen()


def animate_banner(competition_key: str) -> None:
    if competition_key not in COMPETITION_BANNERS:
        return
    colour = COMPETITION_COLOURS.get(competition_key, "bold white")
    for line in COMPETITION_BANNERS[competition_key]:
        console.print(line, style=colour)
        time.sleep(BANNER_LINE_DELAY)


def show_about() -> None:
    clear_screen()
    for line in ABOUT_TEXT.splitlines():
        console.print(line, style="bold green")
        time.sleep(ABOUT_LINE_DELAY)
    console.input("\n[dim]  press enter to go back...[/dim]")
