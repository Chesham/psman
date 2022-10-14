from argparse import ArgumentParser
from datetime import datetime
import functools
import re

import psutil

from .filter import _process_filters, filter_cmdline, filter_name
from .action import _actions
from .logger import logger


_prog = "psman"
_version = "1.0.0"


def iter_process():
    for p in psutil.process_iter(["username"]):
        if any(not f(p) for f in _process_filters):
            continue
        yield p


def main():
    # Arguments
    parser = ArgumentParser(prog=_prog)
    parser.add_argument("--version", action="version", version=f"%(prog)s {_version}")
    parser.add_argument(
        "name", help="Name of target process, specify switch '--re' for regex"
    )
    parser.add_argument(
        "--re",
        action="store_true",
        help="Use regular expression for name of process",
    )
    parser.add_argument(
        "--case",
        action="store_true",
        default=False,
        help="Match name of process with case sensitive",
    )
    parser.add_argument(
        "--cmd-any",
        nargs="*",
        help="Match the command line of process for any arguments",
    )
    parser.add_argument(
        "--cmd-exact",
        nargs="*",
        help="Match the command line of process for exact arguments",
    )
    parser.add_argument(
        "--action",
        choices=_actions.keys(),
        help="Action will execute which process matched",
    )
    args = parser.parse_args()
    name = args.name
    action = _actions[args.action] if args.action else None
    cmd_any = args.cmd_any
    cmd_exact = args.cmd_exact
    _process_filters.append(
        functools.partial(
            filter_name,
            name=name,
            nocase=args.case,
            pattern=(
                re.compile(f"^{name}$", flags=re.IGNORECASE)
                if not args.case
                else re.compile(name)
            )
            if args.re
            else None,
        )
    )
    if cmd_any is not None or cmd_exact is not None:
        cmd_any = [j for i in cmd_any for j in i.split(" ") if j] if cmd_any else None
        cmd_exact = (
            [j for i in cmd_exact for j in i.split(" ") if j] if cmd_exact else None
        )
        _process_filters.append(
            functools.partial(filter_cmdline, cmd_any=cmd_any, cmd_exact=cmd_exact)
        )

    #  Iterate over processes
    for p in iter_process():
        try:
            if action:
                try:
                    sw = datetime.now()
                    action(p)
                except Exception as e:
                    logger.error(f"{action}({p})", exc_info=1)
                else:
                    logger.info(f"{action.__name__}({p.pid}) in {datetime.now() - sw}")
            else:
                logger.info(f"[{p.username()}] {p.pid} {p.name()}")
        except psutil.AccessDenied as e:
            logger.error("need privileges", exc_info=1)
            break


__all__ = [
    "_prog",
    "_version",
    "_actions",
    "logger",
    "_process_filters",
    iter_process.__name__,
]
