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
#include "data/d14.h"

std::string tmp_data =
        "NNCB\n"
        "\n"
        "CH -> B\n"
        "HH -> N\n"
        "CB -> H\n"
        "NH -> C\n"
        "HB -> C\n"
        "HC -> B\n"
        "HN -> C\n"
        "NN -> C\n"
        "BH -> H\n"
        "NC -> B\n"
        "NB -> B\n"
        "BN -> B\n"
        "BB -> N\n"
        "BC -> B\n"
        "CC -> N\n"
        "CN -> C";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

//    std::stringstream ss(data[0]);
//    std::string str;
//    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
//    }
//    std::cout << "\n";
    std::list<char> polymer;
    std::list<char> polymer_tmp;
    std::map<std::pair<char, char>, char> progression;

    for(auto c: data[0]){
        polymer.push_back(c);
    }


    for (int i=1; i<data.size(); i++) {
        auto line = data[i];
        char a, b, c;
        sscanf(line.c_str(), "%c%c -> %c", &a, &b, &c);
//        std::cout << line << "\n";
        progression[{a,b}] = c;
    }

    for(int step=0; step<10; step++){
        for(auto it = polymer.begin(); std::next(it) != polymer.end(); it++){
            char a = *it;
            char b = *std::next(it);
//            std::cout << a << ", " << b << "\n";
            char c = progression[{a, b}];
            polymer_tmp.push_back(a);
            polymer_tmp.push_back(c);
            std::cout << "(" << a << ", " << b << ") -> " << c << "\n";
        }
        polymer_tmp.push_back(polymer.back());
        polymer = polymer_tmp;
        polymer_tmp.clear();
        for(auto c: polymer){
            std::cout << c;
        }
        std::cout << "\n";
    }

    std::map<char, long> cnt;
    for(auto c: polymer){
        cnt[c]++;
    }
    std::vector<long> cnts;
    for(auto it:cnt){
        cnts.push_back(it.second);
    }
    std::sort(cnts.begin(), cnts.end());
    std::cout << cnts.back() - cnts.front();
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::map<std::pair<char, char>, long> pair_count;
    std::map<std::pair<char, char>, char> progression;

    for(int i=0; i<data[0].size()-1; i++){
        pair_count[{data[0][i], data[0][i+1]}]++;
    }


    for (int i=1; i<data.size(); i++) {
        auto line = data[i];
        char a, b, c;
        sscanf(line.c_str(), "%c%c -> %c", &a, &b, &c);
//        std::cout << line << "\n";
        progression[{a,b}] = c;
    }



    for(int step=0; step<40; step++){
        std::map<std::pair<char, char>, long> pair_tmp;
        for(auto it: pair_count){
            char a = it.first.first;
            char b = it.first.second;
//            std::cout << a << ", " << b << "\n";
            char c = progression[{a, b}];
            pair_tmp[{a, c}] += it.second;
            pair_tmp[{c, b}] += it.second;

//            std::cout << "(" << a << ", " << b << ") -> " << c << "\n";
        }
        pair_count = pair_tmp;
//        for(auto it: pair_count){
//            std::cout << "(" << it.first.first << ", " << it.first.second << "): " << it.second << "\n";
//        }
//        std::cout << "\n";
//        for(auto c: polymer){
//            std::cout << c;
//        }
//        std::cout << "\n";
    }

    std::map<char, long> letter_cnts;
    for(auto it:pair_count){
        letter_cnts[it.first.first] += it.second;
        letter_cnts[it.first.second] += it.second;
    }
    letter_cnts[data[0].front()] ++;
    letter_cnts[data[0].back()] ++;

    std::vector<long> cnts;
    for(auto it: letter_cnts){
        cnts.push_back(it.second/2);
    }
    std::sort(cnts.begin(), cnts.end());
    std::cout << cnts.back() - cnts.front();
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
