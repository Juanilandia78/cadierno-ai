#!/usr/bin/env python3

import argparse

from commands.install import install
from commands.bootstrap import bootstrap
from commands.update import update
from commands.doctor import doctor

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

    # install
    install_parser = sub.add_parser(
        "install",
        help="Instala Cadierno AI en un proyecto"
    )

    install_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    # bootstrap
    bootstrap_parser = sub.add_parser(
        "bootstrap",
        help="Analiza un proyecto"
    )

    bootstrap_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    # doctor
    sub.add_parser(
        "doctor",
        help="Diagnostica Cadierno AI"
    )

    # update
    update_parser = sub.add_parser(
        "update",
        help="Actualiza Cadierno AI"
    )

    update_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Ruta del proyecto"
    )

    args = parser.parse_args()

    if args.command == "install":
        install(args.path)

    elif args.command == "bootstrap":
        bootstrap(args.path)

    elif args.command == "doctor":
        doctor()

    elif args.command == "update":
        update(args.path)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()