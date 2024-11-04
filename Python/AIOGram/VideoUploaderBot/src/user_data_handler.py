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

    async def setup_user_schedule(self, user_id, daily_upload_times=None):
        if daily_upload_times is not None:
            daily_times = []
            for time_str in daily_upload_times:
                if not await self.date_time_validation(time_str):
                    return False
                daily_times.append(time_str)
            if await self.update_user(user_id=user_id, table_name='daily_upload_times', upload_time=daily_times):
                return True
            else:
                return False

    async def get_users_to_upload(self, now_time, now_date):
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                current_time = now_time
                today_date = now_date

                query = '''
                SELECT DISTINCT dt.user_id
                FROM daily_upload_times dt
                LEFT JOIN upload_log ul
                ON dt.user_id = ul.user_id AND dt.upload_time = ul.upload_time AND ul.date = ?
                WHERE dt.upload_time = ? AND ul.id IS NULL
                '''

                result = await cursor.execute(query, (today_date, current_time))
                users_to_upload = await result.fetchall()

                logger.info(f"Found {len(users_to_upload)} users scheduled for upload at {current_time}.")
                return [user[0] for user in users_to_upload]

        except aiosqlite.Error as e:
            logger.error(f"Failed to fetch users to upload: {e}")
            return []

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return []

    async def log_upload(self, user_id, upload_time):
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                today_date = date.today().isoformat()

                await cursor.execute('''
                INSERT OR IGNORE INTO upload_log (user_id, upload_time, date)
                VALUES (?, ?, ?)
                ''', (user_id, upload_time, today_date))

                await conn.commit()
                logger.info(f"Logged upload for user {user_id} at {upload_time} on {today_date}.")
                return True

        except aiosqlite.Error as e:
            logger.error(f"Failed to log upload for user {user_id}: {e}")
            return False

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

    async def get_user_api(self, user_id):
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()
                query = '''
                    SELECT api_key
                    FROM users_data
                    WHERE user_id = ?
                    '''

                result = await cursor.execute(query, (user_id,))
                api_key = await result.fetchone()

                logger.info(f"User {api_key} successfully retrieved.")

        except aiosqlite.Error as e:
            logger.error(f"Failed to log upload for user {user_id}: {e}")
            return False

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

    async def date_time_validation(self, date_time_str):
        time_pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$'
        if re.match(time_pattern, date_time_str):
            return True
        return False

