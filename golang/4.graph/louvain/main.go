package main

import (
	"fmt"
	"louvain/ops"
	"strconv"

	"gonum.org/v1/gonum/graph/simple"
)

func main() {
	rawEdges := ops.ReadEdgesFile("karate_club.csv")
	rawEdges.Print(5)

	graph := simple.NewDirectedGraph()
	fmt.Println(len(rawEdges.Rows))

	for _, nodeIDs := range rawEdges.Rows {
		src, _ := strconv.Atoi(nodeIDs[0])
		tgt, _ := strconv.Atoi(nodeIDs[1])
		// for _, i := range rand.Perm(len(rawEdges.Rows)) {
		// 	src, _ := strconv.Atoi(rawEdges.Rows[i][0])
		// 	tgt, _ := strconv.Atoi(rawEdges.Rows[i][1])
		e := simple.Edge{F: simple.Node(src), T: simple.Node(tgt)} // create a new edge
		graph.SetEdge(e)                                           // add the edge to the graph (also creates the vert if it doesn't exist)
	}
	ops.WriteDotFile(graph)
}
