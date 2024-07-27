import asyncio

from src.bot import Universe
from src.database import setup_db


async def main() -> None:
    connection = await setup_db()
    bot = Universe(
        db_connection=connection,
    )
    try:
        await bot.start()
    finally:
        await bot.database.db_connection.close()


if __name__ == "__main__":
    asyncio.run(main())
