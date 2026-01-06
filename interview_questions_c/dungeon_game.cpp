//
// Created by bsaund on 1/5/26.
//
/*
*The demons had captured the princess and imprisoned her in the bottom-right corner of a dungeon. The dungeon consists of m x n rooms laid out in a 2D grid. Our valiant knight was initially positioned in the top-left room and must fight his way through dungeon to rescue the princess.

The knight has an initial health point represented by a positive integer. If at any point his health point drops to 0 or below, he dies immediately.

Some of the rooms are guarded by demons (represented by negative integers), so the knight loses health upon entering these rooms; other rooms are either empty (represented as 0) or contain magic orbs that increase the knight's health (represented by positive integers).

To reach the princess as quickly as possible, the knight decides to move only rightward or downward in each step.

Return the knight's minimum initial health so that he can rescue the princess.

Note that any room can contain threats or power-ups, even the first room the knight enters and the bottom-right room where the princess is imprisoned.



Example 1:


Input: dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]
Output: 7
Explanation: The initial health of the knight must be at least 7 if he follows the optimal path: RIGHT-> RIGHT -> DOWN -> DOWN.
Example 2:

Input: dungeon = [[0]]
Output: 1
*/


// Stream of conciousness thoughts
// The setup has a cute backstory with health and fighting, but basically this is just a path search problem.  The nodes are the square positions and the values in each square is the cost of each incoming edge.
// A few comments about they type of search:
// 1. the edges can be positive, 0 or negative. So vanilla A* which requires an admissalbe heuristic wont work. There are variants of A* that can support inadmissialbe heuristics. But this is overkill for this specific problemm
// 2. The problem says the knight only moves right and down. That means the graph is acyclic. So we never need to worry about revisiting any old nodes
// 3. A side-effect of this: The problem states "to reach the pricness as quickly as possible", but that is actually a pretty big constraint on the problem. There may be circular path where the knight could gain infitie health (e.g. 4 rooms with magic orbs). But in this problem we don't have to consider that
// 4. We do have to worry about visiting nodes from multiple paths. Because this game obeys the markov property (we don't care exactly which path we take to any node, only the total health), we just need to keep track of the "best_to_reach" (or g-value in A*) of each node.
// 5. We dont' care about the total path cost, we care about the minimum the health ever gets. E.g. We can do a first path, assuming the health starts at 0, then remember the maximum negative value we reach
// 6. Ah, this last part is actually kinda tricky. I think we will need to store 2 values. Both for the knigts minimum health, and current health along th epath. That makes our storage of g-values harder
// 7. Okay, lets see if I can make something that better obeys the markov property, ideally only requiring remembering a single number.
// 8. Ah, I need two things: Enough health to survive that cell, and enough health to survive {that cell + remaining journey}

#include <cassert>
#include <iostream>
#include <limits>
#include <map>
#include <vector>


class Solution {
public:
    static int calculateMinimumHP(const std::vector<std::vector<int>>& dungeon) {
        int m = dungeon.size();
        int n = dungeon[0].size();

        //TODO: we may want to validate the dungeon more - e.g. all dungeon[i] are the same size, and it is not empty

        std::vector<std::vector<int>> g(dungeon.size(), std::vector<int>(dungeon[0].size(), 0));

        g[m-1][n-1] = std::max(-dungeon[m-1][n-1], 0);

        // At the start we already know how many steps we need
        for (int step = m + n - 3; step >= 0; step--) {
            for (int i = std::max(0, step - n + 1); i < std::min(step + 1, m); i++) {
                int j = step - i;

                std::cout << "step = " << step << ": (" << i << ", " << j << ")";

                int health_needed_to_survive_room = std::max(0, -dungeon[i][j]);

                int health_needed_to_survive_right_path = std::numeric_limits<int>::max();
                int health_needed_to_survive_down_path = std::numeric_limits<int>::max();
                if (j+1 < n) {
                    health_needed_to_survive_right_path = g[i][j+1];
                }
                if (i+1 < m) {
                    health_needed_to_survive_down_path = g[i+1][j];
                }

                // we need to survive the punishment/reward from the current room + the best path to goal
                // Our health can never drop below 0 though, even if the remainng best path has a ton of heals
                int health_needed = std::max(0, -dungeon[i][j] + std::min(health_needed_to_survive_right_path, health_needed_to_survive_down_path));


                g[i][j] = health_needed;
                std::cout << ": health needed: " << g[i][j] << "\n";

            }
        }
        return g[0][0] + 1;
    }
};


