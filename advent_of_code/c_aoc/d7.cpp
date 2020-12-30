#include <fstream>
#include <iostream>
#include <map>
#include <vector>

#include "absl/strings/match.h"
#include "absl/strings/str_join.h"
#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"

std::string tmp_data =
    "light red bags contain 1 bright white bag, 2 muted yellow bags.\n"
    "dark orange bags contain 3 bright white bags, 4 muted yellow bags.\n"
    "bright white bags contain 1 shiny gold bag.\n"
    "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.\n"
    "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.\n"
    "dark olive bags contain 3 faded blue bags, 4 dotted black bags.\n"
    "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.\n"
    "faded blue bags contain no other bags.\n"
    "dotted black bags contain no other bags.";

// std::string read_from_file(const std::string &day) {
//    std::ifstream f(day + ".txt");
//    return std::string(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
//}
std::string remove_last_word(const std::string& str){
  auto v = split(str, " ");
  std::vector<std::string> v2(v.begin(), v.end() - 1);
  return absl::StrJoin(v2, " ");
}

std::set<std::pair<int, std::string> > parse_contained_bags(const std::string& str){
  std::set<std::pair<int, std::string> > bags;
  for(const auto& b: split(str, ", ")){
    auto parts = split(b, " ");
//    std::cout << "b: " << b << ":  ";
    std::string bag_name = absl::StrJoin(std::vector<std::string>(parts.begin()+1, parts.begin()+3), " ");
    int bag_count = atoi(parts[0].c_str());
//    std::cout << bag_count << " - " << bag_name << "\n";
    if(bag_count != 0) {
      bags.insert({bag_count, bag_name});
    }
  }
  return bags;
}

std::map<std::string, std::set<std::pair<int, std::string>>> parse_bag_map(const std::vector<std::string>& data){
  std::map<std::string, std::set<std::pair<int, std::string>>> bag_contents;
  for (const auto& line : data) {
//    std::cout << line << "\n";
    auto a = split(line, " contain ");
    check(a.size() == 2, "Splitting by `contain` should split into 2");
//    std::cout << a[0] << ": ";
//    std::cout << remove_last_word(a[1]) << "\n";
    bag_contents[remove_last_word(a[0])] = parse_contained_bags(a[1]);
  }
  return bag_contents;
}


void part_1(const std::vector<std::string>& data) {
  std::cout << "--------- PART 1 -----------\n";
  // Part 1
  auto bag_contents = parse_bag_map(data);
  std::set<std::string> outer_bags{"shiny gold"};
  int prev_length = 0;
  while(prev_length != outer_bags.size()){
    prev_length = outer_bags.size();
    for(const auto& [outer, inners]: bag_contents){
      bool contains_outer_bag = false;
      for(const auto& bag: outer_bags){
        for(const auto& [cnt, contained_bag]: inners){
          if(contained_bag == bag){
            contains_outer_bag = true;
            break;
          }
        }
        if(contains_outer_bag){
          break;
        }
      }
      if(contains_outer_bag){
        outer_bags.insert(outer);
      }
    }
  }
  std::cout << "Total possible outer bags: " << outer_bags.size() - 1 << "\n";

}

int count_total_bags(const std::map<std::string, std::set<std::pair<int, std::string>>>& rules, const std::string& bag){
  if(rules.at(bag).size() == 0){
    return 1;
  }
  int count = 1;
  for(const auto& [cnt, contained_bag]: rules.at(bag)){
    count += cnt * count_total_bags(rules, contained_bag);
  }
  return count;
}

void part_2(const std::vector<std::string>& data) {
  std::cout << "\n\n\n--------- PART 2 -----------\n";
  // Part 2
  auto bag_contents = parse_bag_map(data);
  std::cout << "Total contained bags: " << count_total_bags(bag_contents, "shiny gold") - 1 << "\n";
}

int main() {
  auto data_str = read_from_file("d7");
  // Comment out for running on real data
//  data_str = tmp_data;
  auto data = split(data_str, "\n");

  part_1(data);
  part_2(data);

  return 0;
}
