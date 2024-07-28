from __future__ import annotations

import dataclasses
import math
import random
from asyncio import sleep
from typing import TYPE_CHECKING, cast

import disnake

# weird import but it's to avoid circular imports
import src.exts.minigames as games
from src.bot import Universe
from src.database import PlayerExistsError

if TYPE_CHECKING:
    from src.database import PlayerData


# acceleration directed to the center of Earth
# measured in m/s^2
EARTH_ACCELERATION = 9.81
# same thing, just for the moon
MOON_ACCELERATION = 1.62


class AngleModal(disnake.ui.Modal):
    def __init__(self, view: ShootMenu) -> None:
        self.view = view

        super().__init__(
            title="Angle Input",
            components=[
                disnake.ui.TextInput(
                    label="Angle degrees",
                    custom_id="angle_deg",
                    style=disnake.TextInputStyle.short,
                    placeholder="15",
                    value=str(self.view.stats.angle),
                    min_length=1,
                    max_length=3,
                ),
            ],
            timeout=180,
        )

    async def on_timeout(self) -> None:
        await self.view.on_timeout()
        self.view.stop()

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        angle = interaction.text_values["angle_deg"]
        if not angle.isdigit():
            return await interaction.send("Invalid input! You can type only numbers (e.g 10, 45 ...)", ephemeral=True)

        self.view.stats.angle = int(angle)
        await interaction.send(f"Your new angle is {angle}", ephemeral=True)
        return await self.view.update_message()


@dataclasses.dataclass
class ShootStats:
    position: int = 0
    angle: int = 15
    ammunition: int = 5  # shots left
    energy: int = 10  # angles adjustments left
    ship_speed: int = 0
    bullet_velocity: int = 0
    bullet_type: str = "?"
    obstacles_in_range: int = 8
    enemy_position: int = 10
    enemy_health: int = 10
    enemy_energy: int = 5
    enemy_has_vip_pass: bool = False
    enemy_logins_in_a_row: int = 3
    total_shots: int = 0
    hits: int = 0
    g_acc: float = dataclasses.field(
        default_factory=lambda: random.uniform(  # noqa: S311
            MOON_ACCELERATION,
            EARTH_ACCELERATION,
        ),
    )

    @property
    def misses(self) -> int:
        return self.total_shots - self.hits

    @property
    def angle_as_radians(self) -> float:
        return math.radians(self.angle)

    @property
    def get_enemy_distance(self) -> int:
        return abs(self.enemy_position - self.position)

    def calculate_shot_range(self) -> float:
        return (
            2 * self.bullet_velocity * math.cos(self.angle_as_radians) * math.sin(self.angle_as_radians)
        ) / self.g_acc

    def calculate_max_possible_range(self) -> float:
        return (self.bullet_velocity**2) / self.g_acc

    def calculate_flight_time(self) -> float:
        return (2 * self.bullet_velocity * math.sin(self.angle_as_radians)) / self.g_acc

    def calculate_max_height(self) -> float:
        return ((self.bullet_velocity**2) * (math.sin(self.angle_as_radians) ** 2)) / (2 * self.g_acc)

    @property
    def enemy_hitted(self) -> bool:
        return int(self.calculate_shot_range()) == self.enemy_position


