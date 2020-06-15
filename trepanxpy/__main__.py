"""A main program for trepan-xpy."""
import sys
import click
from typing import List

from trepanxpy.version import VERSION
from trepanxpy.debugger import TrepanXPy

@click.command()
@click.version_option(VERSION, "-V", "--version")
@click.option("-x", "--trace", default=False, required=False, flag_value="trace",
              help="Run with instruction tracing, no interactive debugging (until post-mortem)")
@click.option("-c", "--command-to-run",
              help="program passed in as a string", required=False)
@click.argument("path", nargs=1, type=click.Path(readable=True), required=False)
@click.argument("args", nargs=-1)
def main(trace: bool, path: str, command_to_run: str, args: List[str]):

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

    TrepanXPy(string_or_path, is_file, trace_only=trace, args=args)

if __name__ == "__main__":
    main(auto_envvar_prefix="XPYTHON")
