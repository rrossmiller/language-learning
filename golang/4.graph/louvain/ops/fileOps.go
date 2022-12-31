package ops

import (
	"encoding/csv"
	"os"
	"strings"

	"gonum.org/v1/gonum/graph/encoding/dot"
	"gonum.org/v1/gonum/graph/simple"
)

func Check(e error) {
	if e != nil {
		panic(e)
	}
}

func ReadCsv(path string) Record {
	edgesFile, err := os.ReadFile(path)
	Check(err)
	edges := csv.NewReader(strings.NewReader(string(edgesFile)))

	allEdges, err := edges.ReadAll()
	Check(err)

	return Record{allEdges[0], allEdges[1:]}
}
func ReadEdgesFile(path string) Record {
	edges := ReadCsv(path)
	e := make([][]string, 0)
	for _, v := range edges.Rows {
		e = append(e, v[:2])
	}
	return Record{edges.Header[:2], e}
}

// write a dotfile
func WriteDotFile(graph *simple.DirectedGraph) {
	b, err := dot.Marshal(graph, "complete", "", "\t")
	Check(err)

	DirExists("vis")
	err = os.WriteFile("vis/g.dot", b, 0644) //644: -rw-r--r--
	Check(err)

	// fmt.Println("dot -Tpng ../vis/g.dot > ../vis/graph.png") // run to make png
}

func WriteFile(b []byte, fname string) {
	DirExists("vis")
	err := os.WriteFile(fname, b, 0644) //644: -rw-r--r--
	Check(err)
}

func DirExists(pth string) {
	if _, err := os.Stat(pth); os.IsNotExist(err) {
		os.Mkdir(pth, 0750)
	}
}
