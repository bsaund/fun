//
// Created by bsaund on 12/29/20.
//

#ifndef CPP_CONTAINER_CONVERSIONS_H
#define CPP_CONTAINER_CONVERSIONS_H

#include <vector>
#include <set>

template <typename T>
std::set<T> toSet(const std::vector<T>& v){
  std::set<T> s;
  for(const auto& elem: v){
    s.insert(elem);
  }
  return s;
}

std::vector<char> toVector(const std::string& str){
  std::vector<char> v;
  for(const char& c: str){
    v.emplace_back(c);
  }
  return v;
}

std::set<char> toSet(const std::string& str){
  return toSet(toVector(str));
}

template <typename T>
std::set<T> set_intersect(const std::set<T>& a, const std::set<T>& b){
  std::set<T> s;
  std::set_intersection(a.begin(), a.end(), b.begin(), b.end(), std::inserter(s, s.begin()));
  return s;
}

#endif  // CPP_CONTAINER_CONVERSIONS_H
