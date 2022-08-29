package main

import (
	"fmt"
	"gonum.org/v1/gonum/graph/encoding/dot"
	"gonum.org/v1/gonum/graph/graphs/gen"
	"gonum.org/v1/gonum/graph/simple"
	"log"
	"os"
)

func main() {
	dst := simple.NewDirectedGraph()
	gen.Complete(dst, gen.IDSet{2, 4, 5, 9})
	b, err := dot.Marshal(dst, "complete", "", "\t")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s\n", b)
	writeDot(b)
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func writeDot(b []byte) {
	err := os.WriteFile("g.dot", b, 0644) //644: -rw-r--r--
	check(err)
	// dot -Tpng g.dot > graph.png
}
