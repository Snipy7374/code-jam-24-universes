import sqlite3
from pathlib import Path

import aiosqlite


class PlayerData:
    def __init__(self, data: tuple) -> None:
        self._raw_data = data
        self.user_id = data[0]
        self.shots_fired = data[1]
        self.hits = data[2]
        self.misses = data[3]
        self.wins = data[4]
        self.loses = data[5]


class PlayerNotFoundError(LookupError): ...


class PlayerExistsError(NameError): ...


class UnknownValueError(TypeError): ...


class Database:
    def __init__(self) -> None:
        self._db_connection: aiosqlite.Connection

    @property
    def db_connection(self) -> aiosqlite.Connection:
        return self._db_connection

    async def init(self) -> None:
        if not Path("build").is_dir():
            Path("./build").mkdir()
        connection = await aiosqlite.connect("./build/database.db")
        async with connection.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS players_data (
                    _id int PRIMARY KEY,
                    shots_fired int DEFAULT 0,
                    hits int DEFAULT 0,
                    misses int DEFAULT 0,
                    wins int DEFAULT 0,
                    loses int DEFAULT 0
                )
            """)
        self._db_connection = connection

    async def execute(self, sql: str, *args: str | int) -> None:
        """Execute an sql statement."""
        async with self.db_connection.cursor() as cursor:
            await cursor.execute(sql, args)
            await self.db_connection.commit()

    async def fetch(self, sql: str, *args: str | int) -> tuple:
        """Execute a sql statement and fetch the first row."""
        async with self.db_connection.cursor() as cursor:
            await cursor.execute(sql, args)
            await self.db_connection.commit()
            return await cursor.fetchone()

    async def fetchmany(self, sql: str, *args: str | int, rows: int) -> list[tuple]:
        """Execute a sql statement and fetch the first x number of rows."""
        async with self.db_connection.cursor() as cursor:
            await cursor.execute(sql, args)
            await self.db_connection.commit()
            return await cursor.fetchmany(rows)

    async def fetchall(self, sql: str, *args: str | int) -> list[tuple]:
        """Execute a sql statement and fetch all rows."""
        async with self.db_connection.cursor() as cursor:
            await cursor.execute(sql, args)
            await self.db_connection.commit()
            return await cursor.fetchall()

    async def create_player(self, user_id: int) -> PlayerData:
        """Create a row for a player in the database using user id."""
        try:
            await self.execute("INSERT INTO players_data (_id) VALUES (?)", user_id)
        except sqlite3.IntegrityError as error:
            error_message = "Player Already Exists"
            raise PlayerExistsError(error_message) from error
        await self.db_connection.commit()
        return await self.fetch_player(user_id)

    async def fetch_player(self, user_id: int) -> PlayerData:
        """Fetch the data for a player in the database using user id.

        raises PlayerNotFoundError
        """
        data = await self.fetch("SELECT * FROM players_data WHERE _id=?", user_id)
        if data is None:
            error_message = "Create an entry for the player first"
            raise PlayerNotFoundError(error_message)
        return PlayerData(data)

    async def delete_player(self, user_id: int) -> None:
        """Delete the player data from the database."""
        await self.fetch_player(user_id)
        await self.execute("DELETE FROM players_data WHERE _id=?", user_id)

    async def increase(self, user_id: int, value_name: str) -> None:
        """Increase a certain value in the players data."""
        data = await self.fetch_player(user_id)
        try:
            value_data = getattr(data, value_name)
        except Exception as error:
            error_message = (
                "What value are you trying to change? These are available: shots_fired, hits, misses, wins, loses"
            )
            raise UnknownValueError(error_message) from error
        await self.execute("UPDATE players_data SET ?=? WHERE _id=?", value_name, value_data + 1, user_id)

    async def decrease(self, user_id: int, value_name: str) -> None:
        """Decrease a certain value in the players data."""
        data = await self.fetch_player(user_id)
        try:
            value_data = getattr(data, value_name)
        except Exception as error:
            error_message = (
                "What value are you trying to change? These are available: shots_fired, hits, misses, wins, loses"
            )
            raise UnknownValueError(error_message) from error
        await self.execute("UPDATE players_data SET ?=? WHERE _id=?", value_name, value_data - 1, user_id)
