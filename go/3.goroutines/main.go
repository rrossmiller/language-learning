package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	ttl := 45
	jobs := make(chan int, ttl)
	results := make(chan int, ttl)
	numWorkers := 8

	for i := 0; i < numWorkers; i++ {
		go worker(jobs, results)
	}

	for i := 0; i < cap(jobs); i++ {
		jobs <- i
	}
	close(jobs) // this is safe becuase main is the sender to jobs

	// Code to measure
	duration := time.Since(start)
	fmt.Println("elapsed", duration)

	// // print results
	// cnt := 1
	// for i := range results {
	// 	fmt.Println(cnt, i)

	// 	if cnt == ttl {
	// 		close(results)
	// 	}
	// 	cnt++
	// }

	// not recursive
	NotRecursive(ttl, numWorkers, true)
}

func worker(jobs <-chan int, results chan<- int) {
	for n := range jobs {
		results <- fib(n)
	}
}

func fib(n int) int {
	if n <= 1 {
		return n
	}
	return fib(n-1) + fib(n-2)
}
