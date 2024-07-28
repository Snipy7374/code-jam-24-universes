from __future__ import annotations

import random
from typing import TYPE_CHECKING

import disnake
from disnake.ext import commands
from src.views.shoot import ShootMenu

if TYPE_CHECKING:
    from src.bot import Universe
    from src.views.shoot import ShootStats


__all__: tuple[str, ...] = (
    "generate_random_stats",
    "Minigames",
)


def _generate_fake_mac() -> str:
    tokens = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    seq = random.choices(tokens, k=16)  # noqa: S311
    return ":".join([f"{seq[i]}{seq[i+1]}" for i in range(0, len(seq), 2)])


def generate_random_stats(stats: ShootStats, *, skip_health: bool = False) -> None:
    for attr in stats.__dataclass_fields__:
        if attr in ("g_acc", "radians_angle", "ammunition", "angle", "total_shots", "hits"):
            continue

        if attr in ("enemy_position",):
            x = int(stats.calculate_shot_range())
            setattr(stats, attr, random.randint(x, x * 2 if x != 0 else 10))  # noqa: S311
            continue

        if attr in ("enemy_health",) and skip_health:
            setattr(stats, attr, random.randint(1, 20))  # noqa: S311
            continue

        setattr(stats, attr, int(random.random() * 100))  # noqa: S311


class Minigames(commands.Cog):
    def __init__(self, bot: Universe) -> None:
        self.bot = bot

    # disnake typing skill issue
    @commands.slash_command()  # type: ignore[reportUnknownMemberType]
    async def shoot(self, inter: disnake.GuildCommandInteraction) -> None:
        """Run an info overloaded shoot minigame."""
        player = await self.bot.database.fetch_player(inter.author.id)
        view = ShootMenu(inter.author, player)
        generate_random_stats(view.stats)
        embed = disnake.Embed(title="Shoot minigame", description="\n".join(["." * 10] * 5))
        embed.add_field("Planet acceleration", f"{round(view.stats.g_acc, 2)} m/s^2")
        embed.add_field("Position", f"{view.stats.position}")
        embed.add_field("Angle", f"{view.stats.angle}")
        embed.add_field("Ammunition (Shots left)", f"{view.stats.ammunition}")
        embed.add_field("Energy (Moves left)", f"{view.stats.energy}")
        embed.add_field("Ship Speed", f"{view.stats.ship_speed}")
        embed.add_field("Bullet Velocity", f"{view.stats.bullet_velocity}")
        embed.add_field("Bullet Type", f"{view.stats.bullet_type}")

        embed.add_field("Obstacles in range", f"{view.stats.obstacles_in_range}")
        embed.add_field("Outer Space Pression", "1.32 x 10^-11 Pa")

        embed.add_field("Enemy Position", f"{view.stats.enemy_position}")
        embed.add_field("Enemy Health", f"{view.stats.enemy_health}")
        embed.add_field("Enemy Energy", f"{view.stats.enemy_energy}")

        embed.add_field("Enemy has VIP Pass (+100 to Pay 2 Win)", f"{view.stats.enemy_has_vip_pass}")
        embed.add_field("Enemy logins in a row", f"{view.stats.enemy_logins_in_a_row}")

        embed.add_field("Ship insured", "Only below 0-e2 of skin damage")
        embed.add_field("Gun cleaned", f"{random.randint(1, 10_000)} days ago")  # noqa: S311
        embed.add_field("Engines checked", f"{random.randint(1, 100)} years ago")  # noqa: S311

        embed.add_field("Serial Number", f"10-{str(inter.user.id).replace('4', 'A').replace('3', 'E')}-A")
        # yeah you're basically fighting against yourself, enjoy it
        embed.add_field("Enemy Serial Number", f"10-{str(inter.user.id*3).replace('4', 'A').replace('3', 'E')}-A")
        embed.add_field("Manufacturer", "Legit Stuff™")
        embed.add_field("MAC address", _generate_fake_mac())
        embed.add_field(
            "Your stats",
            (
                f"Wins: {player.wins}\n"
                f"Losses: {player.loses}\n"
                f"Total Shots: {player.shots_fired}\n"
                f"Total Hits: {player.hits}\n"
                f"Total Shots Missed: {player.misses}\n"
            ),
        )
        embed.set_footer(text=f"Total shots: {view.stats.total_shots}")

        await inter.send(embed=embed, view=view)
        view.message = await inter.original_message()


def setup(bot: Universe) -> None:
    bot.add_cog(Minigames(bot))
