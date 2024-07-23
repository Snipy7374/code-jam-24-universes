import asyncio

from src.bot import Universe


async def main() -> None:
    bot = Universe()
    await bot.database.init()
    try:
        await bot.start()
    finally:
        await bot.database.db_connection.close()


if __name__ == "__main__":
    asyncio.run(main())
