#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

//#include "absl/strings/match.h"
#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"

std::string tmp_data =
    "1721\n"
    "979\n"
    "366\n"
    "299\n"
    "675\n"
    "1456";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

bool is_contained(int query, std::vector<int> list){
  std::sort(list.begin(), list.end());
  int lower = 0, upper = (int)list.size()-1;

  while(lower < upper){
    int sum = list[lower] + list[upper];
    if(sum == query) {
      return true;
    }
    else if(sum < query){
      lower++;
    }
    else if(sum > query){
      upper--;
    }
  }
  return false;
}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1

  std::vector<int> prev;
  prev.reserve(10000);

  int i;

  for(i=0; i<25; i++){
    int v;
    sscanf(data[i].c_str(), "%d", &v);
    prev.insert(prev.begin(), v);
  }
  i++;

  while(i < data.size()){
    int v;
    sscanf(data[i].c_str(), "%d", &v);
    if(!is_contained(v, prev)){
      std::cout << "The first number not obeying XMAS cypher is " << v;
      break;
    }
    prev.pop_back();
    prev.insert(prev.begin(), v);

    i++;
  }




//  for (const auto& line : data) {
//    sscanf(line.c_str(), "");
//    std::cout << line << "\n";
//  }
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";

  int target_number = 29221323;
  std::vector<int> contig;

  for(const auto &str: data){
    int v;
    sscanf(str.c_str(), "%d", &v);
    contig.insert(contig.begin(), v);

    int sum = std::accumulate(contig.begin(), contig.end(), 0);

    while(sum >= target_number){
      if(sum == target_number){
        int cypher = *std::max_element(contig.begin(), contig.end()) + *std::min_element(contig.begin(), contig.end());
        std::cout << "The cypher weakness is " << cypher << "\n";
        return;
      }
      contig.pop_back();
      sum = std::accumulate(contig.begin(), contig.end(), 0);
    }
  }

  // Part 2
}

int main() {
  auto data_str = read_from_file("d9");
  // Comment out for running on real data
//  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
