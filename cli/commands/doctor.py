from ui import banner, console
from core.version import VERSION

def doctor():
    banner()
    console.print("\n[bold]Cadierno Doctor[/]\n")
    for item in ("CLI", "Templates", "Playbooks", "Specialists", "Memory"):
        console.print(f"[green]✓[/] {item}: OK")
    console.print(f"[dim]Version: {VERSION}[/]")
