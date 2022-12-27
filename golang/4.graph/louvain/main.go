package main

import (
	"fmt"
	"louvain/ops"
	"math/rand"
	"strconv"

	"gonum.org/v1/gonum/graph/simple"
)

func main() {
	rawEdges := ops.ReadEdgesFile("edges.csv")
	rawEdges.Print(5)

	graph := simple.NewUndirectedGraph()
	fmt.Println(len(rawEdges.Rows))

	// for _, nodeIDs := range rawEdges.Rows[:10] {
	// 	src, _ := strconv.Atoi(nodeIDs[0])
	// 	tgt, _ := strconv.Atoi(nodeIDs[1])
	for _, i := range rand.Perm(len(rawEdges.Rows))[:100] {
		src, _ := strconv.Atoi(rawEdges.Rows[i][0])
		tgt, _ := strconv.Atoi(rawEdges.Rows[i][1])
		e := simple.Edge{F: simple.Node(src), T: simple.Node(tgt)} // create a new edge
		graph.SetEdge(e)                                           // add the edge to the graph (also creates the vert if it doesn't exist)
	}
	// ops.WriteDotFile(graph)
}
