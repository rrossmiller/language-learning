from time import perf_counter_ns
def fib(n: int):
	if n <= 1:
		return n
	
	return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    # start = perf_counter_ns()
    # for i in range(45):
    #     print(i,fib(i))
    
    
    # fin = (perf_counter_ns()-start) / 1e9
    # print(fin, "seconds")
    print("it does ~40 per minute")