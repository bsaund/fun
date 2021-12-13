#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <unordered_set>
#include <sstream>
#include <algorithm>
#include <deque>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d12.h"

std::string tmp_data =
        "dc-end\n"
        "HN-start\n"
        "start-kj\n"
        "dc-start\n"
        "dc-HN\n"
        "LN-dc\n"
        "HN-end\n"
        "kj-sa\n"
        "kj-HN\n"
        "kj-dc";



void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

//    std::stringstream ss(data[0]);
//    std::string str;
//    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
//    }
//    std::cout << "\n";
    std::map<std::string, std::vector<std::string>> succ;

    for (const auto& line : data) {
        std::string s1, s2;
        std::stringstream ss(line);
        getline(ss, s1, '-');
        getline(ss, s2);
//        std::cout << s1 << ", " << s2 <<"\n";

        succ[s1].push_back(s2);
        succ[s2].push_back(s1);
    }

    std::deque<std::vector<std::string>> q;
    std::vector<std::vector<std::string>> found_paths;

    q.push_back({"start"});

    while(!q.empty()){
        auto path = q.front();
        q.pop_front();
        for(const auto &next: succ[path.back()]){
            if(next == "end"){
                auto new_path = path;
                new_path.push_back(next);
                found_paths.push_back(new_path);
                continue;
            }
            bool repeat = false;
            if(!std::all_of(next.begin(), next.end(), [](unsigned char c){return std::isupper(c);})){
                for(auto node: path){
                    if(node == next){
                        repeat = true;
                        break;
                    }
                }
            }
            if(repeat){
                continue;
            }
            auto new_path = path;
            new_path.push_back(next);
            q.push_back(new_path);
        }
    }

    for(auto p: found_paths){
        for(auto node: p){
            std::cout << node << ", ";
        }
        std::cout << "\n";
    }
    std::cout << found_paths.size();

}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::map<std::string, std::vector<std::string>> succ;

    for (const auto& line : data) {
        std::string s1, s2;
        std::stringstream ss(line);
        getline(ss, s1, '-');
        getline(ss, s2);
//        std::cout << s1 << ", " << s2 <<"\n";

        succ[s1].push_back(s2);
        succ[s2].push_back(s1);
    }

    std::deque<std::vector<std::string>> q;
    std::vector<std::vector<std::string>> found_paths;

    q.push_back({"0", "start"});

    while(!q.empty()){
        auto path = q.front();
        q.pop_front();
        for(const auto &next: succ[path.back()]){
            if(next == "end"){
                auto new_path = path;
                new_path.push_back(next);
                found_paths.push_back(new_path);
                continue;
            }
            if(next == "start"){
                continue;
            }
            bool repeat = false;
            if(!std::all_of(next.begin(), next.end(), [](unsigned char c){return std::isupper(c);})){
                int cnt = 0;
                int limit = path[0] == "0" ? 2: 1;
                for(auto node: path){
                    if(node == next){
                        cnt ++;
                        if(cnt == limit) {
                            repeat = true;
                            break;
                        }
                    }
                }
            }
            if(repeat){
                continue;
            }

            auto new_path = path;
            if(!std::all_of(next.begin(), next.end(), [](unsigned char c){return std::isupper(c);})) {
                for (auto node : new_path) {
                    if (node == next) {
                        new_path[0] = "1";
                        break;
                    }
                }
            }
            new_path.push_back(next);
            q.push_back(new_path);
        }
    }

    for(auto p: found_paths){
        for(auto node: p){
            std::cout << node << ", ";
        }
        std::cout << "\n";
    }
    std::cout << found_paths.size();
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
