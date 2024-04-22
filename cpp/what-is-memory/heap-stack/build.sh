clear
if [[ $# -gt 0 ]]; then
	echo "look in the leaks report. With MallocStackLogging=1, line numbers should be available for where the leak is"
	export MallocStackLogging=1
	g++ ./main.cpp -std=c++20 -g &&
		leaks --atExit --list -- ./a.out | less
else
	g++ ./main.cpp -std=c++20 &&
		./a.out
fi
