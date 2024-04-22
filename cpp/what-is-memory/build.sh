clear
if [[ $# -gt 0 ]]; then
	g++ $1/main.cpp &&
		./a.out
else
	g++ bits/main.cpp &&
		./a.out
fi
