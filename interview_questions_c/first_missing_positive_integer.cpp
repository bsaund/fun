//Given an unsorted integer array nums, return the smallest missing positive integer.
//
//You must implement an algorithm that runs in O(n) time and uses constant extra space.


#include <vector>
#include <iostream>
#include <cassert>

class Solution{
public:
    static int firstMissingPositive(std::vector<int>& nums){
        for(int i=0; i< (int)nums.size(); i++){
            int value = nums[i];
            nums[i] = -1;
            while(value >= 1 && value <= (int)nums.size()) {
                int tmp_value = nums[value - 1];
                nums[value - 1] = value;
                value = tmp_value;
            }
        }
//        for(auto num: nums){
//            std::cout << num << ", ";
//        }
//        std::cout << "\n";
        for(int i=0; i<(int)nums.size(); i++){
            if(nums[i] != i+1) {
                return i + 1;
            }
        }
        return (int)nums.size() + 1;
    }
};


void test_example_1(){
    Solution s;
    std::vector<int> nums{1,2,0};
    assert(s.firstMissingPositive(nums) == 3);
}

void test_example_2(){
    Solution s;
    std::vector<int> nums{3,4,-1,1};
    assert(s.firstMissingPositive(nums) == 2);
}
void test_example_3(){
    Solution s;
    std::vector<int> nums{7,8,9,11,12};
    assert(s.firstMissingPositive(nums) == 1);
}

void test_example_4(){
    Solution s;
    std::vector<int> nums{15, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};
    std::cout << s.firstMissingPositive(nums) << "\n";
    assert(s.firstMissingPositive(nums) == 2);
}






int main() {
    test_example_1();
    test_example_2();
    test_example_3();
    test_example_4();
}