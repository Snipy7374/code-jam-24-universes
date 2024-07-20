import disnake
from disnake.ext import commands
from src.ad import Ad
from src.bot import Universe


class TestAd(commands.Cog):
    def __init__(self, bot: Universe) -> None:
        self.bot = bot

    @commands.slash_command(name="test_ad", description="A command to test Ad")
    async def test_ad(self, ctx: disnake.ApplicationCommandInteraction) -> None:
        await ctx.response.send_message("Test command executed.", embed=Ad())


def setup(bot: Universe) -> None:
    bot.add_cog(TestAd(bot))
