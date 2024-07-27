from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, ClassVar

import colorama
from src.constants import Config

if TYPE_CHECKING:
    from src.constants import LoggingLevel

__all__: tuple[str, ...] = ("setup_logging",)


def setup_logging() -> None:
    logger = logging.getLogger("disnake")
    logger.setLevel(Config.LOGGING_LEVEL)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

    for k, v in logger.manager.loggerDict.items():
        if k.startswith(("src", "__main__")) and isinstance(v, logging.Logger):
            v.setLevel(Config.LOGGING_LEVEL)
            v.addHandler(handler)


class LogFormatter(logging.Formatter):
    COLOR_MAP: ClassVar[dict[LoggingLevel, str]] = {
        logging.DEBUG: colorama.Fore.MAGENTA,
        logging.INFO: colorama.Fore.BLUE,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.BLACK,
    }

    def __init__(self) -> None:
        super().__init__("[%(asctime)s:%(levelname)s:%(name)s] | %(message)s")

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{self.COLOR_MAP.get(record.levelno)}{record.levelname}{colorama.Fore.RESET}"
        return super().format(record)
