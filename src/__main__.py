import asyncio
import logging

from src.bot import Universe
from src.database import setup_db

_log = logging.getLogger(__name__)


async def start_bot(bot: Universe) -> None:
    try:
        await bot.start()
    except KeyboardInterrupt:
        pass
    finally:
        if not bot.is_closed():
            await bot.close()


async def close_db(bot: Universe) -> None:
    _log.info("Closing DB connection")
    await bot.database.db_connection.close()
    _log.info("DB connection closed")


def cancel_tasks(loop: asyncio.AbstractEventLoop) -> None:
    _log.info("Cancelling all the tasks")
    tasks = {task for task in asyncio.all_tasks(loop) if not task.done()}
    for task in tasks:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    _log.info("Tasks cancelled")


async def close_bot(bot: Universe) -> None:
    _log.info("Closing the Bot")
    await bot.close()
    _log.info("Bot successfully closed")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db_conn = loop.run_until_complete(setup_db())
    bot = Universe(loop, db_conn)

    try:
        loop.run_until_complete(start_bot(bot))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(close_db(bot))
        cancel_tasks(loop)
        loop.run_until_complete(close_bot(bot))
        loop.close()
