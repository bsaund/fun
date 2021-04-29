//
// Created by bsaund on 4/24/21.
//
#include <algorithm>
#include <functional>
#include <iostream>
#include <list>
#include <memory>
#include <random>
#include <vector>

template<typename T>
void print_vector(std::vector<T> v, const std::string& msg){
    std::cout << msg << "\n";
    for(auto i: v) std::cout << i << ' ';
    std::cout << "\n";
}

template<typename T>
void print_optional(std::optional<T> o){
    if(o.has_value()){
        std::cout << o.value() << "\n";
        return;
    }
    std::cout << "<None>\n";
}

void cppref_example() {
    std::list<int> l(10);

    std::iota(l.begin(), l.end(), -4);
    std::vector<std::reference_wrapper<int>> v(l.begin(), l.end());

    // can't use shuffle on a list (requires random access), but can use it on a vector
    std::shuffle(v.begin(), v.end(), std::mt19937{std::random_device{}()});

    std::cout << "Contents of the list: ";
    for (int n : l) {
        std::cout << n << ' ';
    }

    std::cout << "\nContents of the list, as seen through a shuffled vector: ";
    for (int i : v) {
        std::cout << i << ' ';
    }

    std::cout << "\n\nDoubling the values in the initial list...\n\n";
    for (int &i : l) {
        i *= 2;
    }

    std::cout << "Contents of the list, as seen through a shuffled vector: ";
    for (int i : v) {
        std::cout << i << ' ';
    }
}

void optional() {
    int my_int = 5;
    std::optional<int> opt(my_int);

    print_optional(opt);

    std::optional<std::reference_wrapper<int>> ref_opt(my_int);

    my_int = 6;
    print_optional(ref_opt);

    ref_opt.reset();
    print_optional(ref_opt);

}

void vectors(){
    int my_int = 123;
    std::vector<int> v{my_int};
    print_vector(v, "Standard Vector");

    std::vector<std::reference_wrapper<int>> ref_v{my_int};
    print_vector(ref_v, "Reference Vector");

    std::vector<int*> ptr_v{&my_int};
    std::cout << "Pointer vector\n";
    std::cout << *ptr_v[0] << "\n";

    my_int = -456;
    print_vector(v, "Changed my_int and vector is still:");
    print_vector(ref_v, "Reference vector is now");
    std::cout << "Pointer vector is now\n";
    std::cout << *ptr_v[0] << "\n";
}

int main() {
    std::cout << "Hello, reference wrapper" << std::endl;


//    cppref_example();
//    vectors();
    optional();

    return 0;
}
