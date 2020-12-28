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

#endif  // CPP_PRINTING_H
