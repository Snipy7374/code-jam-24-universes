from __future__ import annotations

import logging
from typing import override

import disnake
from disnake.ext import commands
from src.constants import EnvVars
from src.logger import setup_logging

__all__: tuple[str] = ("Universe",)

_log = logging.getLogger(__name__)


class Universe(commands.InteractionBot):
    def __init__(self) -> None:
        super().__init__(
            intents=disnake.Intents.none(),
        )

    async def on_ready(self) -> None:
        _log.info(f"Logged in as {self.user}")

    @override
    async def start(self) -> None:  # type: ignore[reportincomplatibleMethodOverride]
        setup_logging()
        self.load_extensions("./src/exts")
        await super().start(EnvVars.BOT_TOKEN, reconnect=True)
