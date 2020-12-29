//
// Created by bsaund on 12/27/20.
//

#ifndef CPP_PRINTING_H
#define CPP_PRINTING_H

#include <string>
#include <vector>
#include <iostream>

void print(const std::vector<std::string> &v) {
  for(const auto& line: v){
    std::cout << line << "\n";
  }
}

template <typename T>
void print(const std::vector<T> &v){
  for(const T& val: v){
    std::cout << val << ", ";
  }
  std::cout << "\n";
}



#endif  // CPP_PRINTING_H
