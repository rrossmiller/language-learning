package main

import (
	"C"
)

func main() {}

//export Gt3
func Gt3(num float64) bool {
	return num > 3
}
