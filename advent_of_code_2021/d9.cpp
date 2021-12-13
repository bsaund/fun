#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <unordered_set>
#include <sstream>
#include <algorithm>
#include <queue>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d9.h"

std::string tmp_data =
        "2199943210\n"
        "3987894921\n"
        "9856789892\n"
        "8767896789\n"
        "9899965678";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

//    std::stringstream ss(data[0]);
//    std::string str;
//    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
//    }
//    std::cout << "\n";
    std::vector<std::vector<int>> nums;

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
        std::vector<int> row;
        for(const char &c: line){
//            std::cout << c << " ";
            row.push_back(c - '0');
        }
        nums.push_back(row);
//        std::cout << "\n";
    }

    int risk = 0;
    for(int i=0; i<nums.size(); i++){
        for(int j=0; j<nums[0].size(); j++){
//            bool is_low = true;
            int num= nums[i][j];
            if(i>0 && nums[i-1][j] <= num){
                continue;
            }
            if(i<nums.size()-1 && nums[i+1][j] <= num){
                continue;
            }
            if(j>0 && nums[i][j-1] <= num){
                continue;
            }
            if(j<nums[0].size()-1 && nums[i][j+1] <= num){
                continue;
            }
//            std::cout << nums[i][j];
            std::cout << num << "(" << i << ", " << j << ") is a low point\n";
            risk+= num + 1;
        }

    }
    std::cout << risk << "\n";
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
//    std::cout << "Part 2 has " << data.size() << " entries\n";
    std::vector<std::vector<int>> nums;

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
        std::vector<int> row;
        for(const char &c: line){
//            std::cout << c << " ";
            row.push_back(c - '0');
        }
        nums.push_back(row);
//        std::cout << "\n";
    }

    std::vector<Point> low_points;
    for(int i=0; i<nums.size(); i++){
        for(int j=0; j<nums[0].size(); j++){
//            bool is_low = true;
            int num= nums[i][j];
            if(i>0 && nums[i-1][j] <= num){
                continue;
            }
            if(i<nums.size()-1 && nums[i+1][j] <= num){
                continue;
            }
            if(j>0 && nums[i][j-1] <= num){
                continue;
            }
            if(j<nums[0].size()-1 && nums[i][j+1] <= num){
                continue;
            }
//            std::cout << nums[i][j];
            std::cout << num << "(" << i << ", " << j << ") is a low point\n";
            low_points.emplace_back(i,j);
        }
    }

    std::vector<int> basin_sizes;
    for(auto low_point: low_points){
        std::cout << "\nBasin: \n";
        std::unordered_set<Point> basin;
        std::queue<Point> q;
        q.push(low_point);

        while(!q.empty()){
            Point p = q.front();
            q.pop();
            if(nums[p.x][p.y] == 9){
                continue;
            }
            if(basin.count(p)){
                continue;
            }
            basin.insert(p);
            std::cout << nums[p.x][p.y] << ", ";
            if(p.x>0){
                q.push(Point(p.x-1, p.y));
            }
            if(p.x<nums.size()-1){
                q.push(Point(p.x+1, p.y));
            }
            if(p.y>0){
                q.push(Point(p.x, p.y-1));
            }
            if(p.y<nums[0].size()-1){
                q.push(Point(p.x, p.y+1));
            }

        }
        basin_sizes.push_back(basin.size());
    }
    std::sort(basin_sizes.begin(), basin_sizes.end());

    for(auto i: basin_sizes){
        std::cout << i << "\n";
    }
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
