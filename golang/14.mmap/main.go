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
	pth := "donquijote.txt" // https://www.gutenberg.org/files/996/996-0.txt
	times := make([]float64, count)

	//mmap start
	reader, err := mmap.Open(pth)
	check(err)
	defer reader.Close()

	contents := make([]byte, reader.Len())
	var bytesRead int
	for i := 0; i < count; i++ {
		start := time.Now()
		bytesRead, err = reader.ReadAt(contents, 0)
		check(err)
		if bytesRead != reader.Len() {
			fmt.Println(len(contents))
			fmt.Println(bytesRead)
			panic("ahhhh")
		}
		times[i] = float64(time.Since(start).Microseconds())
	}
	mmtime := avg(times)

	//mmap end

	// read file start
	for i := 0; i < count; i++ {
		start := time.Now()
		contents, err = os.ReadFile(pth)
		check(err)
		times[i] = float64(time.Since(start).Microseconds())

	}
	fileRead := avg(times)
	// read file end

	fmt.Println(strings.Split(string(contents), "\n")[1000:1002])
	fmt.Println(mmtime, "micro sec avg")
	fmt.Println(fileRead, "micro sec avg")
	xFaster := float64(fileRead) / float64(mmtime)
	fmt.Printf("mmap is %.3f times faster\n", xFaster)
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func avg(times []float64) (ttl float64) {
	for _, v := range times {
		ttl += v
	}
	ttl = ttl / float64(len(times))
	return
}
