package main

// import (
// 	"fmt"
// 	"sync"
// )

// type request func()

// // rate limiting
// func main() {
// 	requests := populateMap(100)

// 	var wg sync.WaitGroup
// 	maxReq := 10 // max batch of 10

// 	for i := 0; i < len(requests); i += maxReq {
// 		for j := i; j < i+maxReq; j++ {
// 			wg.Add(1)
// 			go func(r request) {
// 				defer wg.Done()
// 				r()
// 			}(requests[j])
// 		}
// 		wg.Wait()
// 		fmt.Println(maxReq, "reqs processed")
// 	}
// }

// func populateMap(ttl int) (requests map[int]request) {
// 	requests = map[int]request{}
// 	for i := 0; i < ttl; i++ {
// 		f := func(n int) request {
// 			return func() {
// 				fmt.Println("request", n)
// 			}
// 		}

// 		requests[i] = f(i)
// 	}
// 	return
// }
