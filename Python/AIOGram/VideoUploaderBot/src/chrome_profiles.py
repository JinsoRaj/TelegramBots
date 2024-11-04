import pyanty as dolphin
import aiohttp
import aiosqlite
import requests
import asyncio
from pyanty import DolphinAPI
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

    async def run_profile(self, profile):
        response = await asyncio.to_thread(dolphin.run_profile(profile['id']))
        self.port = response['automation']['port']
        driver = await asyncio.to_thread(dolphin.get_driver(self.port))
        print(f"Running profile: {profile['name']} with port: {self.port}")
        return driver

    async def check_and_add_profiles_to_queue(self):
        while True:
            profiles_to_upload = await self.get_profiles_to_upload()
            for user_id in profiles_to_upload:
                await self.upload_queue.put(user_id)
            await asyncio.sleep(180)

    async def get_profiles_to_upload(self):
        now_time = await asyncio.to_thread(self.timer.get_current_time_h_m_s())
        now_date = await asyncio.to_thread(self.timer.get_current_time_y_m_d())

        users_to_upload = await self.data_handler.get_users_to_upload(now_time, now_date)

        return users_to_upload

    async def get_all_profiles(self, dolphin_api):
        profiles = []
        api = DolphinAPI(api_key=dolphin_api)
        response = await asyncio.to_thread(api.get_profiles())
        data_list = response.get('data', [])
        for profile in data_list:
            profiles.append(profile)

        return profiles
