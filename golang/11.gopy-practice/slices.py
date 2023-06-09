# Copyright 2017 The go-python Authors.  All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from out import slices, go
import numpy as np

from time import perf_counter


def fib(max):
    rtn = []
    rtn.append(0)
    rtn.append(1)

    for i in range(2, max):
        rtn.append(rtn[i - 1] + rtn[i - 2])
    # print(rtn)
    return rtn


a = [1, 2, 3, 4]
b = slices.CreateSlice()
arr = np.arange(5)
print("Python list:", a)
print("Go slice: ", b)
print(f"arr {arr}")
print("slices.IntSum from Python list:", slices.IntSum(go.Slice_int(a)))
print("slices.IntSum from Go slice:", slices.IntSum(b))
print("slices.IntSum from numpy arr", slices.IntSum(go.Slice_int(arr)))

print()
ans = 63245986
start = perf_counter()
assert fib(40)[-1] == ans

print("Python elapsed:", perf_counter() - start)

start = perf_counter()
assert slices.Fib(40, False)[-1] == ans
print("Go elapsed:", perf_counter() - start)


start = perf_counter()
for _ in range(1000):
    fib(40)
print("1000 Python elapsed:", perf_counter() - start)

start = perf_counter()
for _ in range(1000):
    slices.Fib(40, False)
print("1000 Go elapsed:", perf_counter() - start)

start = perf_counter()
slices.FibParallel(40, 8, 1000, False)
print("1000 Go Parallel elapsed:", perf_counter() - start)
