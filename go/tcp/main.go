package main

import (
	"fmt"
	"io"
	"net"
	"time"
)

var lorem =  "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis."
func main() {
	port := ":9000"
	// server
	go listen(port)
	time.Sleep(100 * time.Millisecond) // wait for the server to start up

	//client
	conn, err := net.Dial("tcp", port)
	if err != nil {
		panic(err)
	}
	fmt.Println("dialed tcp")
	b, err := io.ReadAll(conn)
	fmt.Printf("\nread:\n%d bytes\n%s", len(b), string(b))
}

func listen(port string) {
	ln, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println("server error")
		panic(err)
	}
	fmt.Println("server listening")
	for {
		conn, err := ln.Accept()
		if err != nil {
			panic(err)
		}

		// handle connection
		go func(conn net.Conn) {
			fmt.Println("writing lorem ipsum")
			conn.Write([]byte(lorem))
			err := conn.Close()
			if err != nil {
				panic(err)
			}
		}(conn)
	}
}
