import asyncio
from singleton import Singleton
import time


class RateTracker(Singleton):
    max_rate = 2
    period = 5  # in seconds
    times: list[float] = []

    @classmethod
    def clean_times(cls, i: int) -> bool:
        cls.times = cls.times[len(cls.times) - i :]

    @classmethod
    def check_rate(cls) -> (bool, float):
        """
        Check the call rate over the last `period`
        If the current seconds is (mod somthing) reset some history
        """
        with cls._lock:
            if len(cls.times) == 0:
                cls.add()
                return (True, 0.0)
            # add up all the requests within the last minute
            rate = 0
            last = cls.times[-1]
            t = last
            # loop from the second to last to the 0th entry
            for i, t in enumerate(cls.times[-2::-1]):
                # if the last request was more than a `period` from t
                if last - t >= cls.period:
                    # only keep track of the last `period`
                    cls.clean_times(i)
                    break
                rate += 1

            # (period - (elapsed time of requests that count towards the req rate)) * (how many more periods need to be waited to finish)
            wait_time = (cls.period - (last - t)) * (len(cls.times) / cls.max_rate)-cls.max_rate
            return (rate < cls.max_rate, wait_time)

        # return if the rate is below the threshold and how long to wait
        # return ()

    @classmethod
    def add(cls):
        with cls._lock:
            cls.times.append(time.time())


async def b(tracker: RateTracker, i):
    # this is the part of the function that should controlled by the rate limit

    # await asyncio.sleep(i)
    ok, wait_time = tracker.check_rate()
    print(len(tracker.times), i, ok)
    tracker.add()
    if not ok:
        print("sleeping:", wait_time)
        await asyncio.sleep(wait_time)
    # await asyncio.sleep(1)
    return i


async def a():
    tasks = []
    tracker = RateTracker()
    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        for i in range(10, 0, -1):
            task = tg.create_task(b(tracker, i))
            tasks.append(task)

    print(time.perf_counter() - start)
    for t in tasks:
        print(t.result())


if __name__ == "__main__":
    asyncio.run(a())
