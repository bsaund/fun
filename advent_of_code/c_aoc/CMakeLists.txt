cmake_minimum_required(VERSION 3.17)
project(cpp)

set(CMAKE_CXX_STANDARD 20)

find_package(absl)

add_executable(cpp template.cpp include/file_parsing.h include/printing.h d2.cpp d3.cpp d4.cpp abseil_test.cpp d5.cpp d6.cpp d7.cpp)
add_executable(abseil_test abseil_test.cpp include/container_conversions.h)
target_link_libraries(abseil_test absl::strings)

add_executable(d1 d1.cpp include/file_parsing.h include/printing.h)
add_executable(d2 d2.cpp include/file_parsing.h include/printing.h)
add_executable(d3 d3.cpp include/file_parsing.h include/printing.h)
add_executable(d4 d4.cpp include/file_parsing.h include/printing.h)
add_executable(d5 d5.cpp include/file_parsing.h include/printing.h)
add_executable(d6 d6.cpp include/file_parsing.h include/printing.h include/container_conversions.h)
add_executable(d7 d7.cpp include/file_parsing.h include/printing.h include/container_conversions.h)



set(EXTERNAL_LIBRARIES absl::strings)

target_link_libraries(d4 ${EXTERNAL_LIBRARIES})
target_link_libraries(d5 ${EXTERNAL_LIBRARIES})
target_link_libraries(d6 ${EXTERNAL_LIBRARIES})
target_link_libraries(d7 ${EXTERNAL_LIBRARIES})