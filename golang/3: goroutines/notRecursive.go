package main

import (
	"fmt"
	"time"
)

func NotRecursive(max, numWorkers int, verbose bool) {
	start := time.Now()
	ch := make(chan int)
	go run(max, numWorkers, ch)

	elapsed := fmt.Sprintf("elapsed %v", time.Since(start))

	if verbose {
		for msg := range ch {
			fmt.Println(msg)
		}
	}
	fmt.Println(elapsed)
}

func run(max, numWorkers int, ch chan int) {
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
