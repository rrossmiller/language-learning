package main

import (
	"C"
	"fmt"
)

func main() {}

//export hi
func hi(num int) C.int {
	fmt.Println("hello world")
	return C.int(num * 2)
}


