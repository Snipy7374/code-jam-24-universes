import os

import dotenv

type LoggingLevel = int | str
dotenv.load_dotenv()

__all__: tuple[str, ...] = (
    "EnvVars",
    "Config",
)


class EnvVars:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")


class Config:
    DEBUG: bool = True
    LOGGING_LEVEL: LoggingLevel = "INFO"
