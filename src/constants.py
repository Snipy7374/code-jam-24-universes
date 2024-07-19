
from typing import TypeAlias

import os

import dotenv

LoggingLevel: TypeAlias = int | str
dotenv.load_dotenv()  # type: ignore

__all__: tuple[str, ...] = (
    "EnvVars",
    "Config",
)


class EnvVars:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN") or ""


class Config:
    DEBUG: bool = True
    LOGGING_LEVEL: LoggingLevel = "INFO"
