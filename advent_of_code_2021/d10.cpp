#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <sstream>
#include <algorithm>
#include <stack>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d10.h"

std::string tmp_data =
        "[({(<(())[]>[[{[]{<()<>>\n"
        "[(()[<>])]({[<{<<[]>>(\n"
        "{([(<{}[<>[]}>{[]{[(<()>\n"
        "(((({<>}<{<{<>}{[]{[]{}\n"
        "[[<[([]))<([[{}[[()]]]\n"
        "[{[{({}]{}}([{[{{{}}([]\n"
        "{<[[]]>}<{[{[{[]{()[[[]\n"
        "[<(<(<(<{}))><([]([]()\n"
        "<{([([[(<>()){}]>(<<{{\n"
        "<{([{{}}[<[[[<>{}]]]>[]]";


void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1

//    std::stringstream ss(data[0]);
//    std::string str;
//    while(getline(ss, str, ',')){
//        std::cout << stoi(str) << ", ";
//    }
//    std::cout << "\n";
//    int score = 0;
//    for (const auto& line : data) {
//        sscanf(line.c_str(), "");
//        int a=0, b=0, c=0, d=0;
//
//        for(const char &ch: line){
//            switch(ch){
//                case '(':
//                    a++; break;
//                case '[':
//                    b++; break;
//                case '{':
//                    c++; break;
//                case '<':
//                    d++; break;
//                case ')':
//                    a--; break;
//                case ']':
//                    b--; break;
//                case '}':
//                    c--; break;
//                case '>':
//                    d--; break;
//                default:
//                    std::cout << "UNEXPECTED CHARACTER\n";
//            }
//            if(a<0){
//                score += 2;
//                break;
//            }
//            if(b<0){
//                score += 57;
//                break;
//            }
//            if(c<0) {
//                score += 1197;
//                break;
//            }
//            if(d<0) {
//                score += 25137;
//                break;
//            }
//        }
//        std::cout << score << "\n";
//    }
    int score = 0;
    std::map<char, char> opener{{')','('}, {']', '['}, {'}', '{'}, {'>', '<'}};
    std::map<char, int> scores{{')', 3}, {']', 57}, {'}', 1197}, {'>', 25137}};
    for (const auto& line : data) {
        std::stack<char> cs;
        bool invalid = false;
        for (const char &ch : line) {
            switch(ch){
                case '(':
                case '[':
                case '{':
                case '<':
                    cs.push(ch);
                    break;
                default:
                    if(cs.top() == opener[ch]){
                        cs.pop();
                        break;
                    }
                    std::cout << "Expected " << cs.top() << " but found " << opener[ch] << "\n";
                    score += scores[ch];
                    invalid = true;
                    break;
            }
            if(invalid){
                break;
            }
        }

    }
    std::cout << score << "\n";
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::vector<long> scores;
    std::map<char, char> opener{{')','('}, {']', '['}, {'}', '{'}, {'>', '<'}};
    std::map<char, int> score_map{{'(', 1}, {'[', 2}, {'{', 3}, {'<', 4}};
    for (const auto& line : data) {
        std::stack<char> cs;
        bool invalid = false;
        for (const char &ch : line) {
            switch(ch){
                case '(':
                case '[':
                case '{':
                case '<':
                    cs.push(ch);
                    break;
                default:
                    if(cs.top() == opener[ch]){
                        cs.pop();
                        break;
                    }
//                    std::cout << "Expected " << cs.top() << " but found " << opener[ch] << "\n";
                    invalid = true;
                    break;
            }
            if(invalid){
                break;
            }
        }
        if(invalid){
            continue;
        }
        long score = 0;
        while(!cs.empty()){
            std::cout << cs.top();
            score *= 5;
            score += score_map[cs.top()];
            cs.pop();
        }
        std::cout << ": " << score << "\n";
        scores.push_back(score);
    }
    std::sort(scores.begin(), scores.end());
    std::cout << scores[scores.size()/2] << "\n";
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
