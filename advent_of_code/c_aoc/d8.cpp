#include <fstream>
#include <iostream>
#include <vector>

#include "absl/strings/match.h"
#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"

std::string tmp_data =
    "nop +0\n"
    "acc +1\n"
    "jmp +4\n"
    "acc +3\n"
    "jmp -3\n"
    "acc -99\n"
    "acc +1\n"
    "jmp -4\n"
    "acc +6";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}

bool VERBOSE = false;

void pd(const std::string &s, int i){
  if(VERBOSE){
    std::cout << s << " " << i << "\n";
  }
}

std::pair<int, bool> run_boot_code(const std::vector<std::string>& data){
  int acc = 0;
  int line = 0;
  std::set<int> visited_lines{};

  while(!visited_lines.contains(line)){
    if(line == data.size()){
      return {acc, true};
    }
    if(line > data.size()){
      return {acc, false};
    }
    visited_lines.insert(line);
    std::string instruction(3, '\0');
    int val;
//    std::cout << data[line] << ": ";
    sscanf(data[line].c_str(), "%s %d", instruction.c_str(), &val);
    pd("line ", line);

    if(instruction == "jmp"){
      line += val;
      pd("jmp ", val);
      continue;
    }
    line += 1;
    if(instruction == "acc"){
      acc += val;
    }
  }
  return {acc, false};
}

void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1
  auto boot = run_boot_code(data);
  assert(!boot.second);

  std::cout << "Before repeating, the accumulator is " << boot.first << "\n";
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2
  for(int line = 0; line < data.size(); line++){
    std::vector<std::string> edited_boot_code(data);
    std::string instruction(3, '\0');
    sscanf(data[line].c_str(), "%s", instruction.c_str());
    std::string old_line = data[line];
    if(instruction == "jmp"){
      edited_boot_code[line].replace(0, 3, "nop");
    }
    else if(instruction == "nop"){
      edited_boot_code[line].replace(0, 3, "jmp");
    }
    else{
      continue;
    }
    auto boot = run_boot_code(edited_boot_code);
    if(boot.second){
      std::cout << "After editing line " << line << " the boot code ends with " << boot.first << "\n";
    }
  }
}

int main() {
  auto data_str = read_from_file("d8");
  // Comment out for running on real data
//  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
