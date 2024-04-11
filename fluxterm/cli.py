#!/usr/bin/env python
import argparse
import sys

import fluxterm
from fluxterm.app import Fluxterm


def get_parser():
    parser = argparse.ArgumentParser(
        description="FluxTerm",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="show software version.",
        default=False,
        action="store_true",
    )

    subparsers = parser.add_subparsers(
        help="actions",
        title="actions",
        description="actions",
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", description="show software version")

    # List installed modules
    subparsers.add_parser(
        "start",
        formatter_class=argparse.RawTextHelpFormatter,
        description="start fluxterm",
    )
    return parser


def run_fluxterm():
    """
    run_fluxterm is the entrypoint!
    """
    parser = get_parser()

    def help(return_code=0):
        version = fluxterm.__version__

        print("\nFluxterm v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, _ = parser.parse_known_args()

    # Show the version and exit
    if args.command == "version" or args.version:
        print(fluxterm.__version__)
        sys.exit(0)

    # We don't do anything different for start, but added as a TBA
    # for arguments, maybe.
    start()


def start():
    app = Fluxterm()
    app.run()


if __name__ == "__main__":
    run_fluxterm()
