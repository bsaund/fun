cmake_minimum_required(VERSION 3.19)
project(interview_questions_c)

set(CMAKE_CXX_STANDARD 17)

add_executable(interview_questions_c main.cpp)
add_executable(sudoku_solver sudoku_solver.cpp)
add_executable(first_missing_positive_integer first_missing_positive_integer.cpp)
add_executable(n_queens n_queens.cpp)
add_executable(n_queens_sparse n_queens_sparse.cpp)
add_executable(templating templating.cpp)
add_executable(first_missing_positive_integer first_missing_positive.cpp
        dungeon_game.cpp)
add_executable(valid_number valid_number.cpp)
add_executable(distinct_subsequences distinct_subsequences.cpp)
add_executable(best_time_to_buy_and_sell_stock_iv best_time_to_buy_and_sell_stock_iv.cpp)
add_executable(dungeon_game dungeon_game.cpp)