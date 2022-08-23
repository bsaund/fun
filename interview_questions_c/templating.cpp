#include <iostream>

template <typename T, typename U>
T add(const T &a, const U &b){
    return a + b;
}




int main(){

    std::cout << add(int(1), int(2)) << "\n";
    std::cout << add(long(1), long(2)) << "\n";
    std::cout << add('a', 1) << "\n";
    std::cout << char('a' + 'b') << "\n";
}
