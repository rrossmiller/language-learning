package main

import (
	"fmt"
	"os"
	"strings"
)

const pth = "AHFS/pg_0.txt"

func main() {
	//all of a files contents into memory
	dat, err := os.ReadFile(pth)
	check(err)
	firstFive := strings.Split(string(dat), "\n")[:5]
	for _, l := range firstFive {
		fmt.Println(l)
	}
	fmt.Println()

	// more controll over what parts of a file are read
	f, err := os.Open(pth)
	check(err)

	b1 := make([]byte, 10)
	n1, err := f.Read(b1)
	check(err)
	fmt.Printf("%d bytes: %s\n", n1, string(b1[:n1]))
}
