#include <vector>
#include <iostream>
#include <unordered_set>
#include <cassert>
#include <optional>

typedef std::vector<std::vector<char>> Board;


class SudokuSolver{
public:
    static void solveSudoku(Board& b);
    static std::optional<Board> solveIfPossible(const Board& b);
    void isValid(const Board& b);
    static bool isRowValid(const Board& b, size_t row);
    static bool isColValid(const Board& b, size_t col);
    static bool isSubSquareValid(const Board& b, size_t row, size_t col);
    static bool isNewEntryValid(const Board& b, size_t row, size_t col);
};


void test_does_sudoku_solver_solve_sample_board(){
    Board input {{'5','3','.','.','7','.','.','.','.'},{'6','.','.','1','9','5','.','.','.'},{'.','9','8','.','.','.','.','6','.'},{'8','.','.','.','6','.','.','.','3'},{'4','.','.','8','.','3','.','.','1'},{'7','.','.','.','2','.','.','.','6'},{'.','6','.','.','.','.','2','8','.'},{'.','.','.','4','1','9','.','.','5'},{'.','.','.','.','8','.','.','7','9'}};
    Board output {{'5','3','4','6','7','8','9','1','2'},{'6','7','2','1','9','5','3','4','8'},{'1','9','8','3','4','2','5','6','7'},{'8','5','9','7','6','1','4','2','3'},{'4','2','6','8','5','3','7','9','1'},{'7','1','3','9','2','4','8','5','6'},{'9','6','1','5','3','7','2','8','4'},{'2','8','7','4','1','9','6','3','5'},{'3','4','5','2','8','6','1','7','9'}};
    SudokuSolver ss;
    ss.solveSudoku(input);
    assert(input == output);
    for(auto r: input){
        for(auto c: r){
            std::cout << c << ", ";
        }
        std::cout << "\n";
    }
}

void test_isRowValid_returns_true_when_no_duplicates(){
    Board input {{'5','3','.','.','7','.','.','.','.'},{'6','.','.','1','9','5','.','.','.'},{'.','9','8','.','.','.','.','6','.'},{'8','.','.','.','6','.','.','.','3'},{'4','.','.','8','.','3','.','.','1'},{'7','.','.','.','2','.','.','.','6'},{'.','6','.','.','.','.','2','8','.'},{'.','.','.','4','1','9','.','.','5'},{'.','.','.','.','8','.','.','7','9'}};
    SudokuSolver ss;
    for(size_t r=0; r<9; r++){
        assert(ss.isRowValid(input, r));
    }
}

void test_isRowValid_returns_false_when_duplicates_exist(){
    Board input {{'5','3','3','.','7','.','.','.','.'},{'6','6','.','1','9','5','.','.','.'},{'9','9','8','.','.','.','.','6','.'}};
    SudokuSolver ss;
    for(size_t r=0; r<input.size(); r++){
        assert(!ss.isRowValid(input, r));
    }
}

void test_isSubSquareValid_returns_true_when_no_duplicates(){
    Board input {{'5','3','.','.','7','.','.','.','.'},{'6','.','.','1','9','5','.','.','.'},{'.','9','8','.','.','.','.','6','.'},{'8','.','.','.','6','.','.','.','3'},{'4','.','.','8','.','3','.','.','1'},{'7','.','.','.','2','.','.','.','6'},{'.','6','.','.','.','.','2','8','.'},{'.','.','.','4','1','9','.','.','5'},{'.','.','.','.','8','.','.','7','9'}};
    SudokuSolver ss;
    for(size_t r=0; r<9; r++){
        for(size_t c=0; c<9; c++){
            assert(ss.isSubSquareValid(input, r, c));
        }
    }
}

void test_isSubSquareValid_returns_false_when_duplicate_in_square(){
    Board input {{'5','3','.','.','7','.','.','.','.'},{'6','.','.','1','9','5','.','.','.'},{'.','.','8','.','7','.','.','6','.'},{'8','.','.','.','6','.','.','.','3'},{'4','.','.','8','.','3','.','.','1'},{'7','.','.','.','2','.','.','.','6'},{'.','6','.','.','.','.','2','8','.'},{'.','.','.','4','1','9','.','.','5'},{'.','.','.','.','8','.','.','7','9'}};
    SudokuSolver ss;
    assert(!ss.isSubSquareValid(input, 0, 4));
    assert(!ss.isSubSquareValid(input, 1, 5));
    assert(ss.isSubSquareValid(input, 4, 0));

}



bool SudokuSolver::isRowValid(const Board &b, size_t row) {
    std::unordered_set<char> seen_numbers;
    for(const auto& c: b[row]){
        if(c == '.'){
            continue;
        }
        if(seen_numbers.find(c) != seen_numbers.end()){
            return false;
        }
        seen_numbers.insert(c);
    }
    return true;
}

bool SudokuSolver::isColValid(const Board &b, size_t col) {
    std::unordered_set<char> seen_numbers;
    for(const auto & r : b){
        char c = r[col];
        if(c == '.'){
            continue;
        }
        if(seen_numbers.find(c) != seen_numbers.end()){
            return false;
        }
        seen_numbers.insert(c);
    }
    return true;
}

bool SudokuSolver::isSubSquareValid(const Board &b, size_t row, size_t col) {
    size_t subsquare_r = (row/3)*3;
    size_t subsquare_c = (col/3)*3;
    std::unordered_set<char> seen_numbers;
    for(size_t dr=0; dr<3; dr++){
        for(size_t dc=0; dc<3; dc++){
            char c = b[subsquare_r + dr][subsquare_c + dc];
            if(c == '.'){
                continue;
            }
            if(seen_numbers.find(c) != seen_numbers.end()){
                return false;
            }
            seen_numbers.insert(c);
        }
    }
    return true;
}

bool SudokuSolver::isNewEntryValid(const Board &b, size_t row, size_t col) {
    return isSubSquareValid(b, row, col) && isRowValid(b, row) && isColValid(b, col);
}

void SudokuSolver::solveSudoku(Board &b) {
    b = solveIfPossible(b).value();
}

std::optional<Board> SudokuSolver::solveIfPossible(const Board &b) {
    for(size_t r=0; r<b.size(); r++){
        for(size_t c=0; c<b[r].size(); c++){
            if(b[r][c] != '.'){
                continue;
            }
            std::vector<char> possible_guesses {'1','2','3','4','5','6','7','8','9'};
            Board tmp_board = b;
            for(auto guess: possible_guesses){
                tmp_board[r][c] = guess;
                if(!isNewEntryValid(tmp_board, r, c)) {
                    continue;
                }
                auto attempt = solveIfPossible(tmp_board);
                if(attempt.has_value()){
                    return attempt.value();
                }
            }
            return {};
        }
    }
    return b;
}


int main(){
    test_isRowValid_returns_true_when_no_duplicates();
    test_isRowValid_returns_false_when_duplicates_exist();
    test_isSubSquareValid_returns_true_when_no_duplicates();
    test_isSubSquareValid_returns_false_when_duplicate_in_square();
    test_does_sudoku_solver_solve_sample_board();
    return 0;
}




