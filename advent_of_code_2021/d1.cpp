#include <fstream>
#include <iostream>
#include <vector>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d1.h"

std::string tmp_data =
        "199\n"
        "200\n"
        "208\n"
        "210\n"
        "200\n"
        "207\n"
        "240\n"
        "269\n"
        "260\n"
        "263";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1
    int prev = 0;
    int cur;
    int cnt = -1;
    for (const auto& line : data) {
        sscanf(line.c_str(), "%d", &cur);
//        std::cout << cur << "\n";
        cnt += cur > prev;
        prev = cur;
    }
    std::cout << cnt;
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
//    std::cout << "Part 2 has " << data.size() << " entries\n";
    int cnt = 0;
    for(size_t i=0; i<data.size()-3; i++) {
        auto w1 = stoi(data[i]) + stoi(data[i+1]) + stoi(data[i+2]);
        auto w2 = stoi(data[i+1]) + stoi(data[i+2]) + stoi(data[i+3]);
        cnt += w2 > w1;
        std::cout << w2 << "  ";
        if(w2 > w1) {
            std::cout << "increased\n";
        } else {
            std::cout << "not\n";
        }
    }
    std::cout << cnt;
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
