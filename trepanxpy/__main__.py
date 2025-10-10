"""A main program for trepan-xpy."""
import sys
from typing import List, Optional

import click

from trepanxpy.debugger import TrepanXPy
from trepanxpy.version import __version__


@click.command()
@click.version_option(__version__, "-V", "--version")
@click.option(
    "-X",
    "-v",
    "--trace",
    default=False,
    required=False,
    flag_value="trace",
    help="Run with instruction tracing, no interactive debugging (until post-mortem)",
)
@click.option(
    "-c", "--command-to-run", help="program passed in as a string", required=False
)
@click.option(
    "--style",
    required=False,
    default=None,
    help="Pygments style; 'none' uses 8-color rather than 256-color terminal",
)
@click.argument("path", nargs=1, type=click.Path(readable=True), required=False)
@click.argument("args", nargs=-1)
def main(
    trace: bool, command_to_run: str, style: Optional[str], path: str, args: List[str]
):
    # FIXME: This seems to be needed for pyficache to work on relative paths.
    # is this a bug?
    sys.path.append(".")

    is_file = True
    string_or_path = path
    if command_to_run:
        if path or args:
            print("You must pass either a file name or a command string, not both.")
            sys.exit(4)
        string_or_path = command_to_run
        is_file = False
    elif not path:
        print("You must pass either a file name or a command string, neither found.")
        sys.exit(4)

    TrepanXPy(string_or_path, is_file, trace_only=trace, style=style, args=args)


if __name__ == "__main__":
    main(auto_envvar_prefix="XPYTHON")
