clear
if [[ $# -gt 0 ]]; then
	echo "look in the leaks report. With MallocStackLogging=1, line numbers should be available for where the leak is"
	export MallocStackLogging=1
	g++ ./main.cpp -std=c++20 -g -o bank &&
		leaks --atExit --list -- ./bank 0 | less
else
	g++ ./*.cpp -std=c++20 -o bank &&
		./bank
fi
