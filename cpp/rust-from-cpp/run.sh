clear

cargo build --release

cbindgen --crate rust_from_cpp --output rusty.h #--lang c
# gcc  main.c -L target/release -lrust_from_cpp -lpthread -ldl &&
g++ main.cpp -L target/release -lrust_from_cpp -std=c++17 &&
	./a.out
