import aiosqlite
from datetime import datetime, date
from __init__ import logger
import re


class DataHandler:
    def __init__(self):
        self.database_name = 'users_data.db'

    async def table_creation(self):
        async with aiosqlite.connect(self.database_name) as conn:
            try:
                cursor = await conn.cursor()
                await cursor.execute('''
                CREATE TABLE IF NOT EXISTS users_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    api_key TEXT NOT NULL
                )
                ''')
                await conn.commit()
                logger.info("Table 'users_data' created or already exists.")
                return True

            except aiosqlite.Error as e:
                logger.error(f"Failed to create table: {e}")
                return False

            except Exception as e:
                logger.critical(f"An unexpected error occurred: {e}")
                return False

    async def daily_upload_times_table_creation(self):
        async with aiosqlite.connect(self.database_name) as conn:
            try:
                cursor = await conn.cursor()
                await cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_upload_times (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    upload_time TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users_data (user_id)
                )
                ''')
                await conn.commit()
                logger.info("Table 'daily_upload_times' created or already exists.")
                return True

            except aiosqlite.Error as e:
                logger.error(f"Failed to create table: {e}")
                return False

            except Exception as e:
                logger.critical(f"An unexpected error occurred: {e}")
                return False

    async def upload_log_table_creation(self):
        async with aiosqlite.connect(self.database_name) as conn:
            try:
                cursor = await conn.cursor()
                await cursor.execute('''
                CREATE TABLE IF NOT EXISTS upload_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    upload_time TEXT NOT NULL,
                    date TEXT NOT NULL,
                    UNIQUE(user_id, upload_time, date),
                    FOREIGN KEY (user_id) REFERENCES users_data (user_id)
                )
                ''')
                await conn.commit()
                logger.info("Table 'upload_log' created or already exists.")
                return True

            except aiosqlite.Error as e:
                logger.error(f"Failed to create table: {e}")
                return False

            except Exception as e:
                logger.critical(f"An unexpected error occurred: {e}")
                return False

    async def add_user(self, **kwargs):
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                columns = ', '.join(kwargs.keys())
                placeholders = ', '.join(['?' for _ in kwargs])
                query = f'INSERT INTO users_data ({columns}) VALUES ({placeholders})'

                await cursor.execute(query, tuple(kwargs.values()))
                await conn.commit()
                logger.info(f"User {kwargs['user_id']} successfully added.")
                return True

        except aiosqlite.Error as e:
            logger.error(f"Failed to add user: {e}")
            return False

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

    async def update_user(self, user_id, table_name, **kwargs):
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                if any(isinstance(value, list) for value in kwargs.values()):

                    await cursor.execute(f'''
                                    DELETE FROM {table_name} WHERE user_id = ? AND upload_time IS NOT NULL
                                ''', (user_id,))
                    await conn.commit()
                    logger.info(f"All existing upload_time records for user {user_id} have been deleted.")

                    for key, values in kwargs.items():
                        for value in values:
                            await cursor.execute(f'''
                                            INSERT INTO {table_name} (user_id, {key})
                                            VALUES (?, ?)
                                        ''', (user_id, value))
                            await conn.commit()
                else:
                    set_clause = ', '.join(f'{key} = ?' for key in kwargs)
                    values = tuple(kwargs.values()) + (user_id,)

                    query = f'UPDATE {table_name} SET {set_clause} WHERE user_id = ?'

                    await cursor.execute(query, values)
                    await conn.commit()
                    logger.info(f"User {user_id} successfully updated.")

                return True

        except aiosqlite.Error as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            return False

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

    async def check_user(self, user_id):
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                query = 'SELECT user_id FROM users_data WHERE user_id = ?'

                result = await cursor.execute(query, (user_id,))
                user = await result.fetchone()

                logger.info(f"User {user_id} successfully checked.")

                return user is not None

        except aiosqlite.Error as e:
            logger.error(f"Failed to check user {user_id}: {e}")
            return False

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

