rm louvain
clear
echo building
go build
echo running
echo
./louvain
if [[ $# -gt 0 ]]; then
	dot -Tpng vis/g.dot >vis/graph.png
	open vis/graph.png
fi
