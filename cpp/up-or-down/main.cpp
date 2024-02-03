#include <cstdio>
#include <string>
using std::string;

int main() {
    int x, y = 0;
    // down
    if (&x > &y) {
        printf("Ans: down\n");
    } else {
        printf("Ans: up\n");
    }
}
