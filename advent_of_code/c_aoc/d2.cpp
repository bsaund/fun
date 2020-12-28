#include <fstream>
#include <iostream>
#include <vector>

#include "include/file_parsing.h"
#include "include/printing.h"

std::string tmp_data =
    "1-3 a: abcde\n"
    "1-3 b: cdefg\n"
    "2-9 c: ccccccccc";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  int valid_count = 0;
  for (const auto& line : data) {
    int lower, upper;
    char c;
    std::string s(100, '\0');
    sscanf(line.c_str(), "%d-%d %c: %s", &lower, &upper, &c, s.c_str());
//    std::cout << line << "\n";
    int char_count = std::count(s.begin(), s.end(), c);
//    std::cout << "Char " << c << " lower: " << lower << " upper: " << upper << " char count: " << char_count
//              << " s: " << s << "\n";
        if (char_count >= lower && char_count <= upper) {
      valid_count++;
    }
  }
  std::cout << "valid_count: " << valid_count << "\n";
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  int valid_count = 0;
  for (const auto& line : data) {
    int lower, upper;
    char c;
    std::string s(100, '\0');
    sscanf(line.c_str(), "%d-%d %c: %s", &lower, &upper, &c, s.c_str());
//    std::cout << line << "\n";
    int char_count = std::count(s.begin(), s.end(), c);
//    std::cout << "Char " << c << " lower: " << lower << " upper: " << upper << " char count: " << char_count
//              << " s: " << s << "\n";

    lower -= 1;
    upper -= 1;
    if(s[lower] == c and s[upper] != c){
      valid_count++;
    }
    if(s[upper] == c and s[lower] != c){
      valid_count++;
    }
  }
  std::cout << "valid_count: " << valid_count << "\n";
}

int main() {
  auto data_str = read_from_file("d2");
  // Comment out for running on real data
//  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
