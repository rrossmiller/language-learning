package main

import (
	"encoding/json"
	"graph/simplegraph"
	"os"
)

// simplegraph would be nicer if it were documented, or even commented
// Also common naming convention would be nice (AddNode vs ConnectNode [AddEdge])
func main() {
	simplegraph.Initialize("test.db")
	x := map[string]any{
		"id": "A",
		"a":  1,
	}
	b, _ := json.Marshal(x)
	simplegraph.AddNode("", b, "test.db")

	x = map[string]any{
		"id": "B",
		"a":  2,
	}
	b, _ = json.Marshal(x)
	simplegraph.AddNode("", b, "test.db")

	x = map[string]any{
		"id": "C",
		"a":  3,
	}
	b, _ = json.Marshal(x)
	simplegraph.AddNode("", b, "test.db")

	simplegraph.ConnectNodes("A", "C", "test.db")

	x = map[string]any{
		"type": "relation",
	}
	b, _ = json.Marshal(x)
	simplegraph.ConnectNodesWithProperties("A", "B", b, "test.db")

	s := simplegraph.Visualize([]string{"A", "B", "C"}, "test.db")
	os.WriteFile("g.dot", []byte(s), 0644)
}
