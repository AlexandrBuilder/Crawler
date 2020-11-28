import asyncio

from searcher.application import Application


async def start_async():
    application = Application()
    await application.start_tasks_async()
    await application.run()
    await application.stop_tasks_async()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_async())
