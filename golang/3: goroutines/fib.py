from time import perf_counter_ns, ctime
from concurrent.futures import ProcessPoolExecutor as PPE

# from concurrent.futures import ThreadPoolExecutor as PPE


def fib(n: int):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


def fib_norec(n):
    f = [0, 1]

    for i in range(2, n):
        f[i] = f[i - 1] + f[i - 2]


if __name__ == "__main__":
    start = perf_counter_ns()
    # for i in range(45):
    #     print(i,fib(i))

    print(ctime())
    with PPE() as exec:
        exec.map(fib_norec, range(40))

    fin = (perf_counter_ns() - start) / 1e9
    
    if fin < 0.1:
        print(fin*1000, "millis")
    else:
        print(fin, "seconds")