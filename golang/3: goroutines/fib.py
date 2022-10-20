from time import perf_counter_ns,ctime
from concurrent.futures import ProcessPoolExecutor as PPE
# from concurrent.futures import ThreadPoolExecutor as PPE


def fib(n: int):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    start = perf_counter_ns()
    # for i in range(45):
    #     print(i,fib(i))

    print(ctime())
    with PPE() as exec:
        exec.map(fib, range(40))

    fin = (perf_counter_ns() - start) / 1e9
    print(fin, "seconds")
    # print("it does ~40 per minute not in parrallel")
