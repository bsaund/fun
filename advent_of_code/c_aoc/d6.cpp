#include <fstream>
#include <iostream>
#include <vector>
#include <set>

#include "include/file_parsing.h"
#include "include/printing.h"
#include "absl/strings/match.h"
#include "include/container_conversions.h"

std::string tmp_data = "abc\n"
    "\n"
    "a\n"
    "b\n"
    "c\n"
    "\n"
    "ab\n"
    "ac\n"
    "\n"
    "a\n"
    "a\n"
    "a\n"
    "a\n"
    "\n"
    "b";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1
  int s = 0;
  for (const auto& line : data) {
    std::set<char> questions;
    for (const char& c: line){
      if (absl::StrContains(" \n", c)){
        continue;
      }
      questions.insert(c);
    }
//    std::cout << questions.size() << "\n";
    s += questions.size();
  }
  std::cout << s << "\n";
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2

  int s = 0;
  for(const auto& group : data){
    std::set<char> all_answered;
    int i=0;
    for(const auto& single_person_answer: split(group, "\n")){
      if(i == 0){
        all_answered = toSet(single_person_answer);
      }
      all_answered = set_intersect(all_answered, toSet(single_person_answer));
      i++;
      std::cout << "single answers: " << single_person_answer << "\n";
    }
    std::cout << "All answered: " << all_answered.size() << "\n";
    std::cout << "\n";
    s += all_answered.size();
  }
  std::cout << s << "\n";
}

int main() {
  auto data_str = read_from_file("d6");
  // Comment out for running on real data
//  data_str = tmp_data;
  auto data = split(data_str, "\n\n");

  part_1(data);
  part_2(data);

  return 0;
}
