
# go build -buildmode=c-shared -o libgooey.dylib gooey.go || exit 1

GOOS=linux 
go build -buildmode=c-shared -o libgooey.so gooey.go || exit 1

g++ main.cpp -L. -lgooey -std=c++20 || exit 1
./a.out
