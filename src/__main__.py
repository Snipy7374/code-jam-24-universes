import asyncio

from src.bot import Universe


async def main() -> None:
    bot = Universe()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
