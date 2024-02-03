clear
if [[ -e aoc ]]; then
	rm upordown
fi

if [[ $# -eq 0 ]]; then
	n=11
else
	n=$1
fi

clang++ -std=c++23 *.cpp -o upordown &&
	echo 'running...' &&
	./upordown
