package ops

import "fmt"

type Record struct {
	Header []string
	Rows   [][]string
}

func (r *Record) Print(n int) {
	fmt.Printf(`Header: %v
	%v`, r.Header, r.Rows[:n])
	fmt.Println()
}
