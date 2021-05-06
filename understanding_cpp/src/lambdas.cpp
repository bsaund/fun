

#include <functional>
#include <iostream>


class Foo{
public:
    std::function<void(int)> bar_fn;
    std::function<void(int)> baz_fn;

    Foo(){
        bar_fn = std::bind(&Foo::bar, this, std::placeholders::_1);

        baz_fn = [&](int a) {return bar(a);};
    }

    void bar(int a){
        std::cout << "bar called with: " << a << "\n";
    }
};


int main() {
    std::cout << "Hello, reference wrapper" << std::endl;

    auto f = Foo();
    f.bar(3);
    f.bar_fn(2);
    f.baz_fn(1);

    return 0;
}