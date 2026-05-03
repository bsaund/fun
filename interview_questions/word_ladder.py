"""
A transformation sequence from word begin Word to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord
Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.



Example 1:

Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.
Example 2:

Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
"""





"""
A few obeservations. This is a graph search problem. And the shortest sequence will never revisit the same word, so we have a DAG
We could start with a word, compute all successors, and store an open list and a visited list. At each iteration we add the current node to the visited list and all successors not in the visited list to the open list. 
I think we want to figure out how to compute successors efficitnetly. Looping over the entire dict every time seems inefficient. 
We could compute a single list of all successors in N^2 time by looping over the dict for each item in the dict, storing a dict of successors. 
Not too bad, I wonder if we could be more efficient. 
We also would get a practical benefit if we prioritize our search, a best-first search. Best can be cost to come (i.e. transforamtions so far) + heuristic cost to go. 
So it seems like we want A* here. We have a beautiful heuristic, because we know cost to go is at least the hamming distance between the current word and the goal, since we can only change one letter at a time. 
Finally, just noting that I will implenet a unidir3citonal search, but in practice a bidirectional search is often faster. (Happy to dive into this more)
"""

import heapq





class Solution:
    @staticmethod
    def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
        if begin_word == end_word:
            return 1

        open_list = [(0, begin_word)]
        cost_to_come = {begin_word: 1}

        while len(open_list) > 0:
            # print(open_list)
            _, cur_word = heapq.heappop(open_list)
            next_cost = cost_to_come[cur_word] + 1
            for next_word in Solution.successors(cur_word, word_list):
                if next_word == end_word:
                    # print(f"Found maching word {next_word}: cost to come {cost_to_come}")
                    # print(next_cost)
                    return next_cost
                if next_word in cost_to_come and cost_to_come[next_word] <= next_cost:
                    continue
                cost_to_come[next_word] = next_cost
                minimal_cost_to_go = Solution.hamming_distance(next_word, end_word)
                heapq.heappush(open_list, (next_cost + minimal_cost_to_go, next_word))

        # No solution exists
        return 0 # Note, this was the problem spedification, but is kinda ambiguous with end_word == begin_word. An unsuspecting user might get 0 and assume that means the words are the same.


    @staticmethod
    def successors(word: str, word_list: list[str]) -> list[str]:
        return [w for w in word_list if Solution.hamming_distance_is_1(word, w)]

    @staticmethod
    def hamming_distance(a: str, b: str) -> int:
        if len(a) != len(b):
            raise ValueError(f"Words {a} and {b} are different lengths, problem assumption violated")
        dist = 0
        for c_a, c_b in zip(a, b,):
            dist += c_a != c_b
        if dist == 0:
            assert a == b, "My code has a problem, I got that the hamming dist is 0 but the strings are different"
        return dist

    @staticmethod
    def hamming_distance_is_1(a:str, b:str) -> bool:
        """
        Checks if the hamming distance is 1. Early return if greater than one
        """
        if len(a) != len(b):
            raise ValueError(f"Words {a} and {b} are different lengths, problem assumption violated")
        dist = 0
        for c_a, c_b in zip(a, b,):
            dist += c_a != c_b
            if dist > 1:
                return False
        if dist == 0:
            assert a == b, "My code has a problem, I got that the hamming dist is 0 but the strings are different"
            return False
        assert dist == 1, "My code has a problem, dist should be 1 after this part of the calculation"
        return True




def main():
    assert Solution.ladder_length("aa", "aa", word_list=["aa"]) == 1, "Simple example did not work"
    assert Solution.ladder_length("aa", "ab", word_list=["ab"]) == 2, "Simple example did not work"
    assert Solution.ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"]) == 5
    assert Solution.ladder_length("hit", "cog", ["hot","dot","dox","lot","lxg","cog"]) == 0


if __name__ == "__main__":
    main()