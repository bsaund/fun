#include <iostream>
#include <vector>
#include <cassert>

class Solution {
public:
    static int firstMissingPositive(std::vector<int>& nums) {
        for (int i=0; i< static_cast<int>(nums.size()); i++) {
            int num_to_place = nums[i];
            while (num_to_place > 0 && num_to_place <= static_cast<int>(nums.size()) && num_to_place != nums[num_to_place-1]) {
                int new_num_to_place = nums[num_to_place-1];
                nums[num_to_place-1] = num_to_place;
                num_to_place = new_num_to_place;
            }
        }

        for (int i=0; i< static_cast<int>(nums.size()); i++) {
            if (nums[i] != i + 1) {
                return i+1;
            }
        }
        return static_cast<int>(nums.size()) + 1;
    }
};



int main() {
    std::cout << "Testing firstMissingPositiveInteger" << '\n';

    {
        std::vector<int> v{1,2,3};
        assert(Solution::firstMissingPositive(v) == 4);
    }
    {
        std::vector<int> v{1,3,4};
        assert(Solution::firstMissingPositive(v) == 2);
    }
    {
        std::vector<int> v{3,4,-1,1};
        assert(Solution::firstMissingPositive(v) == 2);
    }
    {
        std::vector<int> v{1,2,0};
        assert(Solution::firstMissingPositive(v) == 3);
    }
    {
        std::vector<int> v{7,8,9,11,12};
        assert(Solution::firstMissingPositive(v) == 1);
    }
}