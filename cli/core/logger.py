LINE = "=" * 50


def title(text: str) -> None:
    print()
    print(LINE)
    print(f" {text}")
    print(LINE)
    print()


def success(text: str) -> None:
    print(f"✔ {text}")


def warning(text: str) -> None:
    print(f"⚠ {text}")


def error(text: str) -> None:
    print(f"✖ {text}")


def info(text: str) -> None:
    print(f"• {text}")
    