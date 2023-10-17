import threading
from datetime import datetime as dt
import time


class Singleton:
    _instance = None
    _lock = threading.RLock()

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
    rate = [0 for _ in range(2)]

    @classmethod
    def check_rate(cls):
        with cls._lock:
            return sum(cls.rate)

    @classmethod
    def add(cls):
        with cls._lock:
            t = dt.now().second
            t = t % 2
            cls.rate[t] += 1


def test_singleton_is_always_same_object():
    # print(RateTracker() is RateTracker())
    r = RateTracker()
    r.add()

    time.sleep(1)
    print(RateTracker().rate)
    s = RateTracker()
    s.add()
    # print(s.rate is r.rate)
    # print(s.rate == r.rate)
    print(RateTracker().rate)
    print(s.rate, r.rate,RateTracker.check_rate())

    # Sanity check - a non-singleton class should create two separate
    #  instances
    # class NonSingleton:
    #     pass
    #
    # assert NonSingleton() is not NonSingleton()
    # print(NonSingleton() is not NonSingleton())


if __name__ == "__main__":
    test_singleton_is_always_same_object()
