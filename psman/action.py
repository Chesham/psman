import os
import signal
import sys

import psutil


def kill_process(p: psutil.Process):
    return os.kill(
        p.pid, (signal.SIGTERM if sys.platform == "win32" else signal.SIGKILL)
    )


_actions = {"kill": kill_process}
