#include <fstream>
#include <iostream>
#include <vector>

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

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1
  std::vector<int> adapters{0};

  for (const auto& line : data) {
    int jolts;
    sscanf(line.c_str(), "%d", &jolts);
    //    std::cout << line << "\n";
    adapters.push_back(jolts);
  }
  std::sort(adapters.begin(), adapters.end());
  adapters.push_back(adapters.back() + 3);

  int count_ones = 0, count_threes = 0;
  //  for(const auto& j: adapters){
  //    std::cout << j << "\n";
  //  }
  for (int i = 0; i < adapters.size() - 1; i++) {
    if(adapters[i+1] - adapters[i] == 1){
      count_ones++;
    }
    if(adapters[i+1] - adapters[i] == 3){
      count_threes++;
    }
  }
  std::cout << count_ones * count_threes << "\n";
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2
  std::vector<int> adapters{0};

  for (const auto& line : data) {
    int jolts;
    sscanf(line.c_str(), "%d", &jolts);
    //    std::cout << line << "\n";
    adapters.push_back(jolts);
  }
  std::sort(adapters.begin(), adapters.end());

  int longest_ones_string = 0;
  int tmp_ones_string = 0;
  std::vector<int> ones_in_a_row;
  for(int i=0; i < adapters.size()-1; i++){
//    std::cout << adapters[i];
    int diff = adapters[i+1] - adapters[i];
    if(diff == 1){
      tmp_ones_string++;
    }
    else{
      longest_ones_string = std::max(longest_ones_string, tmp_ones_string);
//      std::cout << "  longest ones string: " << longest_ones_string << "\n";
      if(tmp_ones_string > 1){
        ones_in_a_row.push_back(tmp_ones_string);
      }
      tmp_ones_string=0;
    }
  }
  ones_in_a_row.push_back(tmp_ones_string);

  long arrangements = 1;
  for(const auto ones_string: ones_in_a_row){
    std::cout << ones_string << "\n";
    if(ones_string == 2){
      arrangements *= 2;
    }
    if(ones_string == 3){
      arrangements *= 4;
    }
    if(ones_string == 4){
      arrangements *= 7;
    }
  }
//  std::cout << "longest ones string " << longest_ones_string << "\n";
  std::cout << arrangements << "\n";
}

int main() {
  auto data_str = read_from_file("d10");
  // Comment out for running on real data
  //  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
