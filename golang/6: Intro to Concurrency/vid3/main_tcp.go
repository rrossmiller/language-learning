package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"sync"
	"time"
)

func main() {
	ttl, max := 10, 3
	tooMany()
	time.Sleep(3 * time.Second)
	var wg sync.WaitGroup

	// for 0-ttl requests
	for i := 0; i < ttl; i += max {
		limit := max
		if i+max > ttl { // dont exceed total
			limit = ttl - i
		}

		wg.Add(limit)
		for j := 0; j < limit; j++ {
			go func(j int) {
				defer wg.Done()

				conn, err := net.Dial("tcp", ":9090")
				check(err, "could not dial")

				sb, err := ioutil.ReadAll(conn)
				check(err, "could not read from conn")

				if string(sb) != "success" {
					log.Fatal("req err, req:", i+1+j)
				}

				fmt.Printf("req %d: %v\n", 1+i+j, string(sb))
			}(j)
		}
		wg.Wait()
	}
}

func tooMany() {
	for i := 0; i < 5; i++ {
		go func(j int) {
			conn, err := net.Dial("tcp", ":9090")
			check(err, "could not dial")

			sb, err := ioutil.ReadAll(conn)
			check(err, "could not read from conn")

			fmt.Printf("**req %d: %v\n", j, string(sb))
		}(i)
	}
}
func check(err error, s string) {
	if err != nil {
		log.Fatal(s, err)
	}
}
