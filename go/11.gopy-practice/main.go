// Copyright 2017 The go-python Authors.  All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package slices

import (
	"fmt"
	"log"
)

func Fib(max int, verbose bool) []int {
	res := run(max)
	if verbose {
		for msg := range res {
			fmt.Println(msg)
		}
	}
	return res
}

func FibParallel(max, numWorkers, numTimes int, verbose bool) {
	//todo
	jobs := make(chan int, numTimes)
	//results := make(chan int, numTimes)
	results := make(chan int)

	for i := 0; i < numWorkers; i++ {
		go func(jobs <-chan int, results chan<- int) {
			for range jobs {
				r := run(max)
				results <- r[len(r)-1]
			}
		}(jobs, results)
	}

	for i := 0; i < numTimes; i++ {
		jobs <- i
	}
	close(jobs)
	fmt.Println("closing jobs")

	n := 1
	for i := range results {
		if i != 63245986 {
			log.Fatal("i != 63245986")
		}
		if n == numTimes {
			close(results)
		}
		n++
	}

}

func run(max int) []int {
	fib := make([]int, max)
	fib[0] = 0
	fib[1] = 1

	for i := 2; i < max; i++ {
		fib[i] = fib[i-1] + fib[i-2]
	}
	return fib
}
