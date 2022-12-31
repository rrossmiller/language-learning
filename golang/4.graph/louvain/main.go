package main

import (
	"fmt"
	"louvain/ops"
	"strconv"

	"gonum.org/v1/gonum/graph/community"
	"gonum.org/v1/gonum/graph/simple"
)

func main() {
	rawEdges := ops.ReadEdgesFile("karate_club.csv")

	// create the graph
	g := simple.NewUndirectedGraph()
	for _, nodeIDs := range rawEdges.Rows {
		src, _ := strconv.Atoi(nodeIDs[0])
		tgt, _ := strconv.Atoi(nodeIDs[1])
		e := simple.Edge{F: simple.Node(src), T: simple.Node(tgt)} // create a new edge
		g.SetEdge(e)                                               // add the edge to the g (also creates the vert if it doesn't exist)
	}

	fmt.Println("****")
	resolution := 1.0
	r := community.Modularize(g, resolution, nil)
	// fmt.Println(rgString(r))
	// fmt.Println()

	out := make(map[int]int)
	for i, v := range r.Communities() {
		for _, w := range v {
			k := int(w.ID())
			out[k] = int(i)
		}
	}

	// b, err := json.MarshalIndent(out, "", "\t") // doesn't preserve key order
	b, _ := ops.MarshalClustersMap(out)
	ops.WriteFile(b, "vis/go_results.json")

	b, _ = ops.MarshalClusters(r.Communities())
	ops.WriteFile(b, "vis/gores.txt")
}
