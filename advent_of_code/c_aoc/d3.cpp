#include <fstream>
#include <iostream>
#include <vector>

#include "include/file_parsing.h"
#include "include/printing.h"

std::string tmp_data =
    "..##.......\n"
    "#...#...#..\n"
    ".#....#..#.\n"
    "..#.#...#.#\n"
    ".#...##..#.\n"
    "..#.##.....\n"
    ".#.#.#....#\n"
    ".#........#\n"
    "#.##...#...\n"
    "#...##....#\n"
    ".#..#...#.#";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1
  std::vector<std::vector<bool>> is_tree;
  for (const std::string& line : data) {
//    sscanf(line.c_str(), "");
    is_tree.emplace_back();
    for (const char& c: line){
//      std::cout << c;
      is_tree.back().push_back(c == '#');
    }
//    std::cout << "length: " << is_tree.back().size() << "\n";
  }

  int l = is_tree[0].size();
  int x = 0;
  int count = 0;
  for(const auto& row: is_tree){
    if(row[x % l]){
      count++;
    }
    x += 3;
  }
  std::cout << "count: " << count << "\n";
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2
  std::vector<std::vector<bool>> is_tree;
  for (const std::string& line : data) {
//    sscanf(line.c_str(), "");
    is_tree.emplace_back();
    for (const char& c: line){
      is_tree.back().push_back(c == '#');
    }
  }

  int l = is_tree[0].size();
  std::vector<int> counts;
  for(int dx: {1, 3, 5, 7}) {
    int x =0;
    int count = 0;
    for (const auto& row : is_tree) {
      if (row[x % l]) {
        count++;
      }
      x += dx;
    }
    counts.push_back(count);
  }

  int count = 0;
  int x=0;
  for (int i=0; i<is_tree.size(); i+=2){
    auto row = is_tree[i];
    if (row[x % l]) {
      count++;
    }
    x += 1;
  }
  counts.push_back(count);

  int prod = 1;
  for(auto num: counts){
    prod *= num;
  }


  std::cout << "prod: " << prod << "\n";
}

int main() {
  auto data_str = read_from_file("d3");
  //===========================
  // Comment out for running on real data
//  data_str = tmp_data;
  //===========================
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
