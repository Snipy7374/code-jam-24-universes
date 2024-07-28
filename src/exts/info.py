from __future__ import annotations

from typing import TYPE_CHECKING

import disnake
from disnake.ext import commands

if TYPE_CHECKING:
    from src.bot import Universe


class InfoCommands(commands.Cog):
    def __init__(self, bot: Universe) -> None:
        self.bot = bot

    @commands.slash_command()
    async def about(self, inter: disnake.GuildCommandInteraction) -> None:
        """Provide information about the bot."""
        cmd = self.bot.shoot_cmd
        embed = disnake.Embed(
            title="About",
            description=(
                "This Discord bot was created by the "
                "Unique Universes team for the Python Discord Code Jam 2024.\n\n"
                "This bot's main feature is a 2D shooter minigame."
                f"{'Invoke </shoot:' + str(cmd.id) + '>' if cmd is not None else ''}"
            ),
            color=0x87CEEB,
        )
        embed.add_field(
            name="Team members",
            value="\\_\\_snipy__\nastroyo\nEarthKii\nMmesek\nnostradamus",
            inline=False,
        )
        embed.set_footer(text="Made by the Unique Universes team")
        await inter.send(embed=embed)


def setup(bot: Universe) -> None:
    bot.add_cog(InfoCommands(bot))
