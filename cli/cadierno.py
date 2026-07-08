#!/usr/bin/env python3

import argparse

from install import install
from bootstrap import bootstrap
from update import update
from doctor import doctor


def main():

    parser = argparse.ArgumentParser(
        prog="cadierno",
        description="Cadierno AI CLI"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("install")
    sub.add_parser("bootstrap")
    sub.add_parser("update")
    sub.add_parser("doctor")

    args = parser.parse_args()

    if args.command == "install":
        install()

    elif args.command == "bootstrap":
        bootstrap()

    elif args.command == "update":
        update()

    elif args.command == "doctor":
        doctor()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()