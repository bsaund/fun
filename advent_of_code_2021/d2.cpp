#include <fstream>
#include <iostream>
#include <vector>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d2.h"

std::string tmp_data =
        "forward 5\n"
        "down 5\n"
        "forward 8\n"
        "up 3\n"
        "down 8\n"
        "forward 2";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1
    char* command;
    int value;

    int pos = 0;
    int depth = 0;
    for (const auto& line : data) {
        sscanf(line.c_str(), "%s %d", command, &value);
//        std::cout << command << "\n";
        if(std::string(command) == "forward") {
            pos += value;
        } else if(std::string(command) == "up"){
            depth -= value;
        } else if(std::string(command) == "down") {
            depth += value;
        } else {
            std::cout << "ERROR\n";
        }

    }
    std::cout << "depth: " << depth << " pos: " << pos << " product: " << pos * depth << "\n";
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    char* command;
    int value;

    int pos = 0;
    int depth = 0;
    int aim = 0;
    for (const auto& line : data) {
        sscanf(line.c_str(), "%s %d", command, &value);
//        std::cout << command << "\n";
        if(std::string(command) == "forward") {
            pos += value;
            depth += aim * value;
        } else if(std::string(command) == "up"){
            aim -= value;
        } else if(std::string(command) == "down") {
            aim += value;
        } else {
            std::cout << "ERROR\n";
        }

    }
    std::cout << "depth: " << depth << " pos: " << pos << " product: " << pos * depth << "\n";
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
