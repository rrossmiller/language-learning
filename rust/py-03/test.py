from time import perf_counter_ns
from rustonacci import fibonacci

def fib(n):
    f = [0, 1]

    for i in range(2, n):
        f.append(f[i - 1] + f[i - 2])
    return f[n - 1]

if __name__ == "__main__":
    n=50
    print('rust')
    start = perf_counter_ns()
    r = fibonacci(n)
    end = perf_counter_ns()
    print(f'elapsed: {end-start}ns')

    print('py')
    start = perf_counter_ns()
    r = fib(n)
    end = perf_counter_ns()
    print(f'elapsed: {end-start}ns')


