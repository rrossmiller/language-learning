package main

import (
	"fmt"
	"os"
	"strings"
	"time"

	"golang.org/x/exp/mmap"
)

func main() {
	count := 1000
	pth := "tgresponse"

	//mmap start
	start := time.Now()
	reader, err := mmap.Open(pth + "/PaperSrc.csv")
	check(err)
	defer reader.Close()

	fmt.Printf("reader.Len(): %v\n", reader.Len())

	contents := make([]byte, reader.Len())
	var bytesRead int
	for i := 0; i < count; i++ {
		bytesRead, err = reader.ReadAt(contents, 0)
		check(err)
	}
	if bytesRead != reader.Len() {
		fmt.Println(len(contents))
		fmt.Println(bytesRead)
		panic("ahhhh")
	}
	mmtime := time.Since(start)
	//mmap end

	// read file start
	start = time.Now()
	for i := 0; i < count; i++ {
		contents, err = os.ReadFile(pth + "/PaperSrc.csv")
		check(err)
	}
	two := time.Since(start)

	// read file end
	fmt.Println(strings.Split(string(contents), "\n")[:2])

	fmt.Println(mmtime)
	fmt.Println(two)
	fmt.Println(float32(two) / float32(mmtime))
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
