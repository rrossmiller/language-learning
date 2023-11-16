import asyncio
import time
from typing import Callable

# import tiktoken
from tqdm import tqdm


class RateLimiter:
    lock = asyncio.Lock()

    def __init__(self, tpm: int):
        """
        Set the TPM and the RPM given 6 RPM per 1000 TPM and return the rate limiter instance.

        Args:
            tpm (int): tokens per minute
        """
        self.tpm = tpm
        self.rpm = int(6 * self.tpm / 1000)
        # logging.debug(f"RateLimiter TPM: {self.tpm} | RPM: {self.rpm}")
        print(f"TPM: {self.tpm} | RPM: {self.rpm}")
        self.period = 60  # seconds
        self.times: list[float] = []
        self.tokens: list[int] = []
        self.spacing = self.period / self.rpm
        # encoding = tiktoken.encoding_for_model("gpt-4")

    async def rate_limit(
        self,
        func: Callable,
        args: tuple,
        worker: str,
        bar: tqdm | None = None,
    ):
        """
        Rate limit the function call to the specified RPM

        Params:
            func (Callable): the function to rate limit
            args (tuple): the arguments to pass to the function
            worker (str): the name of the worker calling the function
        """
        async with self.lock:
            current_time = time.monotonic()
            self.times.append(current_time)

            # Space requests s.t. there are 60/rpm (+ 0.1) seconds in between each request
            # That allows for the max requests per minute (plus some breathing room)

            # Don't wait on the first request
            # Don't wait on requests that are beyone 1 period from the previous request
            is_far_past = (self.times[-1] - self.times[-1]) >= self.period
            if len(self.times) > 1 and not is_far_past:
                if bar is not None:
                    bar.set_description_str(
                        f"{worker} sleeping for {self.spacing+0.1:.3f}"
                    )
                await asyncio.sleep(self.spacing + 0.1)

            # periodically clean out self.times
            if is_far_past:
                self.times = [current_time]
            elif len(self.times) > 100:
                for i, t in enumerate(self.times[::-1]):
                    if (current_time - t) >= self.period:
                        self.times = self.times[-i + 1 :]
                        break

        return await func(*args, bar, worker)


async def worker(
    n: int,
    rl: RateLimiter,
    task_queue: asyncio.Queue,
    ttl_tracker: tqdm | None = None,
    worker_bars=False,
):
    worker_name = f"worker-{n}"
    worker_name += " " if n < 10 else ""
    responses = []
    i = 0

    bar = None
    if worker_bars:
        offset = 0
        if ttl_tracker is not None:
            offset = 1
        bar = tqdm(position=n + offset, desc=worker_name)

    while not task_queue.empty():
        # get the next task
        func, args = await task_queue.get()
        response = await rl.rate_limit(func, args, worker_name, bar)
        responses.append(response)
        i += 1
        if bar is not None:
            bar.update()
        if ttl_tracker is not None:
            ttl_tracker.update()
        task_queue.task_done()
    if bar is not None:
        bar.set_description_str(f"{worker_name}: completed {i} tasks")
    # collate results
    results = []
    for r in responses:
        results.append((r[0], r[1]))

    return results, bar
