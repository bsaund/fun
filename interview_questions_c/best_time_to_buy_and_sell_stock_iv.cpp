//
// Created by bsaund on 1/5/26.
//
/*
*You are given an integer array prices where prices[i] is the price of a given stock on the ith day, and an integer k.

Find the maximum profit you can achieve. You may complete at most k transactions: i.e. you may buy at most k times and sell at most k times.

Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).



Example 1:

Input: k = 2, prices = [2,4,1]
Output: 2
Explanation: Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 4-2 = 2.
Example 2:

Input: k = 2, prices = [3,2,6,5,0,3]
Output: 7
Explanation: Buy on day 2 (price = 2) and sell on day 3 (price = 6), profit = 6-2 = 4. Then buy on day 5 (price = 0) and sell on day 6 (price = 3), profit = 3-0 = 3.
*/


#include <cassert>
#include <iostream>
#include <limits>
#include <vector>

class Solution {
public:
    static int maxProfit(int k, std::vector<int>& prices) {
        if (prices.size() == 0) {
            return 0;
        }

        std::vector<int> buy(k+1, std::numeric_limits<int>::min()); // most profitable way to buy so far
        std::vector<int> sell(k+1, 0);


        for (const int p : prices) {
            std::cout << "Price: " << p << "\n";

            for (int i=1; i<=k; i++) {
                buy[i] = std::max(buy[i], sell[i-1] - p);
                sell[i] = std::max(sell[i], buy[i] + p);
            }
        }
        return sell[k];

            // for (size_t j = 0; j < k; j++) {
            //     std::cout << "j: " << j << ": min_value_after_transactions: " << min_values_after_transactions[j] << "\n";
            //     if (p < min_values_after_transactions[j]) {
            //         min_values_after_transactions[j] = p;
            //     }
            //     int profit = p - min_values_after_transactions[j];
            //     if (profit > 0) {
            //         std::cout << "Profit for " << j + 1  << " transaction is " << profit << std::endl;
            //         dp[j+1] = std::max(dp[j+1], dp[j] + profit);
            //         std::cout << "dp[" << j+1 << "] = " << dp[j+1] << std::endl;
            //         min_values_after_transactions[j+1] = std::numeric_limits<int>::max();
            //     }
            // }
        // }
        //
        // int max_profit = std::numeric_limits<int>::min();
        // for (int profit: dp) {
        //     std::cout << profit << ", ";
        //     max_profit = std::max(max_profit, profit);
        // }
        // std::cout << '\n';
        // return max_profit;

    }

};

int main() {
    std::cout << "hi\n";


    // {
    //     std::vector<int> v{};
    //     assert(Solution::maxProfit(2, v) == 0);
    // }
    // {
    //     std::vector<int> v{2, 4, 1};
    //     assert(Solution::maxProfit(2, v) == 2);
    // }
    {
        std::vector<int> v{3,2,6,5,0,3};
        assert(Solution::maxProfit(2, v) == 7);
    }
    {
        std::vector<int> v{5, 4, 3, 2, 1};
        assert(Solution::maxProfit(2, v) == 0);
    }
    {
        std::vector<int> v{5, 4, 3, 2, 1, 6};
        assert(Solution::maxProfit(2, v) == 5);
    }
    {
        std::vector<int> v{2, 10, 3, 11};
        assert(Solution::maxProfit(2, v) == 16);
    }
    {
        std::vector<int> v{2, 10, 3, 11};
        assert(Solution::maxProfit(1, v) == 9);
    }

}

