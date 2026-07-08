#!/usr/bin/env python3

import argparse

from install import install
from bootstrap import bootstrap
from update import update
from doctor import doctor

VERSION = "0.1.0"


def main():
    parser = argparse.ArgumentParser(
        prog="cadierno",
        description="Cadierno AI CLI"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Cadierno AI {VERSION}"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("install", help="Instala Cadierno AI en un proyecto")
    sub.add_parser("bootstrap", help="Analiza un proyecto")
    sub.add_parser("doctor", help="Diagnostica el proyecto")
    sub.add_parser("update", help="Actualiza Cadierno AI")

    args = parser.parse_args()

    if args.command == "install":
        install()

    elif args.command == "bootstrap":
        bootstrap()

    elif args.command == "doctor":
        doctor()

    elif args.command == "update":
        update()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()