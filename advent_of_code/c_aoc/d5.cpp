#include <fstream>
#include <iostream>
#include <vector>

#include "include/file_parsing.h"
#include "include/printing.h"

std::string tmp_data =
    "FBFBBFFRLR\n"
    "BFFFBBFRRR\n"
    "FFFBBBFRRR\n"
    "BBFFBBFRLL";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1

  int max_id = 0;
  for (const std::string& line : data) {
    int r = 0, c = 0;
    int dr = 64, dc = 4;
    for (const auto& fb : line.substr(0, 7)) {
      r += (fb == 'B') * dr;
      dr /= 2;
    }
    for (const auto& lr : line.substr(7, 10)){
      c += (lr == 'R') * dc;
      dc /= 2;
    }
    int id = r * 8 + c;
    max_id = std::max(id, max_id);
//    std::cout << "Row " << r << " Col " << c << " id " << id << "\n";
  }
  std::cout << "max id " << max_id;
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2

  std::vector<int> ids;
  for (const std::string& line : data) {
    int r = 0, c = 0;
    int dr = 64, dc = 4;
    for (const auto& fb : line.substr(0, 7)) {
      r += (fb == 'B') * dr;
      dr /= 2;
    }
    for (const auto& lr : line.substr(7, 10)){
      c += (lr == 'R') * dc;
      dc /= 2;
    }
    int id = r * 8 + c;
    ids.push_back(id);
//    max_id = std::max(id, max_id);
//    std::cout << "Row " << r << " Col " << c << " id " << id << "\n";
  }

  std::sort(ids.begin(), ids.end());
  print(ids);
  for(int i=0; i<ids.size()-1; i++){
    if(ids[i+1] - ids[i] != 1){
      std::cout << "The missing seat is: " << ids[i] + 1 << "\n";
      break;
    }
  }
}

int main() {
  auto data_str = read_from_file("d5");
  // Comment out for running on real data
  //  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
