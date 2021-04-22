#include <iostream>
#include <memory>
#include <vector>

class Base {
public:
    virtual int foo(int a) {
        std::cout << "BASE\n";
        return a;
    };
};

//NOTE: My initial error was missing "public" inheritance
class DerivedA : public Base {
public:
    int foo(int a) override {
        std::cout << "DERIVED A\n";
        return a * 2;
    };
};

class DerivedB : public Base {
public:
    int foo(int a) override {
        std::cout << "DERIVED B\n";
        return a * 2;
    };
};

int main() {
    std::cout << "Hello, polymorphism" << std::endl;
    std::vector<std::shared_ptr<Base>> vec;
    vec.emplace_back(std::make_shared<Base>());
    vec.emplace_back(std::make_shared<DerivedA>());
    vec.emplace_back(std::make_shared<DerivedB>());


//    std::shared_ptr<Base> b(std::make_shared<DerivedA>());
//    std::cout << b->foo(1) << "\n";

    for(const auto& elem: vec){
        elem->foo(1);
    }

    return 0;
}
