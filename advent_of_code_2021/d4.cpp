#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <set>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d4.h"

std::string tmp_data =
        "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n"
        "\n"
        "22 13 17 11  0\n"
        " 8  2 23  4 24\n"
        "21  9 14 16  7\n"
        " 6 10  3 18  5\n"
        " 1 12 20 15 19\n"
        "\n"
        " 3 15  0  2 22\n"
        " 9 18 13 17  5\n"
        "19  8  7 25 23\n"
        "20 11 10 24  4\n"
        "14 21 16 12  6\n"
        "\n"
        "14 21 17 24  4\n"
        "10 16 15  9 19\n"
        "18  8 23 26 20\n"
        "22 11 13  6  5\n"
        " 2  0 12  3  7";

class Board{
public:
    int board[5][5];

    explicit Board(const std::vector<std::string>& data){
        for(int i=0; i<5; i++){
            int a,b,c,d,e;
            sscanf(data[i].c_str(), "%d %d %d %d %d", &a, &b, &c, &d, &e);
            board[i][0] = a;
            board[i][1] = b;
            board[i][2] = c;
            board[i][3] = d;
            board[i][4] = e;
        }
    }

    bool hasWon(const std::set<int> &called) const{
        //check rows
        for(int i=0; i<5; i++){
            bool row_won = true;
            bool col_won = true;
            for(int j=0; j<5; j++){
                if(!called.count(board[i][j])) {
                    row_won = false;
                }
                if(!called.count(board[j][i])){
                    col_won = false;
                }
            }
            if(row_won or col_won){
                return true;
            }
        }
        return false;
    }
};

int score(const Board &board, const std::set<int> &called, int last_called){
    int unmarked = 0;
    for(int i=0; i<5; i++){
        for(int j=0; j<5; j++){
            if(!called.count(board.board[i][j])){
                unmarked+= board.board[i][j];
            }
        }
    }
    return last_called * unmarked;
}

int winningIndex(const std::vector<Board> &boards, const std::vector<int> &all_called, int *board_ind, int *called_ind){
    std::set<int> called;
    for(*called_ind = 0; ; (*called_ind)++){
        called.insert(all_called[*called_ind]);
        for(*board_ind = 0; *board_ind<boards.size(); (*board_ind)++){
            if(boards[*board_ind].hasWon(called)) {
                return score(boards[*board_ind], called, all_called[*called_ind]);
            }
        }
    }
}

int losingIndex(const std::vector<Board> &boards, const std::vector<int> &all_called, int *board_ind, int *called_ind){
    std::set<int> called;
    std::vector<bool> has_won(boards.size(), false);
    int win_count = 0;

    for(*called_ind = 0; ; (*called_ind)++){
        called.insert(all_called[*called_ind]);
        for(*board_ind = 0; *board_ind<boards.size(); (*board_ind)++){
            if(has_won[*board_ind]){
                continue;
            }
            if(boards[*board_ind].hasWon(called)) {
                has_won[*board_ind] = true;
                win_count += 1;
                if(win_count == boards.size()){
                    return score(boards[*board_ind], called, all_called[*called_ind]);
                }
            }
        }
    }
}




void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1
    int ind = 0;
    std::stringstream ss(data.at(ind));
    std::string item;

    std::vector<int> all_called;
    while(getline(ss, item, ',')){
        all_called.push_back(stoi(item));
    }

    std::vector<Board> boards;
    for(ind = 1; ind<data.size(); ind+=5){
        std::vector<std::string> d;
        for(int i=0; i<5; i++){
            d.push_back(data[ind+i]);
        }
        boards.emplace_back(d);
    }

    std::cout << "num boards: " << boards.size() << "\n";

    int board_ind, last_called_ind;
    int score = winningIndex(boards, all_called, &board_ind, &last_called_ind);

    std::cout << "Board " << board_ind << " wins after calling " << all_called[last_called_ind] << "\n";
    std::cout << "Score is " << score << "\n";



//    for (const auto& line : data) {
//        sscanf(line.c_str(), "");
//        std::cout << line << "\n";
//    }
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    int ind = 0;
    std::stringstream ss(data.at(ind));
    std::string item;

    std::vector<int> all_called;
    while(getline(ss, item, ',')){
        all_called.push_back(stoi(item));
    }

    std::vector<Board> boards;
    for(ind = 1; ind<data.size(); ind+=5){
        std::vector<std::string> d;
        for(int i=0; i<5; i++){
            d.push_back(data[ind+i]);
        }
        boards.emplace_back(d);
    }

    std::cout << "num boards: " << boards.size() << "\n";

    int board_ind, last_called_ind;
    int score = losingIndex(boards, all_called, &board_ind, &last_called_ind);

    std::cout << "Board " << board_ind << " wins after calling " << all_called[last_called_ind] << "\n";
    std::cout << "Score is " << score << "\n";
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
