#include <fstream>
#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cmath>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d7.h"

std::string tmp_data =
        "16,1,2,0,4,2,7,1,2,14";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

    std::stringstream ss(data[0]);
    std::string str;
    std::vector<int> nums;
    int sum = 0;
    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
        nums.push_back(stoi(str));
        sum += stoi(str);
    }

    std::sort(nums.begin(), nums.end());

    int med = nums[nums.size()/2];
    int cost = 0;
    for(auto num: nums){
        cost += std::abs(med - num);
    }
    std::cout << cost << "\n";


    std::cout << "\n";


}

int costFor(const std::vector<int> &nums, int target){
    int cost = 0;
    for(auto num: nums){
        int dist = std::abs(target - num);
        cost += (dist * dist + dist)/2;
    }
    return cost;
}


void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::stringstream ss(data[0]);
    std::string str;
    std::vector<int> nums;
    int sum = 0;
    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
        nums.push_back(stoi(str));
        sum += stoi(str);
    }

    std::sort(nums.begin(), nums.end());

//    int med = nums[nums.size()/2];
//    int med = std::round((double)sum / nums.size());
//    std::cout << med << "\n";
//    long cost = 0;
//    for(auto num: nums){
//        int dist = std::abs(med - num);
//        cost += (dist*dist + dist)/2;
//    }
//    std::cout << cost << "\n";

    int cur_cost = 1000000000;
    int target = 0;
    while(cur_cost > costFor(nums, target)){
        cur_cost = costFor(nums, target);
        target++;
        std::cout << cur_cost << "\n";
    }


    std::cout << "\n";
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
