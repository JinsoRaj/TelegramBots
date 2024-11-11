import aiohttp
from __init__ import logger
from user_data_handler import DataHandler


class ApiHandler:

    async def api_checker(self, api_key):
        """
        Checks the validity of an API key by sending a request to the authentication API.

        Args:
            api_key (str): The API key to be checked.

        Returns:
            bool: True if the API key is valid (status 200), False if invalid or an error occurs.
        """
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
        """
        Saves or updates the user's API key in the database.

        Args:
            user_id (str): The ID of the user.
            api_key (str): The API key to be saved or updated.

        Returns:
            bool: True if the API key was successfully saved or updated, False if an error occurs.
        """

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

    async def stop_profile(self, profile_id):
        """
        Stops a browser profile using the provided profile ID.

        Args:
            profile_id (str): The ID of the profile to stop.

        Returns:
            bool: True if the profile was successfully stopped, False if an error occurs.
        """

        api_url = f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/stop'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        logger.info(f'Successfully stopped profile {profile_id}: {response_json}')
                        return True
                    else:
                        logger.info(f'Failed to stop the profile {profile_id}: {response.status}')
                        return False
        except aiohttp.ClientConnectorError as e:
            logger.info(f"Failed to stop profile {profile_id}: {e}")

