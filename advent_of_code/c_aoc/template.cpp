#include <fstream>
#include <iostream>
#include <vector>

#include "include/file_parsing.h"
#include "include/printing.h"

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

}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";

}

int main() {
  auto data_str = read_from_file("d1");
  // Comment out for running on real data
  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}