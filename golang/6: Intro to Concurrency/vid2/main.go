package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	now := time.Now()

	var wg sync.WaitGroup
	ttl := 11
	wg.Add(ttl - 1)
	for i := 1; i < ttl; i++ {
		go work(i*10, &wg)
	}
	fmt.Println("wait groups")
	wg.Wait()
	fmt.Printf("run time %v\n", time.Since(now))
}

func work(millis int, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(time.Duration(millis) * time.Millisecond)
	fmt.Printf("task %v\n", millis)
}
