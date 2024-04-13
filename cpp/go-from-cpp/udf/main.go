package main

import (
	"C"
)

func main() {}

//export gt3
func gt3(num float64) bool {
	return num > 3
}
