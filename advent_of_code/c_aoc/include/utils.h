//
// Created by bsaund on 12/27/20.
//

#ifndef CPP_UTILS_H
#define CPP_UTILS_H

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


void check(bool should_be_true, const std::string& msg = ""){
  if(should_be_true){
    return;
  }
  std::cout << msg << "\n";
  throw std::logic_error("check failed: " + msg);
}


#endif  // CPP_UTILS_H
