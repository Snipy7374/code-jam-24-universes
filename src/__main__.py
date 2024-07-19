import asyncio

from src.bot import Universe
from src.constants import EnvVars


async def main() -> None:
    bot = Universe()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
