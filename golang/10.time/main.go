package main

import (
	"flag"
	"fmt"
	"log"
	"os/exec"
	"time"
)

func main() {
	perf := flag.Bool("p", false, "perf test")
	flag.Parse()
	args := flag.Args()
	if *perf {
		perfTest(1000, args)
	} else {
		start := time.Now()
		cmd := exec.Command(args[0], args[1:]...)
		out, err := cmd.Output()

		if err != nil {
			// panic(err)
			log.Fatal(err)
		}
		fmt.Println(string(out))
		fmt.Printf("elapsed: %v\n", time.Since(start))
	}
}

func perfTest(n int, args []string) {
	times := make([]time.Duration, n)

	for i := 0; i < n; i++ {
		start := time.Now()
		cmd := exec.Command(args[0], args[1:]...)
		_, err := cmd.Output()

		if err != nil {
			// panic(err)
			log.Fatal(err)
		}
		times = append(times, time.Since(start))
	}

	t := AvgTime(times)
	fmt.Printf("avg elapsed over %d tests: %f ms\n", n, t)
}

func AvgTime(times []time.Duration) float64 {
	ttl := len(times)
	sum := float64(0)
	for i := 0; i < ttl; i++ {
		sum += float64(times[i].Milliseconds())
	}
	return sum / (float64(ttl))
}
