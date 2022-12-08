// Copyright 2017 The go-python Authors.  All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package slices

import (
	"fmt"
)

func NotRecursive(max, numWorkers int, verbose bool) {
	// start := time.Now()
	ch := make(chan int)
	go run(max, ch)

	if verbose {
		for msg := range ch {
			fmt.Println(msg)
		}
	}
	// elapsed := fmt.Sprintf("elapsed %v", time.Since(start))
	// fmt.Println(elapsed)
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
