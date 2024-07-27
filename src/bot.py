from __future__ import annotations

import logging
from typing import TYPE_CHECKING, override

import disnake
from disnake.ext import commands
from src.constants import EnvVars
from src.database import Database
from src.logger import setup_logging

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from aiosqlite import Connection

__all__: tuple[str] = ("Universe",)

_log = logging.getLogger(__name__)


class Universe(commands.InteractionBot):
    def __init__(self, loop: AbstractEventLoop, db_connection: Connection) -> None:
        super().__init__(
            intents=disnake.Intents.none(),
            loop=loop,
        )
        self.database = Database(connection=db_connection)

    async def on_ready(self) -> None:
        _log.info(f"Logged in as {self.user}")

    @override
    async def start(self) -> None:  # type: ignore[reportincomplatibleMethodOverride]
        setup_logging()
        _log.info("Loading extensions")
        self.load_extensions("./src/exts")
        _log.info("Extensions loading finished")
        await super().start(EnvVars.BOT_TOKEN, reconnect=True)
