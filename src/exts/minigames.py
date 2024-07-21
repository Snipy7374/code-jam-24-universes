from __future__ import annotations

from typing import TYPE_CHECKING

import disnake
from disnake.ext import commands
from src.views.shoot import ShootMenu

if TYPE_CHECKING:
    from src.bot import Universe


class Minigames(commands.Cog):
    def __init__(self, bot: Universe) -> None:
        self.bot = bot

    @commands.slash_command()
    async def shoot(self, inter: disnake.GuildCommandInteraction) -> None:
        """Run an info overloaded shoot minigame."""
        embed = disnake.Embed(
            title="Shoot minigame",
        )
        view = ShootMenu(inter.author)
        await inter.send(embed=embed, view=view)
        view.message = await inter.original_message()


def setup(bot: Universe) -> None:
    bot.add_cog(Minigames(bot))
