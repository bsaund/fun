#include <fstream>
#include <iostream>
#include <vector>
#include <sstream>
#include <set>
#include <map>
#include <algorithm>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d8.h"

//std::string tmp_data =
//        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\n"
//        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\n"
//        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\n"
//        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\n"
//        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\n"
//        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\n"
//        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\n"
//        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\n"
//        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\n"
//        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce";

std::string tmp_data = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1


    std::string str;

    std::set<int> accepted_sizes{2, 3, 4, 7};
    int cnt = 0;
    for(auto line: data) {
        std::stringstream ss(line);
        bool start = false;
        while (getline(ss, str, ' ')) {
            if (str == "|") {
                start = true;
                continue;
            }
            if (!start) {
                continue;
            }
            std::cout << str << ", ";
            if (accepted_sizes.count(str.size())) {
                cnt++;
            }
        }
    }
    std::cout << "\n";
    std::cout << cnt << "\n";


}

int countAinB(const std::string &a_, const std::string &b_){
    std::set<char> a(a_.begin(), a_.end());
    std::set<char> b(b_.begin(), b_.end());
    int cnt = 0;
    for(auto c: a){
        cnt += b.count(c);
    }
    return cnt;
}

std::map<std::string, int> deduceDigits(const std::set<std::string> &nums){
    std::map<std::string, int> m;
    std::map<int, std::string> rev;
    for(auto n: nums){
        if(n.size() == 2){
            m[n] = 1;
            continue;
        }
        if(n.size() == 3){
            m[n] = 7;
            continue;
        }
        if(n.size() == 4){
            m[n] = 4;
            continue;
        }
        if(n.size() == 7){
            m[n] = 8;
            continue;;
        }
    }
    for(auto it: m){
        rev[it.second] = it.first;
        std::cout << it.first << " is " << it.second << "\n";
    }

    //find 3
    for(auto n: nums){
        if(m.count(n) or n.size() != 5){
            continue;
        }
        std::set<char> one(rev[1].begin(), rev[1].end());
        std::set<char> unknown(n.begin(), n.end());
        if(std::includes(unknown.begin(), unknown.end(), one.begin(), one.end())){
            std::cout << "1 is: " << rev[1] << " so " << n << " is 3\n";
            m[n] = 3;
            rev[3] = n;
        }
//        std::cout << n << ", ";
    }

    //find 9
    for(auto n: nums){
        if(m.count(n) or n.size() != 6){
            continue;
        }
        if(countAinB(rev[3], n) == 5){
            std::cout << "3 is: " << rev[3] << " so " << n << " is 9\n";
            m[n] = 9;
            rev[9] = n;
        }
    }

    //find 0 and 6
    for(auto n: nums){
        if(m.count(n) or n.size() != 6){
            continue;
        }
        if(countAinB(rev[7], n) == 3){
            m[n] = 0;
            rev[0] = n;
            std::cout <<n << " is 0\n";
        } else{
            m[n] = 6;
            rev[6] = n;
            std::cout <<n << " is 6\n";
        }

    }

    //find 2 and 5
    for(auto n: nums){
        if(m.count(n)){
            continue;
        }
        if(countAinB(rev[6], n) == 5){
            m[n] = 5;
            rev[5] = n;
            std::cout <<n << " is 5\n";
        } else{
            m[n] = 2;
            rev[2] = n;
            std::cout <<n << " is 2\n";
        }

    }
    std::cout << "\n";
    return m;
}


void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::string str;

    long cnt = 0;
    for(auto line: data) {
        std::stringstream ss(line);
        std::set<std::string> all_nums;
        bool start = false;
        std::map<std::string, int> str_to_digit;
        int place = 1000;
        while (getline(ss, str, ' ')) {
            if (str == "|") {
                start = true;
                str_to_digit = deduceDigits(all_nums);
                continue;
            }
            if (!start) {
                all_nums.insert(str);
                continue;
            }
            int digit;
            for(auto it: str_to_digit){
                if(str.size() == it.first.size() and countAinB(it.first, str) == str.size()){
                    digit = it.second;
                    break;
                }
            }

            std::cout << " Looking up " << str << " as " << digit << "\n";
            cnt += place * digit;
            place /= 10;
        }
    }
    std::cout << "\n";
    std::cout << cnt << "\n";
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
