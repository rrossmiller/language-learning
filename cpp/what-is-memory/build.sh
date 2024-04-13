clear
if [[ $# -gt 0 ]]; then
	g++ $1/main.cpp -std=c++20 &&
		./a.out
else
	g++ bits/main.cpp -std=c++20 &&
		./a.out
fi
