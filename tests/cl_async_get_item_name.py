import uvloop
import asyncio
from termcolor import colored

from common import *
from async_server_api import AsyncServerApiClient


class AsyncItemGetter:
    def __init__(self, item_name):
        self.item_name = item_name
        self.api_url = API_URL
        self.api_version = API_VERSION

    async def get_item(self, session: AsyncServerApiClient):
        resp = await session.get_item(name=self.item_name)
        if resp.status != 200:
            print(colored('failed to get item!{}'.format(compose_response_msg(resp)), 'red'))
            return False
        else:
            print(colored('get success!'), 'green')
            return True

    async def run(self):
        async with AsyncServerApiClient(
            server_url=API_URL,
            api_version=API_VERSION
        ) as session:
            resp = await self.get_item(session)
            return resp


def main(count, item_name):
    workers = []
    for _ in range(count):
        worker = AsyncItemGetter(item_name)
        workers.append(worker)
    tasks = []
    uvloop.install()
    loop = asyncio.get_event_loop()
    for worker in workers:
        task = loop.create_task(worker.run())
        tasks.append(task)
    try:
        results = loop.run_until_complete(asyncio.gather(*tasks))
        print(colored(results, color='green'))
    except Exception as e:
        print(e)
    finally:
        for task in tasks:
            task.cancel()


if __name__ == '__main__':
    main(200, "lemonade")



