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
        embed.add_field("Position", f"{ShootMenu.position}")
        embed.add_field("Angle", f"{ShootMenu.angle}")
        embed.add_field("Ammunition (Shots left)", f"{ShootMenu.ammunition}")
        embed.add_field("Energy (Moves left)", f"{ShootMenu.energy}")
        embed.add_field("Speed", f"{ShootMenu.speed}")
        embed.add_field("Velocity", f"{ShootMenu.velocity}")
        embed.add_field("Bullet Type", f"{ShootMenu.bullet_type}")

        embed.add_field("Obstacles in range", f"{ShootMenu.obstacles_in_range}")
        embed.add_field("Fluff Stat X", f"{ShootMenu.fluff_stat_x}")
        embed.add_field("Fluff Stat Y", f"{ShootMenu.fluff_stat_y}")
        embed.add_field("Fluff Stat Z", f"{ShootMenu.fluff_stat_z}")
        embed.add_field("Fluff Stat A", f"{ShootMenu.fluff_stat_a}")

        embed.add_field("Enemy Position", f"{ShootMenu.enemy_position}")
        embed.add_field("Enemy Health", f"{ShootMenu.enemy_health}")
        embed.add_field("Enemy Energy", f"{ShootMenu.enemy_energy}")

        embed.add_field("Enemy has Premium Skin (+10 to dodge)", f"{ShootMenu.enemy_has_premium_skin}")
        embed.add_field("Enemy has bought VIP Pass (+100 to Pay 2 Win)", f"{ShootMenu.enemy_has_vip_pass}")
        embed.add_field("Enemy has logins in a row", f"{ShootMenu.enemy_logins_in_a_row}")

        embed.add_field("Ship insured", "Only below 0-e2 of skin damage")
        embed.add_field("Gun cleaned", "7 days ago")
        embed.add_field("Engines checked", "10 years ago")

        embed.add_field("Serial Number", f"10-{str(inter.user.id).replace('4', 'A').replace('3', 'E')}-A")
        embed.add_field("Enemy Serial Number", f"10-{str(inter.user.id*3).replace('4', 'A').replace('3', 'E')}-A")
        embed.add_field("Manufacturer", "Legit Stuff™")
        embed.add_field("MAC address", "02:4C:90:12:34:56")
        embed.set_footer(text=f"Total shots: {ShootMenu.total_shots}")

        view = ShootMenu(inter.author)
        await inter.send(embed=embed, view=view)
        view.message = await inter.original_message()


def setup(bot: Universe) -> None:
    bot.add_cog(Minigames(bot))
