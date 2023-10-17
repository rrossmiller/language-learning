import asyncio
from ratelimit import limits, sleep_and_retry
import time


@sleep_and_retry
@limits(calls=2, period=5)
async def c(i):
    await asyncio.sleep(0.5)
    print(i)


async def a():
    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        for i in range(3):
            tg.create_task(c(i))
    print(time.perf_counter() - start)


if __name__ == "__main__":
    asyncio.run(a())
