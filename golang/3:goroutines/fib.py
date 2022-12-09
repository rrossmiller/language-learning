from time import perf_counter_ns, ctime
from concurrent.futures import ProcessPoolExecutor as PPE

# from concurrent.futures import ThreadPoolExecutor as PPE
from numba import njit


def fib(n: int):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


# @njit
def fib_norec(n):
    f = [0, 1]

    for i in range(2, n):
        f.append(f[i - 1] + f[i - 2])
    return f[n - 1]


if __name__ == "__main__":
    from argparse import ArgumentParser

    func = fib_norec
    a = ArgumentParser()
    a.add_argument("-p", default=False)
    a.add_argument("-n", default=40)

    par = a.parse_args().p
    n = int(a.parse_args().n)
    if not par:
        start = perf_counter_ns()
        for i in range(n+1):
            # func(i)
            print(i, func(i))
    else:
        start = perf_counter_ns()
        print(ctime())
        with PPE() as exec:
            exec.map(func, range(n+1))

    fin = (perf_counter_ns() - start) / 1e9
    if fin < 0.001:
        print(fin * 1e6, "micros")

    elif fin < 0.1:
        print(fin * 1e3, "millis")
    else:
        print(fin, "seconds")
