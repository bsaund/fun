cmake_minimum_required(VERSION 3.17)
project(cpp)

set(CMAKE_CXX_STANDARD 20)

add_executable(cpp template.cpp include/file_parsing.h include/printing.h)
add_executable(d1 d1.cpp include/file_parsing.h include/printing.h)