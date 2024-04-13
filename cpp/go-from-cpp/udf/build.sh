
# go build -buildmode=c-shared -o libgooey.dylib gooey.go || exit 1

# GOOS=linux 
# GOARCH=amd64
go build -buildmode=c-shared -o libgt3.so main.go || exit 1

g++ test.cpp -L. -lgt3 -std=c++17 || exit 1

# just pass in the path to libgt3.so directly in the g++ call
# g++ test.cpp libgt3.so -std=c++20 || exit 1
./a.out
