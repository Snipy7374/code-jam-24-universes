from __future__ import annotations

import logging
from typing import TYPE_CHECKING, override

import disnake
from disnake.ext import commands, tasks
from src.constants import EnvVars
from src.database import Database
from src.logger import setup_logging

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    from aiosqlite import Connection

__all__: tuple[str] = ("Universe",)

_log = logging.getLogger(__name__)


class FetchTasks:
    def __init__(self, bot: Universe) -> None:
        self.bot = bot

    async def _fetch_shoot_cmd(self) -> None:
        _log.info("Fetching shoot cmd")
        cmds = await self.bot.fetch_global_commands()
        for cmd in cmds:
            if cmd.name != "shoot":
                continue
            if isinstance(cmd, disnake.APISlashCommand):
                self.bot.shoot_cmd = cmd

        if self.bot.shoot_cmd is not None:
            _log.info("Shoot command fetched")

    @tasks.loop(seconds=1, count=1)
    async def fetch_cmd(self) -> None:
        await self.bot.wait_until_ready()
        await self._fetch_shoot_cmd()


class Universe(commands.InteractionBot):
    def __init__(self, loop: AbstractEventLoop, db_connection: Connection) -> None:
        super().__init__(
            intents=disnake.Intents.none(),
            loop=loop,
        )
        self.database = Database(connection=db_connection)
        self.shoot_cmd: disnake.APISlashCommand | None = None
        self.task_cmd = FetchTasks(self)

    async def on_ready(self) -> None:
        _log.info(f"Logged in as {self.user}")

        if not self.task_cmd.fetch_cmd.is_running():
            self.task_cmd.fetch_cmd.start()

    @override
    async def start(self) -> None:  # type: ignore[reportincomplatibleMethodOverride]
        setup_logging()
        _log.info("Loading extensions")
        self.load_extensions("./src/exts")
        _log.info("Extensions loading finished")
        await super().start(EnvVars.BOT_TOKEN, reconnect=True)
