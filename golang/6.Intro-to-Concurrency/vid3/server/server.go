package main

import (
	"fmt"
	"log"
	"net"
	"sync/atomic"
	"time"
)

func main() {
	listener, err := net.Listen("tcp", ":9090")
	check(err, "Could not create listener")
	fmt.Println("listenting on 9090")
	//listen
	var connections int32
	for {
		conn, err := listener.Accept()
		check(err, "")
		connections++

		go func() {
			//serve connections
			defer func() {
				conn.Close()
				atomic.AddInt32(&connections, -1)
			}()

			if atomic.LoadInt32(&connections) > 3 {
				fmt.Println("too many connections")
				return
			}

			time.Sleep(time.Second)
			_, err := conn.Write([]byte("success"))
			check(err, "write error")
		}()
	}
}

func check(err error, s string) {
	if err != nil {
		log.Fatal(s, err)
	}
}
