//
// Created by bsaund on 1/3/26.
//

/*
*Given two strings s and t, return the number of distinct subsequences of s which equals t.

The test cases are generated so that the answer fits on a 32-bit signed integer.



Example 1:

Input: s = "rabbbit", t = "rabbit"
Output: 3
Explanation:
As shown below, there are 3 ways you can generate "rabbit" from s.
rabbbit
rabbbit
rabbbit
Example 2:

Input: s = "babgbag", t = "bag"
Output: 5
Explanation:
As shown below, there are 5 ways you can generate "bag" from s.
babgbag
babgbag
babgbag
babgbag
babgbag
*/


#include <iostream>
#include <vector>
#include <cassert>

class Solution {
public:
    static int numDistinct(std::string_view s, std::string_view t) {
        const int len_s = (int)s.size();
        const int len_t = (int)t.size();
        if (len_s < len_t) return 0;
        if (len_t == 0) return 1;

        std::vector<int> ways_to_make_prefix_j_of_t(len_t+1, 0);
        ways_to_make_prefix_j_of_t[0] = 1;

        for (int i=0; i<len_s; i++) {
            for (int j=len_t; j >= 1; j--) {
                if (s[i] == t[j-1]) {
                    ways_to_make_prefix_j_of_t[j] += ways_to_make_prefix_j_of_t[j-1];
                }
            }
        }
        return ways_to_make_prefix_j_of_t[len_t];
    }
};


int main() {
    std::cout << "distinct_subsequences" << std::endl;

    assert(Solution::numDistinct("abc", "abc") == 1);
    assert(Solution::numDistinct("rabbbit", "rabbit") == 3);
    assert(Solution::numDistinct("babgbag", "bag") == 5);
    assert(Solution::numDistinct("aaaaa", "a") == 5);
    assert(Solution::numDistinct("aaaaa", "aa") == 10);
}