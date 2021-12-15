#include <iostream>
#include <list>

void listInsertion(){
    std::cout << ".================.\n| List Insertion |\n'================'\n\n";

    std::list<int> lst{1,2,3};
    for(auto it=lst.begin(); it!=lst.end(); it){
        std::cout << *it << ", ";
        lst.insert(it, *it++*10);
//        it++;
    }
    std::cout << "\n";


    std::cout << "\nIn the end the list is: \n";
    for(auto n: lst){
        std::cout << n << ", ";
    }
    std::cout << "\n";
}

int main(){
    listInsertion();
    return 0;
}