package main

import (
	"fmt"
	"louvain/ops"
	"sort"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/community"
	"gonum.org/v1/gonum/graph/simple"
)

type clusterId int

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

	out := make(map[int]clusterId)
	for i, v := range r.Communities() {
		for _, w := range v {
			k := int(w.ID())
			out[k] = clusterId(i)
		}
	}

	// b, err := json.MarshalIndent(out, "", "\t")
	b, _ := marshalClustersMap(out)
	ops.WriteFile(b, "vis/go_results.json")

	b, _ = marshalClusters(r.Communities())
	ops.WriteFile(b, "vis/gores.txt")
}

func marshalClusters(clusters [][]graph.Node) ([]byte, error) {
	var sb strings.Builder
	for _, c := range clusters {
		sort.Slice(c, func(i, j int) bool {
			return c[i].ID() < c[j].ID()
		})
		for _, n := range c {
			sb.WriteString(fmt.Sprintf("%v,", n))
		}
		sb.WriteString("\n")
	}
	return []byte(sb.String()), nil
}
func marshalClustersMap(out map[int]clusterId) ([]byte, error) {
	var sb strings.Builder
	sb.WriteString("{\n")
	keys := make([]int, 0, len(out))
	for k := range out {
		keys = append(keys, k)
	}
	sort.Ints(keys)
	var s string
	for i, k := range keys {
		ci := out[k]

		if i < len(keys)-1 {
			s = fmt.Sprintf("\t\"%v\": %v,\n", k, ci)
		} else {
			s = fmt.Sprintf("\t\"%v\": %v", k, ci)
		}
		sb.WriteString(s)
	}
	sb.WriteString("\n}")
	return []byte(sb.String()), nil
}

func rgString(rg community.ReducedGraph) string {
	return fmt.Sprintf("C: %v \n\nstructure: %v \n\nExp:%v", rg.Communities(), rg.Structure(), rg.Expanded())
}
