//
// Created by bsaund on 7/24/22.
//
#include <iostream>
#include <vector>
#include <cassert>

class Board{
private:
    std::vector<std::vector<char>> board;

public:
    explicit Board(int n_):
    board(n_, std::vector<char>(n_, '.'))
    {

    }

    [[nodiscard]] int size() const{
        return (int)board.size();
    }

    void print() const{
        for(auto& r: board){
            for(auto& c: r){
                std::cout << c << ' ';
            }
            std::cout << "\n";
        }
        std::cout << "\n";
    }

    [[nodiscard]] char at(int i, int j, char out_of_range_value) const{
        if(i < 0 || i >= board.size() || j < 0 || j >= board.size()){
            return out_of_range_value;
        }
        return at(i, j);
    }

    char& at(int i, int j){
        return board.at(i).at(j);
    }

    [[nodiscard]] char at(int i, int j) const{
        return board.at(i).at(j);
    }
};

bool can_place_queen(const Board& b, int i, int j){
    std::vector<std::vector<int>> directions{{0,1}, {0, -1}, {1, 0}, {-1,0}, {1,1},{1,-1},{-1,1},{-1, -1}};

    for(int offset = 1; offset <= b.size(); offset++){
        for(const auto& d: directions){
            if(b.at(i+offset*d[0], j+offset*d[1], '.') == 'Q'){
                return false;
            }
//            std::cout << "There is no queen at " << i+offset*d[0] << ", " << j+offset*d[1] << "\n";
        }
    }
    return true;
}

void num_queen_arrangements_helper(const Board &b, int start_i, std::vector<Board>& solutions){
    if(start_i == (int)b.size() -1){
        for(int j=0; j<b.size(); j++){
            if(can_place_queen(b, start_i, j)){
                Board tmp = b;
                tmp.at(start_i, j) = 'Q';
                solutions.push_back(tmp);
            }
        }
    }

    long count = 0;
    for(int j=0; j<b.size(); j++){
        if(can_place_queen(b, start_i, j)){
            Board tmp = b;
            tmp.at(start_i, j) = 'Q';
            num_queen_arrangements_helper(tmp, start_i+1, solutions);
        }
    }
}

std::vector<Board> num_queen_arrangements(int n){
    std::vector<Board> solutions;
    num_queen_arrangements_helper(Board(n), 0, solutions);
    return solutions;
}




void test_can_place_queen_returns_true_when_possible(){
    Board b(4);

    assert(can_place_queen(b, 0, 0) == true);

    b.at(3,2) = 'Q';
    assert(can_place_queen(b, 1, 1) == true);
    assert(can_place_queen(b, 3, 2) == true);
}

void test_can_place_queen_returns_false_when_not_possible(){
    Board b(4);
    b.at(1,1) = 'Q';
    std::vector<std::vector<int>> invalids{{0,0},{1,0},{0,1},{2,0},{0,2},{2,2},{3,3}};
    for(const auto& invalid: invalids){
//        std::cout << "invalid: " << invalid[0] << ", " << invalid[1] << "\n";
        assert(can_place_queen(b, invalid[0], invalid[1]) == false);
    }

}


int main(){
//    test_can_place_queen_returns_true_when_possible();
//    test_can_place_queen_returns_false_when_not_possible();
    for(int n=1; n<=99; n++){
        std::cout << "THere are " << num_queen_arrangements(n).size() << " solutions to the " << n << "-queens problem\n";
    }
    std::cout << num_queen_arrangements(1).size() << "\n";
    std::cout << num_queen_arrangements(4).size() << "\n";
    std::cout << num_queen_arrangements(2).size() << "\n";

//    for(auto& sol: num_queen_arrangements(7)){
//        sol.print();
//    }
}