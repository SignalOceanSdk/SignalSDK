import os


class Connection:
    __DEFAULT_API_HOST = 'https://signalprodapims.azure-api.net/'

    def __init__(self, api_key: str = None, api_host: str = None):
        self.__api_key = api_key
        self.__api_host = api_host

    @property
    def headers(self):
        return {
            'Api-Key': self.__api_key or os.environ.get('SIGNAL_OCEAN_API_KEY'),
            'Content-Type': 'application/json'
        }

    @property
    def api_host(self):
        return (
            self.__api_host
            or os.environ.get('SIGNAL_OCEAN_API_HOST')
            or Connection.__DEFAULT_API_HOST
        )
