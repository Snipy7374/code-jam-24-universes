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
        await super().start(EnvVars.BOT_TOKEN, reconnect=True)


bot = Universe()


@bot.slash_command(
    name="about",
    description="Provides information about the bot's creators, its purpose, and its version",
)
async def about(interaction: disnake.ApplicationCommandInteraction) -> None:
    embed_dict = {
        "title": "About",
        "description": (
            "This Discord bot was created by the "
            "Unique Universes team for the Python Discord Code Jam 2024.\n\n"
            "This bot's main feature is a 2D shooter minigame."
        ),
        "color": 0x87CEEB,
        "fields": [
            {
                "name": "Team members",
                "value": ("\\_\\_snipy\\_\\_\nastroyo\nEarthKii\nMmesek\nnostradamus"),
                "inline": False,
            },
            {
                "name": "Version",
                "value": "-----TODO-----",
                "Inline": False,
            },
        ],
        "footer": {"text": "Made by the Unique Universes team"},
    }
    await interaction.response.send_message(embed=disnake.Embed.from_dict(embed_dict))


bot.run()
