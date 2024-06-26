package main

import (
	"fmt"
	"time"
)

func NotRecursive(max, numWorkers int, verbose bool) {
	start := time.Now()
	ch := make(chan int)
	go run(max, ch)

	if verbose {
		for msg := range ch {
			fmt.Println(msg)
		}
	}
	elapsed := fmt.Sprintf("elapsed %v", time.Since(start))

	fmt.Println(elapsed)

	fmt.Println("not parallel...", max)

	start = time.Now()
	f := runNotParallel(max)
	elapsed = fmt.Sprintf("elapsed %v", time.Since(start))
	if verbose {
		for i, v := range f {
			fmt.Printf("%d: %d\n", i, v)
		}
	}
	fmt.Println(elapsed)
}

func runNotParallel(max int) []int {
	fib := make([]int, max)
	fib[0] = 0
	fib[1] = 1
	for i := 2; i < max; i++ {
		fib[i] = fib[i-1] + fib[i-2]
	}
	return fib
}

func run(max int, ch chan int) {
	fib := make([]int, max)
	fib[0] = 0
	fib[1] = 1
	ch <- fib[0]
	ch <- fib[1]

	for i := 2; i < max; i++ {
		fib[i] = fib[i-1] + fib[i-2]
		ch <- fib[i]
	}
	close(ch)
}
