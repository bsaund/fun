#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_map>

//#include "absl/strings/match.h"
//#include "include/container_conversions.h"
#include "include/file_parsing.h"
#include "include/utils.h"
#include "data/d5.h"

std::string tmp_data =
        "0,9 -> 5,9\n"
        "8,0 -> 0,8\n"
        "9,4 -> 3,4\n"
        "2,2 -> 2,1\n"
        "7,0 -> 7,4\n"
        "6,4 -> 2,0\n"
        "0,9 -> 2,9\n"
        "3,4 -> 1,4\n"
        "0,0 -> 8,8\n"
        "5,5 -> 8,2";


class Point {
public:
    int x, y;
    Point(int x_, int y_) : x(x_), y(y_) {}
    bool operator==(const Point &other) const {
        return x == other.x and y == other.y;
    }
};

template<>
struct std::hash<Point>
{
    std::size_t operator()(const Point& p) const{
        return std::hash<int>()(p.x) ^ (std::hash<int>()(p.y) << 1);
    }
};

void addPoint(std::unordered_map<Point, int> &counts, const Point& p){
    if(counts.count(p) == 0){
        counts[p] = 0;
    }
    counts[p] += 1;
    std::cout << "Adding (" << p.x << ", " << p.y << ")\n";
}

void part_1(const std::vector<std::string>& data) {
    std::cout << "--------- PART 1 -----------\n";
    // Part 1
    std::unordered_map<Point, int> counts;

    for (const auto& line : data) {
        int x1, y1, x2, y2;
        sscanf(line.c_str(), "%d,%d -> %d,%d", &x1, &y1, &x2, &y2);
        if(x1 == x2){
            int lower = std::min(y1, y2);
            int upper = std::max(y1, y2);
            for(int y=lower; y<=upper; y++){
                addPoint(counts, Point(x1, y));
            }
        } else if(y1 == y2){
            int lower = std::min(x1, x2);
            int upper = std::max(x1, x2);
            for(int x=lower; x<=upper; x++){
                addPoint(counts, Point(x, y1));
            }
        } else {
            int x = x1;
            int y = y1;
            int dx = x2 > x1 ? 1: -1;
            int dy = y2 > y1 ? 1: -1;
            while(x != x2){
                addPoint(counts, Point(x, y));
                x += dx;
                y += dy;
            }
            addPoint(counts, Point(x, y));
        }
    }

    int sum=0;
    for(const auto val: counts){
        sum += (val.second > 1);
        std::cout << "(" << val.first.x << ", " << val.first.y << "): " << val.second << "\n";
    }
    std::cout << "sum: " << sum << "\n";
}

void part_2(const std::vector<std::string>& data) {
    std::cout << "\n\n\n--------- PART 2 -----------\n";
    // Part 2
    std::cout << "Part 2 has " << data.size() << " entries\n";
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
