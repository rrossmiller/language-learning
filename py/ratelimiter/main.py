import asyncio
import time

from ratelimit import RateTracker


async def task(i, rate_tracker: RateTracker):
    for _ in range(i):
        x = rate_tracker.queue_and_check_rate(10)
        print(x)


async def run():
    rate_tracker = RateTracker()
    # rate is 6/1
    # 36 requests should take minimum 6-cls.period seconds
    async with asyncio.TaskGroup() as tg:
        for _ in range(3, 0, -1):
            tg.create_task(task(12, rate_tracker))


class A:
    def __init__(self) -> None:
        pass


if __name__ == "__main__":
    r = RateTracker()
    print(RateTracker() is r)
    print(A() is A())
    exit()
    # have two threads hit the rate limiter as fast as possible.
    # the rate limiter must keep them below the specified rate
    start = time.perf_counter()
    asyncio.run(run())
    end = time.perf_counter()

    print(end - start)
