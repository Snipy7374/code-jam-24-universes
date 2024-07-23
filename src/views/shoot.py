from __future__ import annotations

import math

import disnake


class ShootMenu(disnake.ui.View):
    message: disnake.InteractionMessage
    angle_x: int = 0
    angle_y: int = 0

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
        await inter.send(
            f"You are taking your shot at degree {math.atan2(self.angle_x, self.angle_y) * (180 / math.pi)}",
            ephemeral=True,
        )

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="➡️", row=1)
    async def aim_right_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        self.angle_x += 1
        await self.update_angle(inter)
