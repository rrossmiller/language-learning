import asyncio
import time

from ratelimit import RateTracker


async def task(i, rate_tracker: RateTracker):
    for _ in range(i):
        x = rate_tracker.queue_and_check_rate(10)

        print(x)


async def run():
    rate_tracker = RateTracker()
    r = RateTracker()
    assert r is rate_tracker

    # max 100 reqs over 5 seconds
    # max 10 tokens over 5 seconds
    # 2 tasks, 12*10 tokens = 240 tokens
    # should take 240 tokens (5 seconds/10tokens) =120 seconds -5 seconds (because first req here will be free)
    # = 115 seconds minimum
    async with asyncio.TaskGroup() as tg:
        for _ in range(2, 0, -1):
            tg.create_task(task(12, rate_tracker))


if __name__ == "__main__":
    # have two threads hit the rate limiter as fast as possible.
    # the rate limiter must keep them below the specified rate

    start = time.perf_counter()
    asyncio.run(run())
    end = time.perf_counter()

    print(end - start)
