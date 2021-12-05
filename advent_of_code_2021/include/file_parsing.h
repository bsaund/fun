//
// Created by bsaund on 12/27/20.
//

#ifndef CPP_FILE_PARSING_H
#define CPP_FILE_PARSING_H

#include <fstream>
#include <iostream>

std::string read_from_file(const std::string &day) {
    std::ifstream f(day + ".txt");
    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
}

std::vector<std::string> split(const std::string &str, const std::string& delimiter) {
    std::vector<std::string> res;
    size_t pos_start=0, pos_end;
    size_t delim_len = delimiter.length();
    std::string token;
    while((pos_end = str.find(delimiter, pos_start)) != std::string::npos){
        token = str.substr(pos_start, pos_end-pos_start);
        pos_start = pos_end + delim_len;
        if(token.length() > 0) {
          res.push_back(token);
        }
    }
    token = str.substr(pos_start);
    if(token.length() > 0) {
      res.push_back(token);
    }
    return res;
}

#endif//CPP_FILE_PARSING_H
