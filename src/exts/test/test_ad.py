import disnake
from src.ad import Ad
from src.bot import Universe


class TestAd(disnake.Cog):
    def __init__(self, bot: Universe) -> None:
        self.bot = bot

    @disnake.slash_command(name="test ad", description="A command to test Ad")
    async def test_ad(self, ctx: disnake.ApplicationCommandInteraction) -> None:
        await ctx.response.send_message("Test command executed.", embed=Ad())


async def setup(bot: Universe) -> None:
    bot.add_cog(TestAd(bot))
