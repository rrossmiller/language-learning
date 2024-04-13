#include <iostream>
#include <vector>

#include "libgooey.h"

int main() {
    std::cout << hi(9) << std::endl;

    auto v = std::vector<int>{1, 2, 3, 4};

    for (auto i : v) {
        std::cout << i << std::endl;
    }

    return 0;
}
