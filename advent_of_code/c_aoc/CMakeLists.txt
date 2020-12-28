cmake_minimum_required(VERSION 3.17)
project(cpp)

set(CMAKE_CXX_STANDARD 20)

add_executable(cpp template.cpp include/file_parsing.h include/printing.h d2.cpp d3.cpp d4.cpp)
add_executable(d1 d1.cpp include/file_parsing.h include/printing.h)
add_executable(d2 d2.cpp include/file_parsing.h include/printing.h)
add_executable(d3 d3.cpp include/file_parsing.h include/printing.h)
add_executable(d4 d4.cpp include/file_parsing.h include/printing.h)