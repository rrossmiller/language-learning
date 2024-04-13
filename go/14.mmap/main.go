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
		find4LetterWord(contents, false)
		times[i] = float64(time.Since(start).Microseconds())
	}
	mmtime := avg(times)
	find4LetterWord(contents, true)

	//mmap end

	// read file start
	for i := 0; i < count; i++ {
		start := time.Now()
		contents, err = os.ReadFile(pth)
		check(err)
		find4LetterWord(contents, false)
		times[i] = float64(time.Since(start).Microseconds())

	}
	fileRead := avg(times)
	find4LetterWord(contents, true)

	// read file end

	fmt.Println(strings.Split(string(contents), "\n")[1000:1002])
	fmt.Println(mmtime, "micro sec avg")
	fmt.Println(fileRead, "micro sec avg")
	xFaster := float64(fileRead) / float64(mmtime)
	fmt.Printf("mmap is %.3f times faster\n", xFaster)

	contents = make([]byte, reader.Len())
	_, err = reader.ReadAt(contents, 0)
	check(err)
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
func find4LetterWord(contents []byte, isPrint bool) {
	l := 0
	for i, w := range contents {
		if rune(w) == ' ' {
			if l == 4 {
				if isPrint {
					fmt.Println(string(contents[i-l:i]), " -- ", i)
				}
				return
			}
			l = 0
		} else {
			l++
		}
	}
}

func avg(times []float64) (ttl float64) {
	for _, v := range times {
		ttl += v
	}
	ttl = ttl / float64(len(times))
	return
}
