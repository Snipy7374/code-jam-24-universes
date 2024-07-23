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
        embed = disnake.Embed(title="Shoot minigame", description="\n".join(["." * 10] * 5))
        embed.add_field("Position", "0")
        embed.add_field("Angle", "0")
        embed.add_field("Ammunition (Shots left)", "1")
        embed.add_field("Energy (Moves left)", "1")
        embed.add_field("Speed", "0")
        embed.add_field("Velocity", "0")
        embed.add_field("Bullet Type", "?")

        embed.add_field("Obstacles in range", "8")
        embed.add_field("Fluff Stat X", "1")
        embed.add_field("Fluff Stat Y", "2")
        embed.add_field("Fluff Stat Z", "3")
        embed.add_field("Fluff Stat A", "4")

        embed.add_field("Enemy Position", "10")
        embed.add_field("Enemy Health", "10")
        embed.add_field("Enemy Energy", "5")

        embed.add_field("Enemy has Premium Skin (+10 to dodge)", "False")
        embed.add_field("Enemy has bought VIP Pass (+100 to Pay 2 Win)", "Unknown")
        embed.add_field("Enemy has logins in a row", "3")

        embed.add_field("Ship insured", "Only below 0-e2 of skin damage")
        embed.add_field("Gun cleaned", "7 days ago")
        embed.add_field("Engines checked", "10 years ago")

        embed.add_field("Serial Number", f"10-{str(inter.user.id).replace('4', 'A').replace('3', 'E')}-A")
        embed.add_field("Enemy Serial Number", f"10-{str(inter.user.id*3).replace('4', 'A').replace('3', 'E')}-A")
        embed.add_field("Manufacturer", "Legit Stuff™")
        embed.add_field("MAC address", "02:4C:90:12:34:56")
        embed.set_footer(text="Total shots: 0")

        view = ShootMenu(inter.author)
        await inter.send(embed=embed, view=view)
        view.message = await inter.original_message()


def setup(bot: Universe) -> None:
    bot.add_cog(Minigames(bot))
