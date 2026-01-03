//
// Created by bsaund on 1/3/26.
//

/*
*Given a string s, return whether s is a valid number.

For example, all the following are valid numbers: "2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7", "+6e-1", "53.5e93", "-123.456e789", while the following are not valid numbers: "abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53".

Formally, a valid number is defined using one of the following definitions:

An integer number followed by an optional exponent.
A decimal number followed by an optional exponent.
An integer number is defined with an optional sign '-' or '+' followed by digits.

A decimal number is defined with an optional sign '-' or '+' followed by one of the following definitions:

Digits followed by a dot '.'.
Digits followed by a dot '.' followed by digits.
A dot '.' followed by digits.
An exponent is defined with an exponent notation 'e' or 'E' followed by an integer number.

The digits are defined as one or more digits.



Example 1:

Input: s = "0"

Output: true

Example 2:

Input: s = "e"

Output: false

Example 3:

Input: s = "."

Output: false

*/


#include <iostream>
#include <string>
#include <regex>
#include <cassert>


class Solution {
public:
    static bool isNumber(std::string s) {
        // std::regex r(R"(^[-+]?(?:\d+|(?:\d+\.\d*|\.\d+))(?:[eE][-+]?\d+)?$)");
        // return std::regex_search(s, r);

        // std::cout << s << std::endl;
        // return false;

        if (not removeDecimalPrefix(s)) {
            return false;
        }
        // std::cout << s << std::endl;
        return s.empty() || isExponent(s);
    }

    /*
     * Removes the decimal prefix of s, if present
     * Returns true if the string had a valid decimal prefix, false otherwise
     */
    static bool removeDecimalPrefix(std::string& s) {
        enum State {BEGINNING, FIRST_NON_SIGN, PREDECIMAL, LEADING_DECIMAL, DECIMAL, POSTDECIMAL};
        State state = BEGINNING;

        size_t i = 0;
        for (; i<s.size(); ++i) {
            // std::cout << s[i] << std::endl;
            char c = s[i];

            if (state == BEGINNING) {
                if (c == '-' || c == '+') {
                    state = FIRST_NON_SIGN;
                } else if (std::isdigit(c)) {
                    state = PREDECIMAL;
                } else if (c == '.') {
                    state = LEADING_DECIMAL;
                } else {
                    return false;
                }
            } else if (state == FIRST_NON_SIGN) {
                if (c == '-' || c == '+') {
                    return false;
                }
                if (c == '.') {
                    state = LEADING_DECIMAL;
                } else if (std::isdigit(c)) {
                    state = PREDECIMAL;
                }
            } else if (state == LEADING_DECIMAL) {
                if (std::isdigit(c)) {
                    state = POSTDECIMAL;
                } else {
                    return false;
                }
            } else if (state == PREDECIMAL) {
                if (c == '.') {
                    state = POSTDECIMAL;
                } else if (!std::isdigit(c)) {
                    break;
                }
            } else if (state == POSTDECIMAL) {
                if (!std::isdigit(c)) {
                    break;
                }
            }
        }
        // std::cout << "erasing to " << i << "\n";
        s.erase(0, i);
        // std::cout << "After erasing: " << s << "\n";
        if (state == BEGINNING || state == LEADING_DECIMAL || state == FIRST_NON_SIGN) {
            return false;
        }
        return true;
    }

    static bool isExponent(const std::string& s) {
        // std::cout << "Checking exponent " << s << "\n";
        if (s.size() < 2) {
            return false;
        }

        if (s[0] != 'e' && s[0] != 'E') {
            // std::cout << "checking first char " << s[0] << "\n";
            return false;
        }

        size_t i = 1;

        if (s[i] == '-' || s[i] == '+') {
            i++;
        }


        bool at_least_one_digit = false;
        for (; i < s.size(); i++) {
            if (!std::isdigit(s[i])) {
                // std::cout << "Checking exponent char " << s[i] << "\n";
                return false;
            }
            at_least_one_digit = true;
        }
        return at_least_one_digit;
    }
};


int main() {
    std::cout << "valid_number\n";


    assert(Solution::isNumber("2"));
    assert(Solution::isNumber("0089"));
    assert(Solution::isNumber("-0.1"));
    assert(Solution::isNumber("+3.14"));
    assert(Solution::isNumber("4."));
    assert(Solution::isNumber("-.9"));
    assert(Solution::isNumber("2e10"));
    assert(Solution::isNumber("-90E3"));
    assert(Solution::isNumber("3e+7"));


    assert(!Solution::isNumber("abc"));
    assert(!Solution::isNumber("1a"));
    assert(!Solution::isNumber("1e"));
    assert(!Solution::isNumber("e3"));
    assert(!Solution::isNumber("99e2.5"));
    assert(!Solution::isNumber("--6"));
    assert(!Solution::isNumber("-+3"));
    assert(!Solution::isNumber("95a54e53"));
    assert(!Solution::isNumber("."));
    assert(!Solution::isNumber("-"));
    assert(!Solution::isNumber("+"));
    assert(!Solution::isNumber(""));

}
