#include <stdio.h>

#include "rusty.h"

int main() {
    int result = rust_function();
    printf("Called Rust function, result: %d\n", result);

    bool b = greater_than_5(4);
    printf("%d\n", b);
    b = greater_than_5(6);
    printf("%d\n", b);
}
