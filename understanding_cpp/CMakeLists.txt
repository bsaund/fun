cmake_minimum_required(VERSION 3.17)
project(understanding_cpp)

set(CMAKE_CXX_STANDARD 17)

add_executable(understanding_cpp src/main.cpp)
add_executable(vector_polymorphism src/vector_polymorphism.cpp)
add_executable(reference_wrapper  src/reference_wrapper.cpp)
add_executable(lambdas  src/lambdas.cpp)
add_executable(default_operators  src/default_operators.cpp src/strings.cpp)
add_executable(compare_strings  src/strings.cpp)
add_executable(list src/list.cpp)

