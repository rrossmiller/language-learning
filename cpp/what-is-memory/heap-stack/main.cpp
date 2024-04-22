#include <format>
#include <iostream>
#include <string>

class Point {
   public:
    int x;
    int y;

    std::string toString() {
        return std::format("Point:\n\tp.x: {}\n\tp.y: {}", x, y);
    }

    void leak() {
        for (int i = 0; i < 10; i++) {
            int* x = new int;
        }
    }
};

class Foo {
   public:
    Point* p;
    Foo() {
    }
    Foo(Point* p) {
        p = p;
    }
};

int main() {
    Point* p = new Point;
    p->x = std::stoi("1");
    p->y = 0;

    // std::cout << p->toString() << std::endl;
    // std::cout << &p << std::endl;
    // delete p;

    Foo* f = new Foo(p);
    // f->p = new Point();
    // auto p = f->p;

    std::cout << p->toString() << std::endl;
    std::cout << "f " << f->p->toString() << std::endl;
    // std::cout << &p << std::endl;

    // free(p);
    delete f;

    // for (int i = 0; i < 10; i++) {
    //   int* x = new int;
    // }

    // p.leak();
}
