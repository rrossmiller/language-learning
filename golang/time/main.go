package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"time"
)

func main() {
	start := time.Now()
	cmd := exec.Command(os.Args[1], os.Args[2:]...)
	out, err := cmd.Output()

	if err != nil {
		// panic(err)
		log.Fatal(err)
	}
	fmt.Println(string(out))
	fmt.Printf("elapsed: %v\n", time.Since(start))
}
