package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	now := time.Now()
	waitGroupsJoinPoint()
	// channelJoinPoit()
	fmt.Printf("run time %v\n", time.Since(now))
}

func waitGroupsJoinPoint() {
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		task(400)
	}()

	go func() {
		defer wg.Done()
		task(500)
	}()
	fmt.Println("wait groups")
	wg.Wait()
}

// this is dumb. use wait groups if data isn't getting passed betwen goroutines
func channelJoinPoit() {
	ttl := 2
	done := make(chan string, ttl)
	go func() {
		task(400)
		done <- "t4"
	}()

	go func() {
		task(500)
		done <- "t5"
	}()
	fmt.Println("channel join point")

	cnt := 0
	for i := range done {
		fmt.Println(i, cnt)
		cnt += 1
		if cnt == ttl {
			close(done)
		}
	}
}