class ShootMenu(disnake.ui.View):
    message: disnake.InteractionMessage

    def __init__(self, author: disnake.Member, player: PlayerData) -> None:
        super().__init__(timeout=None)
        self.author = author
        self.cached_player = player
        self.stats = ShootStats()

    async def on_timeout(self) -> None:
        # disnake typing skill issue
        for item in self.children:  # type: ignore[reportUnknownMemberType]
            item.disabled = True  # type: ignore[reportAttributeAccessIssue]
        await self.message.edit(
            embed=self.message.embeds[0].set_footer(text="View expired!!"),
            view=self,
        )

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if interaction.author == self.author:
            return True

        await interaction.send("This component is not for you!", ephemeral=True)
        return False

    async def update_angle(self, inter: disnake.MessageInteraction) -> None:
        await self.message.edit(
            embed=self.message.embeds[0].set_field_at(
                1,
                name="Angle",
                value=f"{self.stats.angle}",
            ),
        )
        await inter.send(f"Your new angle is {self.stats.angle}", ephemeral=True)

    async def update_message(self) -> None:
        # yk, black magic shit to not update the fields manually
        for field in self.message.embeds[0]._fields:  # type: ignore[reportPrivateUsage]
            # fields that shouldn't be updated
            if field["name"] in (
                "Outer Space Pression",
                "Ship insured",
                "Gun cleaned",
                "Engines checked",
                "Serial Number",
                "Enemy Serial Number",
                "Manufacturer",
                "MAC address",
                "Planet acceleration",
            ):
                continue

            field_name = field["name"]
            # fields whose name is different from the stats class
            # and as such needs a lil' transformation
            if field_name == "Your stats":
                field["value"] = (
                    f"Wins: {self.cached_player.wins}\n"
                    f"Losses: {self.cached_player.loses}\n"
                    f"Total Shots: {self.cached_player.shots_fired + self.stats.total_shots}\n"
                    f"Total Hits: {self.cached_player.hits + self.stats.hits}\n"
                    f"Total Shots Missed: {self.cached_player.misses + self.stats.misses}"
                )
                continue

            if field_name in (
                "Ammunition (Shots left)",
                "Energy (Moves left)",
                "Enemy has VIP Pass (+100 to Pay 2 Win)",
            ):
                field_name = field_name[: field_name.find("(") - 1]
            field["value"] = getattr(self.stats, field_name.lower().replace(" ", "_"))
        self.message.embeds[0].set_footer(text=f"Current Game Total Shots: {self.stats.total_shots}")
        await self.message.edit(embed=self.message.embeds[0], view=self)

    @disnake.ui.button(style=disnake.ButtonStyle.gray, label="Angle", disabled=True)
    async def angle_label(self, _: disnake.ui.Button[ShootMenu], __: disnake.MessageInteraction) -> None:
        # this button serves as a label
        return

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="➕")  # noqa: RUF001
    async def angle_plus(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        if self.stats.angle == 180:  # noqa: PLR2004
            self.stats.angle = 1
        else:
            self.stats.angle += 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.danger, emoji="➖")  # noqa: RUF001
    async def angle_minus(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        if self.stats.angle == 0:
            self.stats.angle = 179
        else:
            self.stats.angle -= 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.gray, label="Write angle")
    async def angle_in(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        await inter.response.send_modal(modal=AngleModal(self))

    async def stop_game(self) -> None:
        # we manually call the on timeout to disable the view
        await self.on_timeout()
        # cancel all scheduled timeout tasks and interaction listeners
        # for this view
        self.stop()

    @disnake.ui.button(style=disnake.ButtonStyle.danger, label="Shoot", row=1)
    async def shoot_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        bot = cast(Universe, inter.bot)

        try:
            player = await bot.database.create_player(inter.author.id)
        except PlayerExistsError:
            player = None

        if player is None:
            player = await bot.database.fetch_player(inter.author.id)

        if self.stats.ammunition != 0:
            self.stats.total_shots += 1
            self.stats.ammunition -= 1
            await inter.send(
                (
                    f"You are taking your shot at degree {int(self.stats.angle)} "
                    f"with a max height of {int(self.stats.calculate_max_height())} meters "
                    f"your shot will land at {int(self.stats.calculate_shot_range())} meters of distance "
                    f"flying for {round(self.stats.calculate_flight_time(), 2)} seconds."
                ),
                ephemeral=True,
            )
            await sleep(0.5)

            if self.stats.enemy_hitted:
                await inter.send(
                    (
                        "You hitted the enemy!! Decreasing enemy health, regenerating "
                        "5 energy and giving 1 ammunition as reward!"
                    ),
                    ephemeral=True,
                )
                self.stats.hits += 1
                self.stats.enemy_health -= 2
                self.stats.energy += 5
                self.stats.ammunition += 1

                if self.stats.enemy_health <= 0:
                    self.stats.enemy_health = 0
                    await self.stop_game()
                    await inter.send("You Won!!!!", ephemeral=True)
                    await bot.database.update_stats(
                        inter.author.id,
                        self.stats.total_shots,
                        self.stats.hits,
                        self.stats.misses,
                        player.wins + 1,
                        player.loses,
                    )
            else:
                await inter.send(
                    "Unfortunately you didn't hit the enemy!! Try to change the shoot angle!",
                    ephemeral=True,
                )
            # to make the game a little bit more enjoyable we change the stats every time the user shoot
            games.generate_random_stats(self.stats, skip_health=True)
            await self.update_message()

            if self.stats.ammunition == 0:
                await self.stop_game()
                await inter.send("Game Over :'(", ephemeral=True)
                await bot.database.update_stats(
                    inter.author.id,
                    self.stats.total_shots,
                    self.stats.hits,
                    self.stats.misses,
                    player.wins,
                    player.loses + 1,
                )
        else:
            await inter.send("You can't shoot because you're out of ammunition.")
