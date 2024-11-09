import aiosqlite
import random
from pathlib import Path
from __init__ import logger
from uploading_timer import Timer
import asyncio
import os
import re


class DataHandler:
    def __init__(self):
        self.database_name = 'users_data.db'

    async def table_creation(self):
        """
        Creates the 'users_data' table if it does not already exist.

        Returns:
            bool: True if the table is created successfully, False if an error occurs.

        Logs:
            - Info: If the table is created or already exists.
            - Error: If a database error occurs during table creation.
        """
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
        """
        Creates the 'daily_upload_times' table for tracking upload schedules.

        Returns:
            bool: True if the table is created successfully, False if an error occurs.

        Logs:
            - Info: If the table is created or already exists.
            - Error: If a database error occurs during table creation.
        """
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
        """
        Creates the 'upload_log' table to log video upload times for each user.

        Returns:
            bool: True if the table is created successfully, False if an error occurs.

        Logs:
            - Info: If the table is created or already exists.
            - Error: If a database error occurs during table creation.
        """
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
        """
        Adds a new user to the 'users_data' table.

        Args:
            **kwargs: Dictionary containing 'user_id' and 'api_key' for the new user.

        Returns:
            bool: True if the user is added successfully, False if an error occurs.

        Logs:
            - Info: When the user is successfully added.
            - Error: If a database error occurs during the user addition.
        """
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
        """
        Updates user information in the specified table.

        Args:
            user_id (str): The ID of the user to update.
            table_name (str): The name of the table to update.
            **kwargs: Key-value pairs of the columns to update.

        Returns:
            bool: True if the update is successful, False if an error occurs.

        Logs:
            - Info: When the user information is successfully updated.
            - Error: If a database error occurs during the update.
        """

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
        """
        Checks if a user exists in the 'users_data' table.

        Args:
            user_id (str): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.

        Logs:
            - Info: When the user check is successful.
            - Error: If a database error occurs during the check.
        """

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
        """
        Sets up a user's daily upload schedule.

        Args:
            user_id (str): The ID of the user.
            daily_upload_times (list): List of times in 'HH:MM:SS' format.

        Returns:
            bool: True if the schedule is set up successfully, False otherwise.
        """
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
        """
        Retrieves users who are scheduled to upload at or before a given time.

        Args:
            now_time (str): The current time in 'HH:MM:SS' format.
            now_date (str): The current date in 'YYYY-MM-DD' format.

        Returns:
            list: List of user records scheduled for upload.
        """
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                current_time = now_time
                today_date = now_date

                logger.debug(f"Executing query with date: {today_date} and time: {current_time}")

                query = '''
                    SELECT DISTINCT dt.user_id, MAX(dt.upload_time) AS nearest_time
                    FROM daily_upload_times dt
                    LEFT JOIN upload_log ul
                    ON dt.user_id = ul.user_id AND dt.upload_time = ul.upload_time AND ul.date = ?
                    WHERE dt.upload_time <= ? AND ABS(strftime('%s', ?) - strftime('%s', dt.upload_time)) <= 300 AND ul.id IS NULL
                    GROUP BY dt.user_id
                    ORDER BY nearest_time DESC
                    '''

                result = await cursor.execute(query, (today_date, current_time, current_time))
                users_to_upload = await result.fetchall()

                logger.info(f"Found {len(users_to_upload)} users scheduled for upload at or before {current_time}.")
                return [user for user in users_to_upload]

        except aiosqlite.Error as e:
            logger.error(f"Failed to fetch users to upload: {e}")
            return []

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return []

    async def log_upload(self, user_id, upload_time):
        """
        Logs the upload details for a user in the database.

        Args:
            user_id (int): The ID of the user who uploaded the content.
            upload_time (str): The time the upload occurred.

        Returns:
            bool: True if the log entry was successful, False if an error occurred.
        """
        try:
            async with aiosqlite.connect(self.database_name) as conn:
                cursor = await conn.cursor()

                timer = Timer()

                today_date = await asyncio.to_thread(timer.get_current_time_y_m_d)

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
        """
        Retrieves the API key for a user from the database.

        Args:
            user_id (int): The ID of the user for whom the API key is being retrieved.

        Returns:
            list: A list containing the API key if successful, False if an error occurred.
        """
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

                return [key for key in api_key]

        except aiosqlite.Error as e:
            logger.error(f"Failed to log upload for user {user_id}: {e}")
            return False

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

    async def date_time_validation(self, date_time_str):
        """
       Validates if the provided time string matches the format HH:MM:SS.

       Args:
           date_time_str (str): The time string to validate.

       Returns:
           bool: True if the string matches the time format, False otherwise.
       """

        time_pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$'
        if re.match(time_pattern, date_time_str):
            return True
        return False

    async def pick_random_video(self, user_id, videos_folder_path):
        """
        Selects a random video from the user's video folder.

        Args:
            user_id (int): The ID of the user.
            videos_folder_path (str): The path to the folder where videos are stored.

        Returns:
            str|bool: The path of the selected video if successful, False if an error occurred.
        """
        try:
            folder_path = Path(videos_folder_path)

            names = [item.name for item in folder_path.iterdir() if item.is_dir()]

            if names and user_id in names:
                folder_path = Path(f"{videos_folder_path}/{user_id}")
                files = [file.resolve() for file in folder_path.iterdir() if file.is_file()]
                if files:
                    logger.info(f"Random video successfully retrieved for user {user_id}.")
                    return random.choice(files)
                logger.info(f"There is no video files at {user_id} folder")
                return False
            else:
                if await self.create_user_video_folder(f"{videos_folder_path}/{user_id}"):
                    logger.info(f"Successfully create user:{user_id} videos folder")
                logger.info(f"Failed to create user:{user_id} videos folder")
                return False

        except Exception as e:
            logger.error(f"Failed to pick a random file: {e}")
            return False

    async def create_user_video_folder(self, user_videos_folder_path):
        """
        Creates a folder for the user's videos if it doesn't already exist.

        Args:
            user_videos_folder_path (str): The path where the user's video folder should be created.

        Returns:
            bool: True if the folder was created successfully, False if it already exists.
        """

        if not os.path.exists(user_videos_folder_path):
            os.makedirs(user_videos_folder_path)
            return True
