package main

import (
	"fmt"
	"regexp"
)

var doubleStr = regexp.MustCompile(`"([\s\S][^"]*)"`)

func main() {
	content := []byte(`
    "hi"
    'hello'
    "hey"
    `)
	f(content)
	fmt.Println("..")
	fmt.Printf("%s\n", content)

}
func f(content []byte) {

	f := doubleStr.FindAllSubmatchIndex(content, -1)
	for _, x := range f {
		fmt.Println(x)
		fmt.Printf("> %s\n", content[x[0]:x[1]])
		fmt.Printf("> %s\n", content[x[2]:x[3]])
		fmt.Println()
	}
	content[0] = byte('-')
}
