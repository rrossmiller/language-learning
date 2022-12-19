package main

import (
	"fmt"
	"time"
)

func task(millis int) {
	time.Sleep(time.Duration(millis) * time.Millisecond)
	fmt.Printf("task %v\n", millis)
}
