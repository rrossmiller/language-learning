package main

import (
	"fmt"
	"time"
)

type Foo struct {
	Created time.Time
	// ...
}

func main() {
	x := Foo{Created: time.Now()}

	fmt.Println(time.Since(x.Created))
}
