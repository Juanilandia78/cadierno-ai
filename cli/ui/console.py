import os
import sys
import re

plain_mode = os.getenv("CADIERNO_PLAIN") == "1" or os.getenv("NO_COLOR") is not None or os.getenv("CI") == "true" or os.getenv("TERM") == "dumb"

try:
    from rich.console import Console
    from rich.panel import Panel
    _rich = True
except ImportError:
    _rich = False


class _Fallback:
    def print(self, message="", **_kwargs):
        print(re.sub(r"\[/?[a-zA-Z ][^\]]*\]", "", str(message)))


console = Console(color_system="auto", force_terminal=None, no_color=plain_mode) if _rich else _Fallback()


def banner() -> None:
    if _rich and not plain_mode:
        console.print(Panel.fit("[bold cyan]CADIERNO AI[/]\n[dim]Context • Memory • Engineering[/]", border_style="cyan"))
    else:
        console.print("CADIERNO AI — Context • Memory • Engineering")


def success(message: str) -> None: console.print(f"[green]✓[/] {message}" if _rich else f"✓ {message}")
def info(message: str) -> None: console.print(f"[cyan]•[/] {message}" if _rich else f"• {message}")
def warning(message: str) -> None: console.print(f"[yellow]⚠[/] {message}" if _rich else f"⚠ {message}")
def error(message: str) -> None: console.print(f"[red]✖[/] {message}" if _rich else f"✖ {message}")
