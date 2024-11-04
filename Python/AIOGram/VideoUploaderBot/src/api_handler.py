import aiohttp
from src import logger
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

