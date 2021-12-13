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


class Point {
public:
    int x, y;
    Point(int x_, int y_) : x(x_), y(y_) {}
    bool operator==(const Point &other) const {
        return x == other.x and y == other.y;
    }
};

template <typename T>
std::vector<Point> itercoords(const std::vector<std::vector<T>> &d){
    std::vector<Point> p;
    p.reserve(d.size() * d[0].size());
    for(int i=0; i<d.size(); i++){
        for(int j=0; j<d.size(); j++){
            p.template emplace_back(i, j);
        }
    }
    return p;
}

template<>
struct std::hash<Point>
{
    std::size_t operator()(const Point& p) const{
        return std::hash<int>()(p.x) ^ (std::hash<int>()(p.y) << 1);
    }
};


#endif  // CPP_UTILS_H
