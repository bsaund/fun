cmake_minimum_required(VERSION 3.17)
project(cpp)

set(CMAKE_CXX_STANDARD 20)

find_package(absl)

add_executable(cpp template.cpp include/file_parsing.h include/printing.h d2.cpp d3.cpp d4.cpp abseil_test.cpp)
add_executable(abseil_test abseil_test.cpp)
target_link_libraries(abseil_test absl::strings)

add_executable(d1 d1.cpp include/file_parsing.h include/printing.h)
add_executable(d2 d2.cpp include/file_parsing.h include/printing.h)
add_executable(d3 d3.cpp include/file_parsing.h include/printing.h)
add_executable(d4 d4.cpp include/file_parsing.h include/printing.h)




target_link_libraries(d4 absl::strings)