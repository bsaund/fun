#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <unordered_set>
#include <sstream>
#include <algorithm>
#include <list>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d15.h"

std::string tmp_data =
        "1163751742\n"
        "1381373672\n"
        "2136511328\n"
        "3694931569\n"
        "7463417111\n"
        "1319128137\n"
        "1359912421\n"
        "3125421639\n"
        "1293138521\n"
        "2311944581";


int heur(const Point &p, const std::vector<std::vector<int>> &data){
    return (data.size() - p.x + data[0].size() + p.y)*9;
}

bool isValid(const Point &p, const std::vector<std::vector<int>> &data){
    return p.x >= 0 && p.y >= 0 && p.x < data.size() && p.y < data.size();
}

void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1
    std::vector<std::vector<int>> grid;

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
//        std::cout << line << "\n";
        std::vector<int> v;
        for(auto c: line){
            v.push_back(int(c - '0'));
        }
        grid.push_back(v);
    }

    for(auto v: grid){
        for(auto c: v){
            std::cout << c;
        }
        std::cout << "\n";
    }

    std::unordered_map<Point, int> g;
    std::unordered_map<Point, Point> came_from;

    std::list<Point> open;
    open.push_back(Point(0,0));

    while(!open.empty()){
        auto best = open.front();
        int best_val = 9999999;
        for(auto p: open){
            int est = g[p] + heur(p, grid);
            if(est < best_val){
                best_val = est;
                best = p;
            }
        }
        open.remove(best);

        for(int i=-1; i<=1; i++){
            for(int j=-1; j<=1; j++){
                if(std::abs(i) + std::abs(j) > 1){
                    continue;
                }
                Point n(best.x+i, best.y+j);

                if(!isValid(n, grid)){
                    continue;
                }
//                std::cout << "it is valid\n";
                int c_tmp = g[best] + grid[n.x][n.y];
                if(g.count(n) && g[n] < c_tmp){
                    continue;
                }
//                std::cout << "Expanding " << n.x << ", " << n.y << " with cost " << c_tmp << "\n";
                g[n] = c_tmp;
                came_from.emplace(n, best);
                if(n.x == grid.size()-1 && n.y == grid[0].size()-1){
                    break;
                }
                open.push_back(n);

            }
        }

    }
    std::cout << "\n\n" << g[Point(grid.size()-1, grid[0].size()-1)];
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::vector<std::vector<int>> grid;

    for (const auto& line : data) {
        sscanf(line.c_str(), "");
//        std::cout << line << "\n";
        std::vector<int> v;
        for(auto c: line){
            v.push_back(int(c - '0'));
        }
        grid.push_back(v);
    }

//    for(auto v: grid){
//        for(auto c: v){
//            std::cout << c;
//        }
//        std::cout << "\n";
//    }
    std::vector<std::vector<int>> grid_tmp;

    for(auto row: grid) {
        std::vector<int> a;
        for (int i = 0; i < 5; i++) {
            for (auto elem : row) {
                a.push_back((elem + i -1)%9 +1);
            }
        }
        grid_tmp.push_back(a);
    }
    grid = grid_tmp;
    grid_tmp.clear();




    for(auto i=0; i<5; i++){
        for(auto row: grid){
            std::vector<int> new_row;
            for(auto elem: row){
                new_row.push_back((elem + i - 1) %9 +1);
            }
            grid_tmp.push_back(new_row);
        }

    }
    grid = grid_tmp;

    for(auto row:grid){
        for(auto elem: row){
//            std::cout << elem;
        }
//        std::cout << "\n";
    }

    std::unordered_map<Point, int> g;
    std::unordered_map<Point, Point> came_from;

    std::list<Point> open;
    open.push_back(Point(0,0));
    std::unordered_set<Point> closed;


    while(!open.empty()){
        auto best = open.front();
        int best_val = 9999999;
        for(auto p: open){
            int est = g[p];
            if(est < best_val){
                best_val = est;
                best = p;
            }
        }
        open.remove(best);
        closed.emplace(best);

        for(int i=-1; i<=1; i++){
            for(int j=-1; j<=1; j++){
                if(std::abs(i) + std::abs(j) > 1){
                    continue;
                }
                Point n(best.x+i, best.y+j);

                if(!isValid(n, grid)){
                    continue;
                }
                if(closed.count(n)){
                    continue;
                }

//                std::cout << "it is valid\n";
                int c_tmp = g[best] + grid[n.x][n.y];
                if(g.count(n) && g[n] <= c_tmp){
                    continue;
                }
                if(closed.count(n)){
//                    continue;
                    std::cout << "Rexpanding " << n.x << ", " << n.y << ". old val: " << g[n] << ". new val: " << c_tmp << "\n";
                }
                std::cout << "Expanding " << n.x << ", " << n.y << " with cost " << c_tmp << "\n";
                g[n] = c_tmp;
                came_from.emplace(n, best);
                if(n.x == grid.size()-1 && n.y == grid[0].size()-1){
                    break;
                }

                open.push_back(n);

            }
        }

    }
    std::cout << "\n\n" << g[Point(grid.size()-1, grid[0].size()-1)];
}

int main() {
//    auto data_str = read_from_file("d1");
    // Comment out for running on real data
//    data_str = tmp_data;
    auto data = split(data_str, "\n");

//    part_1(data);
    part_2(data);

    return 0;
}
