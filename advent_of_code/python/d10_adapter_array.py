adapters = """
126
38
162
123
137
97
92
67
136
37
146
2
139
74
101
163
128
127
13
111
30
117
3
93
29
152
80
21
7
54
69
40
48
104
110
142
57
116
31
70
28
151
108
20
157
121
47
75
94
39
73
77
129
41
24
44
132
87
114
58
64
4
10
19
138
45
76
147
59
155
156
83
118
109
107
160
61
91
102
115
68
150
34
16
27
135
161
46
122
90
1
164
100
103
84
145
51
60
"""

# Part 1
adapters = sorted([0] + [int(a) for a in adapters.split("\n") if a])
adapters += [max(adapters) + 3]

diffs = [b - a for a, b in zip(adapters, adapters[1:]) if b - a]
diff1 = len([a for a in diffs if a == 1])
diff3 = len([a for a in diffs if a == 3])
print(diffs)
print(diff1 * diff3)

# Part 2
import math

#
# def count_arrangements(ad):
#     for i in range(1, 4):
memorized_lengths = {1: 1, 0: 0}


def ways_to_connect_1_chains(chain_len):
    if chain_len not in memorized_lengths:
        ways = 1 + ways_to_connect_1_chains(chain_len - 1) + ways_to_connect_1_chains(chain_len - 2)
        memorized_lengths[chain_len] = ways
    return memorized_lengths[chain_len]


for i in range(7):
    print(f"ways to connect {i}: {ways_to_connect_1_chains(i)}")
ways_to_connect_1_chains(1)

chain_count = 0
ways = 1
for d in diffs:
    if d == 1:
        chain_count += 1
    elif d == 3:
        if chain_count >= 1:
            print(f"{chain_count=}")
            ways *= ways_to_connect_1_chains(chain_count)
        chain_count = 0

print(ways)
