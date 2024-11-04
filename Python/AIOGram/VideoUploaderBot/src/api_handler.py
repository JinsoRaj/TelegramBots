import aiohttp
from __init__ import logger
from user_data_handler import DataHandler


class ApiHandler:

    async def api_checker(self, api_key):
        api_url = 'http://localhost:3001/v1.0/auth/login-with-token'

        request_data = {
            'token': api_key
        }

        headers = {
            'Content-Type': 'application/json'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=request_data, headers=headers) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        print('Successful response:', response_json)
                        logger.info(f'Successful response from the API request: {response_json}')
                        return True
                    else:
                        print('Error:', response.status)
                        logger.info(f'Failed to check API. API is invalid: {response.status}')
                        return False
        except aiohttp.ClientConnectorError as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return False

    async def api_saver(self, user_id, api_key):
        data_handler = DataHandler()

        if not await self.api_checker(api_key):
            return False

        user = await data_handler.check_user(user_id=user_id)

        if user:
            if await data_handler.update_user(user_id=user_id, table_name='users_data', api_key=api_key):
                return True
            return False
        else:
            if await data_handler.add_user(user_id=user_id, api_key=api_key):
                return True
            return False
