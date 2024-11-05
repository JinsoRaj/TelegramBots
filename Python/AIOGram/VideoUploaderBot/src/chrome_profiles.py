import pyanty as dolphin
import aiohttp
import aiosqlite
import requests
import asyncio
from pyanty import DolphinAPI
from selenium_script import SeleniumScript
from uploading_timer import Timer
from user_data_handler import DataHandler
from __init__ import logger


class DolphinProfiles:
    def __init__(self, max_concurrent_uploads=3):
        self.port = 9222
        self.task_semaphore = asyncio.Semaphore(max_concurrent_uploads)
        self.upload_queue = asyncio.Queue()
        self.data_handler = DataHandler()
        self.timer = Timer()
        self.running_tasks = False
        self.check_task = None
        self.worker_task = None

    async def run_profile(self, profile):
        try:
            logger.info(f"Starting profile: {profile['name']}")
            response = await asyncio.to_thread(dolphin.run_profile, profile['id'])
            self.port = response['automation']['port']
            driver = await asyncio.to_thread(dolphin.get_driver, self.port)
            logger.info(f"Profile {profile['name']} is running on port {self.port}")
            return driver
        except Exception as e:
            logger.error(f"Error running profile {profile['name']}: {e}")
            return None

    async def check_and_add_profiles_to_queue(self):
        while self.running_tasks:
            try:
                users_to_upload = await self.get_profiles_to_upload()
                if users_to_upload:
                    for user_id in users_to_upload:
                        api_key = await self.data_handler.get_user_api(user_id)
                        profiles_to_upload = await self.get_all_profiles(api_key[0])

                        for profile in profiles_to_upload:
                            await self.upload_queue.put(profile)
                            logger.info(f"Profile {profile['name']} added to the queue.")
            except Exception as e:
                logger.error(f"Error while checking and adding profiles to queue: {e}")
            await asyncio.sleep(180)

    async def get_profiles_to_upload(self):
        now_time = await asyncio.to_thread(self.timer.get_current_time_h_m_s)
        now_date = await asyncio.to_thread(self.timer.get_current_time_y_m_d)

        users_to_upload = await self.data_handler.get_users_to_upload(now_time, now_date)

        return users_to_upload

    async def task_worker(self):
        while self.running_tasks:
            profile = await self.upload_queue.get()

            try:
                async with self.task_semaphore:
                    driver = await self.run_profile(profile)

                    if driver:
                        selenium_script = SeleniumScript(driver)
                        await selenium_script.upload_video(profile)
                        logger.info(f"Video upload for profile {profile['name']} completed.")
                    else:
                        logger.error(f"Failed to start WebDriver for profile {profile['name']}.")

            except Exception as e:
                logger.error(f"Error during task execution for profile {profile['name']}: {e}")

            finally:
                self.upload_queue.task_done()

    async def get_all_profiles(self, dolphin_api):
        try:
            profiles = []
            api = DolphinAPI(api_key=dolphin_api)
            response = await asyncio.to_thread(api.get_profiles)
            data_list = response.get('data', [])

            for profile in data_list:
                profiles.append(profile)

            logger.info(f"Retrieved {len(profiles)} profiles from Dolphin API.")
            return profiles
        except Exception as e:
            logger.error(f"Error retrieving profiles from Dolphin API: {e}")
            return []

    async def start_tasks(self):
        if not self.running_tasks:
            logger.info("Starting background tasks.")
            self.running_tasks = True
            self.check_task = asyncio.create_task(self.check_and_add_profiles_to_queue())
            self.worker_task = asyncio.create_task(self.task_worker())
        else:
            logger.info("Background tasks are already running.")

    async def stop_tasks(self):
        if self.running_tasks:
            logger.info("Stopping background tasks.")
            self.running_tasks = False
            # Cancel the tasks
            if self.check_task:
                self.check_task.cancel()
            if self.worker_task:
                self.worker_task.cancel()

            await asyncio.gather(self.check_task, self.worker_task, return_exceptions=True)
            logger.info("Background tasks stopped.")
        else:
            logger.info("Background tasks are not running.")
