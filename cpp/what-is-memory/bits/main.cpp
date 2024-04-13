#include <cstdint>
#include <cstdio>

// readbit macro
#define BITVALUE(x, n) ((x >> n) & 0x1)
// #define READBIT3 0b1<<3
// #define READBIT3 0b1000
#define READBIT3 0x8

void read_bit(int8_t x, int8_t n) {
    // printf("shift right 3 %d\n", x >> n);           // x=42,n=3 ->  101 =
    // 4+0+1
    printf("bit %d: %d\n", n, (x >> n) & 0x1);  // 101 = 4+0+1
}
int main() {
    // auto v = std::vector<int>{1, 2, 3, 4};
    //
    // for (auto i : v) {
    // std::cout << i << std::endl;
    // }
    //
    uint8_t x = 42;
    int8_t num_bits = sizeof(x) * 8;
    for (int i = num_bits - 1; i >= 0; i--) {
        auto b = BITVALUE(x, i);
        printf("%d", b);
    }
    printf("\n");
    printf("%d\n", x);
    printf("num bits %d\n", num_bits);
    read_bit(x, 3);
    printf("\n");
    read_bit(x, 4);
    printf("\n");
    printf("bitval 3 %d\n", BITVALUE(x, 3));

    bool a = (x & READBIT3);
    printf("readbit 3 %d\n", a);
}
