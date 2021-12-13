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
#include "data/d11.h"

std::string tmp_data =
        "5483143223\n"
        "2745854711\n"
        "5264556173\n"
        "6141336146\n"
        "6357385478\n"
        "4167524645\n"
        "2176841721\n"
        "6882881134\n"
        "4846848554\n"
        "5283751526";

bool isvalid(const Point& p, const std::vector<std::vector<int>> &d){
    return p.x >= 0 && p.y >= 0 && p.x < d.size() && p.y < d[0].size();
}

void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

//    std::stringstream ss(data[0]);
//    std::string str;
//    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
//    }
//    std::cout << "\n";

    std::vector<std::vector<int>> oct;

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
//        std::cout << line << "\n";
        std::vector<int> l;
        for(const char &c: line){
            l.push_back((int)c - '0');
        }
        oct.push_back(l);
    }


    int num_flashes = 0;
    for(int step=0; step<100; step++){
        std::cout << "After step " << step << ";\n";
        for(auto l: oct){
            for(int o: l){
                std::cout << o;
            }
            std::cout << "\n";
        }

        for(const auto p: itercoords(oct)){
            oct[p.x][p.y] ++;
        }
        std::unordered_set<Point> has_flashed;
        bool new_flash = true;
        while(new_flash){
            new_flash = false;
            for(const auto p:itercoords(oct)){
                if(oct[p.x][p.y] <= 9){
                    continue;
                }
                if(has_flashed.count(p)){
                    continue;
                }
                new_flash = true;
                has_flashed.emplace(p.x, p.y);

                for(int i=-1; i<=1; i++){
                    for(int j=-1; j<=1; j++){
                        Point adj(p.x + i, p.y+j);
                        if(!isvalid(adj, oct)){
                            continue;
                        }
                        oct[adj.x][adj.y] ++;
                    }
                }
            }
        }
        num_flashes += has_flashed.size();
        for(const Point &p: has_flashed){
            oct[p.x][p.y] = 0;
        }
    }
    std::cout << num_flashes;
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::vector<std::vector<int>> oct;

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
//        std::cout << line << "\n";
        std::vector<int> l;
        for(const char &c: line){
            l.push_back((int)c - '0');
        }
        oct.push_back(l);
    }


    int num_flashes = 0;
    for(int step=0; step<10000; step++){
//        std::cout << "After step " << step << ";\n";
//        for(auto l: oct){
//            for(int o: l){
//                std::cout << o;
//            }
//            std::cout << "\n";
//        }

        for(const auto p: itercoords(oct)){
            oct[p.x][p.y] ++;
        }
        std::unordered_set<Point> has_flashed;
        bool new_flash = true;
        while(new_flash){
            new_flash = false;
            for(const auto p:itercoords(oct)){
                if(oct[p.x][p.y] <= 9){
                    continue;
                }
                if(has_flashed.count(p)){
                    continue;
                }
                new_flash = true;
                has_flashed.emplace(p.x, p.y);

                for(int i=-1; i<=1; i++){
                    for(int j=-1; j<=1; j++){
                        Point adj(p.x + i, p.y+j);
                        if(!isvalid(adj, oct)){
                            continue;
                        }
                        oct[adj.x][adj.y] ++;
                    }
                }
            }
        }
        num_flashes += has_flashed.size();
        for(const Point &p: has_flashed){
            oct[p.x][p.y] = 0;
        }
        if(has_flashed.size() == oct.size() * oct[0].size()){
            std::cout << "Flashed simultaneously on step " << step + 1 << "\n";
            return;
        }
    }
    std::cout << num_flashes;
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
