import logging


class Formatter(logging.Formatter):
    default_time_format = '%H:%M:%S'
    default_msec_format = '%s.%03d'
    # Logger


logger = logging.Logger(__file__)
h = logging.StreamHandler()
h.setFormatter(
    Formatter(
        fmt="{asctime} [{levelname}] {message}",
        style="{",
    )
)
logger.addHandler(h)
