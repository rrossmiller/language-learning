import threading
import time


class Singleton:
    _instance = None
    _lock = threading.RLock()
    # _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance


class RateTracker(Singleton):
    max_rate = 60
    token_max = 10_000
    period = 60  # in seconds
    times: list[float] = []
    tokens: list[int] = []

    reqs = 0
    tkns = 0

    @classmethod
    def queue_and_check_rate(cls, tkns) -> tuple[int, int]:
        """
        Check the rate over the last `period`
        """
        with cls._lock:
            # add current task
            cls.times.append(time.time())
            cls.tokens.append(tkns)
            cls.tkns += tkns
            cls.reqs += 1

            # if this is the first item it doesn't need to wait
            if len(cls.times) == 1:
                return cls.reqs, sum(cls.tokens)

            # get all the requests within the last period
            last_time = cls.times[-1]
            rate = 0
            tkn_rate = 0
            time_n = last_time
            # loop from the second to last to the 0th entry
            for i, t in enumerate(cls.times[-2::-1]):
                rate += 1
                tkn_rate += cls.tokens[i]
                # if the last request was more than a `period` from t
                # we can reset the times list
                if last_time - t >= cls.period - 1:
                    # only keep track of the last `period`
                    if len(cls.times) > 100:
                        cls.cleanup_times(i)
                    break
                time_n = t

            if rate >= cls.max_rate - 1 or tkn_rate >= cls.token_max:
                # (period - (elapsed time of requests that count towards the req rate)) * (how many more periods need to be waited to finish)
                wait_time = cls.period - (last_time - time_n)

                # hold the lock until running can continue
                print("rate in last min:", rate)
                print("tokens in last min:", tkn_rate)
                print("sleeping for", wait_time)
                time.sleep(wait_time)
            return cls.reqs, sum(cls.tokens)

    @classmethod
    def cleanup_times(cls, i: int):
        cls.times = cls.times[len(cls.times) - i :]
        cls.tokens = cls.tokens[len(cls.tokens) - i :]

    @classmethod
    def check_rate(cls) -> tuple[bool, float]:
        """
        Check the call rate over the last `period`
        If the current seconds is (mod somthing) reset some history
        """
        with cls._lock:
            if len(cls.times) == 1:
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
                    cls.cleanup_times(i)
                    break
                rate += 1

            # (period - (elapsed time of requests that count towards the req rate)) * (how many more periods need to be waited to finish)
            wait_time = (cls.period - (last - t)) * (len(cls.times) / cls.max_rate)
            return (rate < cls.max_rate, wait_time)

        # return if the rate is below the threshold and how long to wait
        # return ()

    @classmethod
    def _add(cls):
        # with cls._lock:
        cls.times.append(time.time())
