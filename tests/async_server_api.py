from aiohttp import ClientSession


class AsyncServerApiClient(ClientSession):
    def __init__(self, server_url, api_version):
        super().__init__()
        self.server_url = server_url
        self.api_version = api_version
        self.api_path = '{}/{}'.format(self.server_url, self.api_version)

    async def get_item(self, name):
        api_url = '{}/item?name={}'.format(self.api_path, name)
        return await self.get(api_url)



