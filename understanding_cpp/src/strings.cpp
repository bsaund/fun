//
// Created by bsaund on 9/20/21.
//
#include <string>
#include <iostream>

std::string areEqual(const std::string &s1, const std::string &s2){
    return s1 == s2 ? "equal" : "not equal";
}

void compareStrings(){

    std::string s1("abc");
    std::string s2("abc");
    std::string s3(10, '\0');
    s3 = "abc";
    std::string s4(3, '\0');
    sscanf("abc", "%s", s4.c_str());
    std::string s5(10, '\0');
    sscanf("abc", "%s", s5.c_str());
    std::string s6(10, '\0');
    sscanf("abc", "%s", s6.c_str());
    s6.shrink_to_fit();



    std::cout << "s1 and s2 are " << areEqual(s1, s2) << "\n";
    std::cout << "s1 and s3 are " << areEqual(s1, s3) << "\n";
    std::cout << "s1 and s4 are " << areEqual(s1, s4) << "\n";
    std::cout << "s1 and s5 are " << areEqual(s1, s5) << "\n";
    std::cout << "s1 and s6 are " << areEqual(s1, s6) << "\n";
}


int main(){
    compareStrings();
}