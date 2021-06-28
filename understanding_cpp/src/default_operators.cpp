

#include <functional>
#include <iostream>

class Foo{
public:
    Foo(int val)
    : value(val)
    {

    }

public:
    const int value;
};


int main() {
    Foo foo(2);

    foo = Foo(3);

    std::cout << "foo: " << foo.value << "\n";

    return 0;
}//
// Created by bsaund on 6/3/21.
//
