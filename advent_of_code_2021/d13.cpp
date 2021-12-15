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
#include "data/d13.h"

std::string tmp_data =
        "6,10\n"
        "0,14\n"
        "9,10\n"
        "0,3\n"
        "10,4\n"
        "4,11\n"
        "6,0\n"
        "6,12\n"
        "4,1\n"
        "0,13\n"
        "10,12\n"
        "3,4\n"
        "3,0\n"
        "8,4\n"
        "1,10\n"
        "2,14\n"
        "8,10\n"
        "9,0\n"
        "\n"
        "fold along y=7\n"
        "fold along x=5";

void print(std::unordered_set<Point> dots){
    int ar[7][200] {0};
    std::cout << "\n\n";
    for(const auto d: dots){
//        std::cout <<
        ar[d.x][d.y] = 1;
    }
    for(auto & i : ar){
        for(int j : i){
            std::cout << (j ? '@' : ' ');
        }
        std::cout << "\n";
    }
    std::cout << "\n\n";
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

    std::unordered_set<Point> dots;
    std::vector<int> x_folds;
    std::vector<int> y_folds;
    for (const auto& line : data) {
        if(line[0] != 'f'){
            int i, j;
            sscanf(line.c_str(), "%d,%d", &i, &j);
            dots.emplace(j, i);
        } else{
            char v;
            int i;
            sscanf(line.c_str(), "fold along %c=%d", &v, &i);
            if(v=='x'){
                x_folds.push_back(i);
            } else{
                y_folds.push_back(i);
            }
        }

    }

    for(auto d: dots){
        std::cout << d.x << ", " << d.y << "\n";
    }
    for(int i: x_folds){
        std::cout << "x_fold: " << i << "\n";
    }
    for(int i: y_folds){
        std::cout << "y_fold: " << i << "\n";
    }

//    print(dots);

    std::unordered_set<Point> new_dots;



    //y_fold
//    int y_fold = y_folds[0];
//    std::cout << "Folding y along " << y_fold << "\n";
//
//    for(auto d: dots){
//        if(d.x <= y_fold){
//            new_dots.insert(d);
//            continue;
//        }
//        new_dots.emplace(2*y_fold - d.x, d.y);
//    }
//
//    dots = new_dots;
//    new_dots.clear();
//    print(dots);


    //x_fold
    int x_fold = x_folds[0];
    std::cout << "Folding x along " << x_fold << "\n";
    for(auto d: dots){
        if(d.y <= x_fold){
            new_dots.insert(d);
            continue;
        }
        new_dots.emplace(d.x, 2*x_fold-d.y);

    }
    dots = new_dots;

//    print(dots);
    std::cout << dots.size();



}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::unordered_set<Point> dots;
    std::vector<int> x_folds;
    std::vector<int> y_folds;
    for (const auto& line : data) {
        if(line[0] != 'f'){
            int i, j;
            sscanf(line.c_str(), "%d,%d", &i, &j);
            dots.emplace(j, i);
        } else{
            char v;
            int i;
            sscanf(line.c_str(), "fold along %c=%d", &v, &i);
            if(v=='x'){
                x_folds.push_back(i);
            } else{
                y_folds.push_back(i);
            }
        }

    }

    for(auto d: dots){
        std::cout << d.x << ", " << d.y << "\n";
    }
    for(int i: x_folds){
        std::cout << "x_fold: " << i << "\n";
    }
    for(int i: y_folds){
        std::cout << "y_fold: " << i << "\n";
    }

//    print(dots);

    std::unordered_set<Point> new_dots;



    //y_fold
    for(int y_fold: y_folds) {
        std::cout << "Folding y along " << y_fold << "\n";

        for (auto d : dots) {
            if (d.x <= y_fold) {
                new_dots.insert(d);
                continue;
            }
            new_dots.emplace(2 * y_fold - d.x, d.y);
        }

        dots = new_dots;
        new_dots.clear();
    }
//    print(dots);


    //x_fold
    for(int x_fold: x_folds) {
        std::cout << "Folding x along " << x_fold << "\n";
        for (auto d : dots) {
            if (d.y <= x_fold) {
                new_dots.insert(d);
                continue;
            }
            new_dots.emplace(d.x, 2 * x_fold - d.y);
        }
        dots = new_dots;
        new_dots.clear();
    }

    print(dots);
    std::cout << dots.size();
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
