//
// Created by bsaund on 7/24/22.
//
#include <iostream>
#include <vector>
#include <algorithm>

class SpareQueenBoard{
public:
    std::vector<int> queens;
    std::vector<int> positive_diagonals;
    std::vector<int> negative_diagonals;

    bool can_add_queen(int i) const{
        auto contains = [](const std::vector<int> &v, int val){
            return (bool)std::count(v.begin(), v.end(), val);
        };

        if(contains(queens, i)){
            return false;
        }
        int s = (int)queens.size();

        if(contains(positive_diagonals, i+s)){
            return false;
        }
        if(contains(negative_diagonals, i-s)){
            return false;
        }

        return true;
    }

    bool try_add_queen(int i){
//        if(!can_add_queen(i)){
//            return false;
//        }
        int s = queens.size();
        queens.push_back(i);
        positive_diagonals.push_back(i + s);
        negative_diagonals.push_back(i - s);
        return true;
    }
};

std::vector<SpareQueenBoard> getAllNQueenSolutions(int n, int row, const SpareQueenBoard& b){
    if(row == n){
        return std::vector<SpareQueenBoard>{b};
    }
    std::vector<SpareQueenBoard> solutions;
    for(int j=0; j<n; j++){
        if(b.can_add_queen(j)){
            SpareQueenBoard tmp = b;
            tmp.try_add_queen(j);
            auto v = getAllNQueenSolutions(n, row+1, tmp);
            solutions.insert(solutions.end(), v.begin(), v.end());
        }
    }
    return solutions;
}



int main(){
    std::cout << "HI\n";
    for(int i=1; i<20; i++){
        std::cout << "There are " << getAllNQueenSolutions(i, 0, SpareQueenBoard()).size() << " solutions to the " << i << "-queens problem\n";
    }
}