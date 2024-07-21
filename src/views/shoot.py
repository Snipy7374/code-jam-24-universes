from __future__ import annotations

import disnake


class ShootMenu(disnake.ui.View):
    message: disnake.InteractionMessage

    def __init__(self, author: disnake.Member) -> None:
        super().__init__(timeout=10)
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

    @disnake.ui.button(style=disnake.ButtonStyle.danger, label="Shoot")
    async def shoot_callback(self, _: disnake.ui.Button[ShootMenu], inter: disnake.MessageInteraction) -> None:
        await inter.send("Sus", ephemeral=True)