int main() {
    std::cout << "dungeon_game\n";

    {
        std::vector<std::vector<int>> dungeon{{-2,-3,3},{-5,-10,1},{10,30,-5}};
        assert(Solution::calculateMinimumHP(dungeon) == 7);
    }
    {
        std::vector<std::vector<int>> dungeon{{0, -2, -2}, {0, -1, 0}};
        assert(Solution::calculateMinimumHP(dungeon) == 2);
    }

    {
        std::vector<std::vector<int>> dungeon{{0}};
        assert(Solution::calculateMinimumHP(dungeon) == 1);
    }
    {
        std::vector<std::vector<int>> dungeon{{-1}};
        assert(Solution::calculateMinimumHP(dungeon) == 2);
    }
    {
        std::vector<std::vector<int>> dungeon{{3}};
        assert(Solution::calculateMinimumHP(dungeon) == 1);
    }

    {
        std::vector<std::vector<int>> dungeon{{0, -2, 10},{-1,0,0},{0,0,0}};
        assert(Solution::calculateMinimumHP(dungeon) == 2);
    }
}





// First pass at solution
struct KnightHealth {
    int current_health;
    int minimum_health;

    KnightHealth(int current_health, int minimum_health) : current_health(current_health), minimum_health(minimum_health) {}

    [[nodiscard]] bool isNotBetterThan(const KnightHealth& other) const {
        return current_health <= other.current_health && minimum_health <= other.minimum_health;
    }
};

struct KnightHealthPossibilities {
    std::vector<KnightHealth> healths;

    void addOrIgnore(const KnightHealth& health) {
        for (auto already_realized_healths: healths) {
            if (health.isNotBetterThan(already_realized_healths)) {
                return;
            }
        }
        healths.push_back(health);
    }

    void writeHealths() const {
        for (auto h: healths) {
            std::cout << "\t(" << h.current_health << ", " << h.minimum_health << "), ";
        }
        std::cout << "\n";
    }
};


class OldSolution {
public:
    static int calculateMinimumHP(const std::vector<std::vector<int>>& dungeon) {

        const int m = dungeon.size();
        const int n = dungeon[0].size();
        if (dungeon.empty() || dungeon[0].empty()) {
            return 0; // Alternatively we could error because maybe an empty dungeon is not a valid input
        }

        std::map<std::pair<int, int>, KnightHealthPossibilities> g;
        const int starting_health = dungeon[0][0];

        KnightHealthPossibilities starting_knight_health;
        starting_knight_health.addOrIgnore(KnightHealth(starting_health, starting_health));
        g[{0, 0}] = starting_knight_health;

        // We know from the beginning exactly how many steps it will take
        for (int step = 0; step < dungeon.size() + dungeon[0].size() - 1; step++) {
            for (int i=std::max(0, step - m); i<std::min(step+1, m); i++) {
                int j = step - i;
                if (j < 0) {
                    std::cout << "step = " << step << "\n";
                    std::cout << "i = " << i << "\n";
                    std::cout << "j = " << j << "\n";
                    assert(false); // something went wrong with bounds;
                }
                auto health_so_far = g[{i, j}];

                // std::cout << "(" << i << ", " << j << ")\n";
                // health_so_far.writeHealths();

                if (j+1 < n) {
                    if (g.find({i, j+1}) == g.end()) {
                        g[{i, j+1}] = KnightHealthPossibilities();
                    }
                    int r = dungeon[i][j+1];
                    for (auto h: health_so_far.healths) {
                        KnightHealth new_health(h.current_health+r, std::min(h.minimum_health, h.current_health+r));
                        g[{i, j+1}].healths.push_back(new_health);
                    }
                }

                if (i+1 < m) {
                    if (g.find({i+1,j}) == g.end()) {
                        g[{i+1,j}] = KnightHealthPossibilities();
                    }
                    int r = dungeon[i+1][j];
                    for (auto h: health_so_far.healths) {
                        KnightHealth new_health(h.current_health + r, std::min(h.minimum_health, h.current_health + r));
                        g[{i+1, j}].addOrIgnore(new_health);
                    }
                }
            }
        }
        int highest_min_health = std::numeric_limits<int>::min();
        for (auto health: g[{m-1, n-1}].healths) {
            highest_min_health = std::max(highest_min_health, health.minimum_health);
        }
        return std::max(-highest_min_health, 0)+1;
    }
};