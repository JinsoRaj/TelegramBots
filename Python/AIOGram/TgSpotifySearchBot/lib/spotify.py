import aiohttp
from base64 import b64encode
from lib.models.token import Token
from lib.models.search_results import SearchResults


class Spotify:
    def __init__(self, client_id: str, client_secret: str) -> None:
        """Async Spotify API wrapper 

        Args:
            client_id (str): The client ID of your Spotify app
            client_secret (str): The client secret of your Spotify app
        """
        self._client_id = client_id
        self._client_secret = client_secret

        self._session = None
        self._token_obj = None

        self._headers = {
            'Content-Type': 'application/json'
        }

    async def login(self) -> Token:
        """Login to Spotify API

        Returns:
            Token: The OAuth2 access token object
        """
        if self._session is None:
            self._session = aiohttp.ClientSession()

        if self._token_obj is not None and not self._token_obj.is_expired:
            return Token

        self._token_obj = await self._get_access_token()
        self._headers['Authorization'] = f'Bearer {self._token_obj.access_token}'
        return self._token_obj

    async def _get_access_token(self) -> Token:
        """Get an access token from Spotify API

        Returns:
            Token: The OAuth2 access token object
        """
        auth = self._b64encode(f'{self._client_id}:{self._client_secret}')

        headers = {'Authorization': f'Basic {auth}'}
        data = {'grant_type': 'client_credentials'}

        token = await self._make_request(
            method='POST',
            url='https://accounts.spotify.com/api/token',
            data=data,
            headers=headers,
            timeout=15
        )

        return Token(
            access_token=token['access_token'],
            token_type=token['token_type'],
            expires_in=token['expires_in']
        )

    async def search(
        self,
        query: str,
        limit=10,
        offset=0,
        type=['artist', 'album', 'track', 'playlist', 'show', 'episode']
    ) -> SearchResults:
        """Search for an item on Spotify

        Args:
            query (str): The search query
            limit (int, optional): The limit of items to fetch. Defaults to 10.
            offset (int, optional): Defaults to 0.
            type (list, optional): The type of item to search. Defaults to ['artist', 'album', 'track', 'playlist', 'show', 'episode'].

        Returns:
            SearchResults: The search results object
        """

        if self._token_obj is None or self._token_obj.is_expired:
            await self.login()

        resp = await self._make_request(
            method='GET',
            url='https://api.spotify.com/v1/search',
            params={
                'q': query,
                'type': ','.join(type),
                'limit': limit,
                'offset': offset,
                'include_external': 'audio'
            },
            headers=self._headers,
            timeout=15
        )

        return SearchResults(**resp)
     
    async def _make_request(
        self,
        method: str,
        url: str,
        data: dict = {},
        headers: dict = {},
        params={},
        **kwargs
    ) -> str:
        """Makes a request to the provided api

        Args:
            method (str): The HTTP method
            url (str): The URL to make the request to
            data (dict, optional): The data to send. Defaults to {}.
            headers (dict, optional): The headers to send. Defaults to {}.
            params (dict, optional): The url parameters to send. Defaults to {}.

        Raises:
            Exception: If the request fails

        Returns:
            str: The response as json
        """

        if self._session is None:
            self._session = aiohttp.ClientSession()

        async with self._session.request(
            method=method,
            url=url,
            data=data,
            headers=headers,
            params=params,
            **kwargs
        ) as req:

            if req.status != 200:
                raise Exception(f'Error while making request: {req.status}')

            return await req.json()

    def _b64encode(self, data: str) -> str:
        """Encode data to base64

        Args:
            data (str): The data to encode

        Returns:
            str: The encoded data
        """
        return (b64encode(data.encode('ascii'))).decode('ascii')