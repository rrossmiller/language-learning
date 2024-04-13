clang leaker.cpp -o leaker

# Run leaks detecting tool
leaks -atExit -- ./leaker | grep LEAK:

