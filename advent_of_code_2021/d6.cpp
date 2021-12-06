#include <fstream>
#include <iostream>
#include <vector>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d6.h"
#include <map>
#include <sstream>

std::string tmp_data =
        "3,4,3,1,2";


std::map<int, size_t> fish_map;

std::vector<int> fishAfterDays(int starting_timer, int num_days){
    std::vector<int> timers{starting_timer};
    for(int i=0; i<num_days; i++){
        int n = timers.size();
        for(int j=0; j<n; j++){
            timers[j]--;
            if(timers[j] <0){
                timers[j] = 6;
                timers.push_back(8);
            }
        }
    }
    return timers;
}

void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

    for(int i=0; i<9; i++){
        fish_map[i] = fishAfterDays(i, 80).size();
    }

    std::string s;
    std::stringstream ss(data[0]);
    size_t sum = 0;
    while(getline(ss, s, ',')){
//        std::cout << stoi(s) << "\n";
        sum+= fish_map[stoi(s)];
    }
    std::cout << sum << "\n";

}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::map<int, size_t> map128, map256;
    for(int i=0; i<9; i++){
        std::cout << "Computing fish for " << i << " timer\n";
        map128[i] = fishAfterDays(i, 128).size();
    }

    for(int i=0; i<9; i++){
        map256[i] = 0;
        for(const int c: fishAfterDays(i, 128)){
            map256[i] += map128[c];
        }
    }

    std::string s;
    std::stringstream ss(data[0]);
    size_t sum = 0;
    while(getline(ss, s, ',')){
//        std::cout << stoi(s) << "\n";
        sum+= map256[stoi(s)];
    }
    std::cout << sum << "\n";
}

int main() {
//    auto data_str = read_from_file("d1");
    // Comment out for running on real data
//    data_str = tmp_data;
    auto data = split(data_str, "\n");

    part_1(data);
    part_2(data);

    return 0;
}
