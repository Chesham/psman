import functools
import re
from typing import Callable

import psutil


_process_filters: list[Callable[[psutil.Process], bool]] = []


def filter_name(
    p: psutil.Process, *, name: str, nocase=True, pattern: re.Pattern = None
):
    if pattern:
        return pattern.match(p.name())
    else:
        if nocase:
            return p.name().lower() == name.lower()
        else:
            return p.name() == name


def filter_cmdline(p: psutil.Process, *, cmd_any=None, cmd_exact=None):
    cmds = set(p.cmdline()[1:])
    if cmd_any:
        if type(cmd_any) is not set:
            cmd_any = set(cmd_any)
        if any((i in cmds) for i in cmd_any):
            return True
    if cmd_exact:
        if type(cmd_exact) is not set:
            cmd_exact = set(cmd_exact)
        if all((i in cmds) for i in cmd_exact):
            return True
    return False
