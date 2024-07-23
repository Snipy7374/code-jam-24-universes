from __future__ import annotations

import math

import disnake


class ShootMenu(disnake.ui.View):
    message: disnake.InteractionMessage
    angle_x: int = 0
    angle_y: int = 0
    position: int = 0
    angle: int = 0
    ammunition: int = 3  # shots left
    energy: int = 1  # moves left
    speed: int = 0
    velocity: int = 0
    bullet_type: str = "?"
    obstacles_in_range: int = 8
    fluff_stat_x: int = 1
    fluff_stat_y: int = 2
    fluff_stat_z: int = 3
    fluff_stat_a: int = 4
    enemy_position: int = 10
    enemy_health: int = 10
    enemy_energy: int = 5
    enemy_has_premium_skin: bool = False
    enemy_has_vip_pass: bool = False
    enemy_logins_in_a_row: int = 3
    total_shots: int = 0

    def __init__(self, author: disnake.Member) -> None:
        super().__init__(timeout=None)
        self.author = author

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if interaction.author == self.author:
            return True

        await interaction.send("This component is not for you!", ephemeral=True)
        return False

    async def update_angle(self, inter: disnake.MessageInteraction) -> None:
        await self.message.edit(
            embed=self.message.embeds[0].set_field_at(1, name="Angle", value=f"{self.angle_x}-{self.angle_y}"),
        )
        await inter.send(f"Your new angle is {self.angle_x}-{self.angle_y}", ephemeral=True)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="↖️", row=0)
    async def aim_up_left_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_y += 1
        self.angle_x -= 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="⬆️", row=0)
    async def aim_up_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_y += 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="↗️", row=0)
    async def aim_up_right_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_y += 1
        self.angle_x += 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="↙️", row=2)
    async def aim_down_left_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_y += 1
        self.angle_x += 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="⬇️", row=2)
    async def aim_down_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_y -= 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="↘️", row=2)
    async def aim_down_right_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_y += 1
        self.angle_x += 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="⬅️", row=1)
    async def aim_left_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_x -= 1
        await self.update_angle(inter)

    @disnake.ui.button(style=disnake.ButtonStyle.danger, label="Shoot", row=1)
    async def shoot_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        if self.ammunition != 0:
            self.ammunition -= 1
            self.total_shots += 1
            await inter.send(
                f"You are taking your shot at degree {math.atan2(self.angle_x, self.angle_y) * (180 / math.pi)}",
                ephemeral=True,
                embed=self.message.embeds[0]
                .set_field_at(2, name="Ammunition (Shots left)", value=self.ammunition - 1)
                .set_footer(text=f"Total Shots: {self.total_shots}"),
            )
        else:
            await inter.send("You can't shoot because you're out of ammunition.")

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="➡️", row=1)
    async def aim_right_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_x += 1
        await self.update_angle(inter)
