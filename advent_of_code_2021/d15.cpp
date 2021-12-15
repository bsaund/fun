#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <unordered_set>
#include <sstream>
#include <algorithm>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d15.h"

std::string tmp_data =
        "1721\n"
        "979\n"
        "366\n"
        "299\n"
        "675\n"
        "1456";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

//    std::stringstream ss(data[0]);
//    std::string str;
//    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
//    }
//    std::cout << "\n";

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
        std::cout << line << "\n";
    }
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::cout << "Part 2 has " << data.size() << " entries\n";
}

int main() {
//    auto data_str = read_from_file("d1");
    // Comment out for running on real data
    data_str = tmp_data;
    auto data = split(data_str, "\n");

    part_1(data);
    part_2(data);

    return 0;
}
