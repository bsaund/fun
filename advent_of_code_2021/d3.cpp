#include <fstream>
#include <iostream>
#include <vector>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "data/d3.h"
#include "include/file_parsing.h"
#include "include/utils.h"

std::string tmp_data =
        "00100\n"
        "11110\n"
        "10110\n"
        "10111\n"
        "10101\n"
        "01111\n"
        "00111\n"
        "11100\n"
        "10000\n"
        "11001\n"
        "00010\n"
        "01010";


void part_1(const std::vector<std::string> &data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

    std::vector<int> cnts;
    for (const auto &line : data) {
        //        sscanf(line.c_str(), "%d", &i);
        if (cnts.size() == 0) {
            cnts.resize(line.size());
        }
        std::cout << line << "\n";
        for (int i = 0; i < line.size(); i++) {
            cnts[i] += (line[i] == '0');
        }
    }

    int gamma = 0;
    int eps = 0;
    int place = 1;
    for (int i = cnts.size() - 1; i >= 0; i--) {
        gamma += place * (cnts[i] < data.size() / 2);
        eps += place * (cnts[i] > data.size() / 2);
        place *= 2;
    }
    std::cout << gamma << ", " << eps << "\n";
    std::cout << gamma * eps << "\n";
}

char most_common_char(const std::vector<std::string> &data, int place){
    int cnt = 0;
    for(auto str: data){
        std::cout << str << ", ";
        cnt += (str[place] == '1');
    }
    std::cout << "\n";
    return (double)cnt >= ((double)data.size()/2) ? '1': '0';
}


void part_2(const std::vector<std::string> &data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2

    auto ox_numbers = data;
    for(int place=0; ;place++){
        if(ox_numbers.size() <= 1){
            break;
        }
        std::vector<std::string> new_ox_numbers;
        auto letter = most_common_char(ox_numbers, place);
        std::cout << "most common letter: " << letter << "\n";
        for(const auto &num: ox_numbers){
            if(num[place] == letter){
                new_ox_numbers.push_back(num);
            }
        }
        ox_numbers = new_ox_numbers;
    }

    auto co_numbers = data;
    for(int place=0; ;place++){
        if(co_numbers.size() <= 1){
            break;
        }
        std::vector<std::string> new_co_numbers;
        auto letter = most_common_char(co_numbers, place);
        std::cout << "most common letter: " << letter << "\n";
        for(const auto &num: co_numbers){
            if(num[place] != letter){
                new_co_numbers.push_back(num);
            }
        }
        co_numbers = new_co_numbers;
    }

    std::cout << ox_numbers[0] << "\n";
    std::cout << co_numbers[0] << "\n";

    int ox_num = 0;
    int co_num = 0;
    int place = 1;
    for(int i=ox_numbers[0].size()-1; i>=0; i--){
        ox_num += (ox_numbers[0][i]=='1') * place;
        co_num += (co_numbers[0][i]=='1') * place;
        place *= 2;
    }
    std::cout << ox_num << ", " << co_num << ", " << ox_num * co_num << "\n";
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
