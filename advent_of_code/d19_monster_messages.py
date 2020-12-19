rules_str = """98: 29 106
14: 29 1 | 106 52
16: 1 106 | 69 29
63: 106 113 | 29 39
117: 29 88 | 106 115
65: 86 106 | 47 29
62: 96 96
109: 106 128 | 29 50
12: 79 29 | 65 106
54: 106 29
64: 29 63 | 106 89
26: 106 105 | 29 22
99: 82 106 | 53 29
67: 71 106 | 129 29
20: 3 29 | 75 106
82: 29 40
114: 106 41 | 29 19
125: 107 106 | 104 29
79: 29 52 | 106 110
112: 106 98 | 29 60
101: 29 3 | 106 98
94: 29 117 | 106 67
126: 45 106 | 75 29
120: 106 55 | 29 34
77: 106 38 | 29 25
75: 106 106
60: 106 106 | 96 29
68: 29 112 | 106 100
127: 29 10 | 106 32
115: 103 106 | 23 29
81: 52 29 | 123 106
18: 29 98 | 106 60
86: 106 51 | 29 3
38: 35 106 | 68 29
102: 29 72 | 106 12
47: 98 106 | 98 29
13: 77 106 | 64 29
66: 106 5 | 29 126
121: 40 29
70: 93 106 | 118 29
90: 120 106 | 44 29
17: 26 29 | 49 106
1: 3 29 | 62 106
25: 29 28 | 106 24
103: 119 29 | 98 106
27: 106 3 | 29 58
8: 42
73: 106 59 | 29 1
88: 85 106 | 27 29
128: 106 114 | 29 70
31: 29 78 | 106 56
28: 46 29 | 7 106
124: 102 29 | 37 106
52: 98 29 | 95 106
23: 105 29 | 22 106
69: 96 51
24: 29 21 | 106 53
29: "b"
36: 29 45 | 106 98
78: 109 29 | 125 106
32: 29 98 | 106 75
118: 29 95 | 106 58
119: 106 106 | 29 96
71: 2 29 | 21 106
43: 96 40
42: 106 124 | 29 13
22: 29 29 | 106 106
19: 40 106 | 54 29
113: 96 101
7: 40 29 | 95 106
10: 106 40 | 29 105
6: 29 119 | 106 3
80: 51 29 | 95 106
46: 106 119 | 29 60
30: 51 29 | 58 106
61: 54 106
57: 22 106 | 45 29
76: 29 18 | 106 43
92: 91 29 | 14 106
91: 106 48 | 29 43
72: 106 17 | 29 81
21: 29 40 | 106 58
40: 106 106 | 29 106
49: 106 119 | 29 98
33: 108 106 | 6 29
122: 29 75 | 106 40
53: 29 95 | 106 75
100: 96 3
110: 119 106 | 62 29
41: 106 105 | 29 54
35: 29 46 | 106 112
107: 15 29 | 83 106
56: 94 29 | 90 106
97: 29 22
4: 106 98 | 29 51
59: 106 60 | 29 58
50: 106 16 | 29 73
93: 29 60 | 106 51
111: 29 74 | 106 110
74: 58 96
15: 122 106 | 57 29
37: 106 87 | 29 92
58: 29 106 | 29 29
104: 29 66 | 106 76
39: 106 4 | 29 121
2: 29 58 | 106 62
48: 62 29 | 22 106
106: "a"
34: 29 121 | 106 27
116: 106 58 | 29 54
96: 106 | 29
85: 29 58 | 106 119
3: 106 29 | 29 29
0: 8 11
123: 98 106 | 40 29
95: 106 96 | 29 106
83: 106 20 | 29 36
129: 106 61 | 29 27
45: 29 29
108: 106 119 | 29 3
5: 29 119 | 106 60
11: 42 31
44: 9 106 | 111 29
84: 106 30 | 29 97
87: 106 99 | 29 127
9: 122 29 | 116 106
89: 29 84 | 106 33
55: 86 106 | 80 29
105: 29 106 | 106 29
51: 106 29 | 106 106""".split('\n')

messages = """baabbbaaaaababbbbbabbbaabbabaabaababaaba
abbabaaaababbbbbababaaba
abaaaaababbbbbaaaabbabbb
bbbbbbbaaaabaaaaaaababbabbbbbbabbbbabaababbabbaababbabba
abaababbabababbaabbaaababababaababababaabbbbbbab
bbaabaaabbbaabaaaaaaabba
aaabbabaabbababbababbbab
babaaaaabbbbabaaaaaaaaabaabababa
aababbaabaaaabbbaababbaabbbababababbabaabbabbaab
baabbbbabbbababbaaabaaaababbbbab
aaaaaababaaabaaaaababaaa
babbabbabbbababaaabaaaaabaaaabab
abaabababbbababbababbaaaaaaabbbabbbbaabbbabbbabbbabbabab
bbabaaabaaaaabaaabbabbbbbababbba
bbbababbabaaabbbabbaaaaaababbabb
babbabbbaaaaaabbabaaabbbbbbbbababaabaaabaaabaabbaabbabba
abbaababbabaabbbbbabaaab
ababaaaaaababbaaabbbbabb
abbaaaaabbbaabbbaabaabbbbababbba
bbababaaaababbbabababaabaaabbbbbabbabbabbbbabbbbaabbababbaaaabbb
aabababbbabbbaabaaababaabbababbbabbaaaabbaaaaaab
baaabaabbbbbaaaaaaababab
abaabbababbbaaabbbbaaaaabababbabbbabbaaaababaabbbbbbabab
bbababaabaaaababaaaababb
abbabbaababaabbbababbbab
ababaabbbbbaababbbbabaaa
bbbaaaaaabaaaaabbbabbaba
abaabaabaaabaabbaaababaabaaaabbababbbaaaaaababab
aababbaaaababbabbbbaababababbbbababaaababababbbaabbbbbba
abbbabbbabbabbaabbbaabba
baababbaabbbabbbaaaabaabbbbbbbab
babbabbabbbaabaabbabbbab
bbabbbbbbbbabaaabaaaaaaa
abbbbaaababbbbbbabbabbbb
aababaabaaabbaaabaaaabaa
abaabaabbbaaabbbaaabbbaabbbbbabaaabaabaaabbaaabbbbaaabaabbaabbab
aabababbaaabaaaaaabbbabb
aabbbaababaabbbaaabbbababbbbabbabbbbaaaabbbbbaaa
babbabaaaaabbababbbabaababbbabbbbaaababb
bbabbbbbbabbabaabbbbbbaa
aababbaabbbabbbabaaaaaba
baaabbbabaaaabbbbababbabaaaababa
abbbaaabaabbbbaabbbbbbbabbabaaba
baaabbbabbbbabaaabbabbba
aabbbbaabbabbbaaabababbaaaabbaaaaabbbbba
bbaabbaababaaabbabbbbbbb
abbababaabaabaaaaaababab
baaaabaabbabaaaaabaababa
aabbbbaabbbabaaaaabaabbb
bbaaaaaababababaaaaabbab
bbabbabbaaababbbbbaabaab
bbaabbabababbaaaabbaaaaaabbaaaaabbaaaaaaaabababbbabbbaba
baaabbbabaaabbbabababbba
aabbaabbbbbabaaabbbbbaab
aaaabaaaaaabbbbabbbaabbabaaaabab
aaabbabbaaabbaaaabbbbabb
abbaabbbaababbbbabbbbaabbbaaababaaabababbbbbabbababbbaaaaaaaaaabbbbabababbbbbbbb
aaaabbbbababbbbbbbaabbba
ababaaaabaabaaaabaabaaba
aaabbbbbbbaaaaaababaaaaa
aabbbababbaababbbbbbbbaa
bbbaabaabaababbbabbabababababbaaaaabaaaabbabbbaaabbabbbabbabbaab
bbbbbbbaaaaaaaabbaaababa
abaabbabbabbbbbaaaaaabab
aaaaabbbbaabbbbabaabaabbbbbaababbaabbbbbbabaabaa
abbababbbaaaaaababbabbab
bbaababbababaaaaabaabbaa
bbbaaaababaabbbbaabbbbbbaabbaaba
abbaaababbaababaabbaaababbaaaaaaaaaaaaaa
babbbbaabaababbaaaaaaabbabaaabbbbaabababbbbabbba
aaaaabbbaabbabbbababaaaabababbabbbbababa
baababbaabababaabababbbb
baaaabbaabbabaaaabbbabab
aaabaabbaaabbabbababbabbbbbbbbababaaabbabababbbabaabbbbbbabbaaaababbaaab
baaabbababaabaabbbbaabaaaaaabbaababbbaba
bababaabbbbbaaaabbbaaaaaababbabaabaaaaabbabaabaabbabaaaababbaabbaaabbaab
baaabbabbbbaaaaaaaaaaabbbaaaabbbbaababbaaaabbaabbbabaaaaaabbbbab
bbaabbaaababbababbbbbbaa
babbbbbaababbaabbaabbaba
bababbaaabbbaabaaabbabbbbaaaaabb
aabbbababbababaababbaaaabbabaabb
aababbababbbbababbbbaaaabbaaaaaaaaababaa
aabbaabbbbaabaaaabaaabab
baaabbbabbbaaababbbbbabbbbbbaaab
babbbbbababaabbbabababab
bbbbabaabaaabaaaaabbaabaaabbbbbaabbabbbbaaaaabbaabbababa
abbbababaabbbaabaabababa
bbabbaabbbbbbbaababbaaab
abbaaababaaabbababbaaabbbabbbbabababaaab
baababaababaabaabbabbbaaabbbababababbabababaaabababbbbabbaaabbaa
bbabaababababaabbabbbaba
abaabbabbaaaabbbbabababb
aabbabbbbaaabaaaabbbaabaabaabaabaaabaababbabbbaabbabbaab
aaabbaabbbabaabababbabbbbbaaaabaaaaabbbbbbbabababbabbbababbaaabb
aaabbaaaabaaaaababbababbaaaabbbbbabbbbabaaabbbabbbbbbbab
abbbaabbbabbaababbabbbab
baaabbbaaabbbaabaababbaaabaabaabbbbaabba
abaaaaabbbabbabbbbbaabbb
babaaaaaabababaaaaababbabbbaabaaaaabaaab
baababbabbbbbabbaabbabba
aaaaabbbabbbbbaabbabbaaaabbbaababaababaaaababaaabaabbaaababaaaba
babaaaaaabbaaaaaabaababbaabbbabbabbabababbabbbbaabbaabaabbbaabba
aaababbaababbbbbaaaaaaaa
aababbaaaaaaaabaaaaaaabbbbbbbbabbbbaabbb
bababbabbaaabaaabaaaaaabaabbabaaaababaaa
aaaabbbaaabbabbabbbbbaab
babbabbabbbbaaaaaabaaaabaabbbbaaababaaaaabababbbabaaaaabbbbabbaabaaabaab
baabbbbbbaaaaaabbbababbaaaababbbbbaaabbaabbbabaaaaabaaab
abbaaababbababbbbabbbabaabaaaabb
aabaaabbbaabababbbbbabab
baabaabbabbaaabbaaaaabbbaaababbbbaaaaaaa
bbaababbababaaaabbabbbbbbbbabaabbaabbabbababbbabbabbabab
abababaababbbaabbaabbaaa
bbbaaaaaaabbabbbababbbaa
abbbaaaabbbbaabaaabbbabb
babbbaabbbbbbabaaaaabbbbbbbbbaaaaababbaababaabbabbbabbab
aababbbabaaababababbabbb
bbabbaaaaabbbbaabbbabbaa
baabbabbbbabbbbbababbabaaaaabaabababbaabbbbaaaaaabbabaab
abbbbaaaaaabaaaabbbaaaab
abbbbabababaaaaabbaaaaab
babbaaaabaaaababaaaababbaabaabab
ababbbbbbbbaabaaaaabbbab
aabbbaabababbabbaababbabaabbbbabbabaabbaaaaaaaba
babbaabababbaababbaaabaa
baababaaaabbabaaabbabbba
aababbaabaaabbbbbababaaaabbabbab
aaabaaaababbbbbbbabbaaab
aaababbbabbabbaababbabbaabbaaaaaabbabaaaabbbbbba
bbbaabababbbaababaabbaaa
abaaaaababaababbaabbbbaaaabbaabaaaabababbbabbbbaababbaaa
aababbaabaabaabbabbbbbaaaabaaaaababbbbaababbabab
abbbbabaaababaabbbbbabaaabbaaababaabaaaaaabbbbabbabbabbbbabaabbaaaaaaaaa
abaabbababbaaabaaaaababb
abaaaababaabbbbaaababbaaabbbaaabbababbaaababaaababbbbbbb
aabbabaabbabbbbbaaaabbaaababbbabbbaaaaaaaaababbabaaabbba
baababbabaabbbabbbbbaabbbbababbbbabbaaab
bbbababbababbbbbbabbbbaaabbabbabbbabbbab
abbbbaaaabaaabbabaabaaba
bbbbabaabababbaababbaaab
baaabbabbabbbaabbbabaaaa
abababaabbbaababbbbbabbaaababaabbaaaabab
abbabbaaaabbbaabbbaabaaabbabbbbababaabaaaabbaaab
babababaaabbaabbbbaabbbbbbbbbabbbababbbaababaaab
bbabaababaaabbbbbbbabaaabbaaaabb
abaaabbbabbabaaababababb
ababaaaaabaabaabbaaabbaa
abbbaabaabbbaabaaaabbaaaaaaabaabbabaaaba
abaaaaaabababbbaabaababbaaababbaaaabbbabbbbaaaaa
aaabbaaabababbaabbababbb
abbaaaaababbabbaabbabaab
aababaabaaaabaabbbaabbaaababbabb
baaaaabaabbabbbbbbabbabbbbbabaabababbaaababbbabababaaabbbabaaababaaaaabb
baaabaaaabbbaabbbbbbabab
aababbaaabbbaabbabaaaaabbabbabbababbbbaabbbbaaaabbaaaabb
bbbbbabbbaaabbbbbbbabaabbbbaaaba
bbaaababbababaaabaabaababaaabaababbaaaba
abaaaaaaaaaaaaabaaabbbab
abbabbaaaaaabbbabaaaaabaabbaaaabbaabababbaaaaaaaaababbbbbbababba
aabbaaaaabbbabbbaabbaabbaabbbbababbbabaa
ababbababaababbaabaaabbaaaabaabbabbbbbab
bbaaaaaabbabbabbabbbbabb
bbbababbbbaabbaaabaabbbaabbbabbbbbabbaab
aaaabbbbbababbbbbaabaabbbbbaabbaaaabbaab
bbbababbaaaaaababbbaabba
abaaaaaababbabbabbbaaaab
abababaaabbaababbaaabbaa
aababbabaaaaaaabbabbbaaa
babaaabbabbbabbabbabbbbaabaaabaaaaaabbaababbaaab
baabaabaabbaabbaaaaaaabababaaaabababbabbbaaaaabbabbbaabb
abbabbaaaaaabbbbabaaabaa
babaabbbabaabaaabbbbabbb
bbbbbbbaabaabaababaabbbbabbbabaa
aabbabbbabbbaaabaabbaaaaaaaaabaabbabbaabbbbaabbaaabbbaaabaaabbaabbaaabba
abbbabbbabbaababbabbbbbbabbbbabb
bababbaabbbabababbbaaabaaababbba
aabbbbabaabbabaaababaabbabababaaaabbaababbbbabbbabbaaabababbaabb
aaaaaabbaabaaabbabbabaab
baaabaaabababaabbabbbbaaababaaaaabbaabaa
aaaababbbbbbbbbbaabaaaab
bbbaaaaabababbabababaaba
bbaabaaabaabbbaabbababbaabaaabbabbbaabba
abababaabbbaabbbbbaaabbb
bbaaaabababbaaaababaabbaaababbaababbbbbabbbabbbabbabbaaababababbaababbbbababbaaaababababbbaabbbb
bbabbaaaabbaaababababbababababbaabaaabaa
abbaabaaabbbbabbaaabababbbbbaaaababbababbbbabbba
baaaabbbbabbbbbbbbbaababbaabbaba
aabbabbabaaaababababababbabaababbbaaabbb
abbaabbbbababbbabababaabaaababbbbbbabbababbaababababbbbb
abaababbbaabaabbbaaaaaba
bbaaaaaabbbaababbabaababbaaaababaaaababaabbbaaababbbbbbaabbbbbabbabbbbbaaaaaaaba
abbaaabaaaababbbbaababbaaababbbb
abaabaaabbbbaababababaaaaaaababa
bbaabbbbbbabbbaabbaaaaba
abbbbbaabaaabbabbbabaaba
baabbbaabaabbbabbabaabbbbbaaaabb
abaabaabbbabbabbabbaaabaaabbaaaabaababbbaabbbaaaaaabbbaa
abbaaabaabbbaaaabaabaaab
baaabbbabbaabaaabaababaabbbabbbaaaabbbbbbabbbaaaabbaaaab
abbbbbaaabaababaabaaabbbbbabbbbbbabbbabababbbbaabaabbbaaaaaabbaa
abbbabbbbabaabbbaabababbbbabbbabaaaabbab
bbaabaaaabababbababaabab
aaabaaaabbbaabaabbabaaab
abbaababbbaabbbbaabababbbbbabaabaaabaaaababababbabbaaaab
bbbaababbaaaabbababaaaba
bbaabababbbabaabbabbaaab
abbbbabaabbbaabbabababbabaaabbabaababaabbabbbabbabbbbbbabbaabaabbabababb
baabababbbaaaaababaaabaa
aabaaaaaaaabaabbabbbbaaabbabbaab
aaabaabbaaaabaababbaaababbabaaba
abaaaaaaabbbaabbabaaabbbbaabbbbaaaaaaaaaaaabababaaaabbba
baabbbaaaaabbababbbbbbbb
baababbaabbaaabbaaaaaaabbbabaaabbbabaabb
aabaaaaabaabbbbbaabbbaabaaababbabbabbaabaaaaabab
ababbaabaaabbabbbbaabbba
baaabbbbababbababababbabbbbabaabbabbbaabaaaaabaaababbbab
aabbbbabaabbbbababababbabaabbaabbbabbaaaababaabbababaaab
bbbbbabbabbabbaaabaabbba
babbbaabbbabbbabbbbabbaabaaaaaaabaabababaaababbaabaaaaabbabbbbbaaaabaaabbbbabaaa
abbbaaabbaaabbbabbbbbaab
aabbbaaaabaaabaabbbabbaabaaababa
bbbaaaaaabaaaaabaaaabbbbbabababaaaabbaaabaabaabbaabaaaba
abbaaabaaabaabaabaabaaab
baabababbbaaaababbabbababbbaabba
abababaababbbaabaaabaabbbbabbbbaaaaabaaaaababaaaababaabababaaaba
bbababbaaababbbbbbbaaaababababab
bbbbbabbbaababbababbabbb
abbbbaaaaaaaabbbbbbaabbb
aabaabababbaaabaaaabaababaaaabbaabaaaaaabbbbabab
abbaaababbbbbabbaaabaaaaabababbb
abaabbabaabbaabbbbabbbbaabbbbabbaaabbbbaabbbbaba
aaaabbbbaaaaaabbbaabaaab
baaabbabbaabbbaaaaaaaababababbaaabaaabbabaaaaaaabaaabbaa
abbaaaaabbabbaaaaababbbb
bbbabaabaaaaaaabbaaaabab
aaaaaabbbaaabbbabbbabaabbaababaabaaaabaa
abaabaaaabbbbabaabaabbabbabbabab
ababbababbbbabaaabbaaabbaaaababa
abbabbabbbaaabbaababbaabaabaaaababbabababbbaababbaabbbbbbabbabbaabbbbabbbaabbbab
baababababaabaaaabbbaaba
baabaabbbbbbbbbaaaabaaab
abbabbaabaaabaaababbabbb
bbaabaaabaabbabbaababaabbbbbabbaaababbba
bbabbabaaaabbaabbbabbbaabababbbbbbbbaaabbaabbbababbaaaab
babbbbbabbbabbbaaaabbbba
aabbbbaaabababbaaaababbbbabaaaab
baabababaabaaaaabbaaaaaaabbbbbaabbaaaabb
abbabbabaabbbaaaaaababaaababbabb
bbbabaaaabaabbbaababaaab
bbaabaaabbbbaabbabbbbababbaaaaaaababaaaabbabaabb
ababaaaaabbbaabababbbbbaaabaabba
abbbbababbabbbaaaababbabbbababbabaabaaba
aabaaaaabaabaabbbbabaaaa
abaaabbbbabbbaabbbaababbabbaaabaababaaab
aaaababbbbbbaaabaaabbbbabaaababa
bbabbbaabbababaaabbbbbaabaaaaabb
babbaabababababaaababbba
abbbaaabababbbbbaabbabba
bbbbabbbaaabaabbbaaababaaabbabbabbbabbbbbaaabaabbabaaabbaaaaaabbbaaabbabaababaab
baaaabbbbbbababaaabbaaab
babbbaababbabababaabaaaaaaaabaaaaabbabab
babbaaababaaabaabaabbaba
ababbbbbbbaabbaaabbbbbbb
bbbabbbabbababaababbaaaabaaabbbbabbaaabbbabbbaaabbababbb
aabbaaaaaaaaaabbabaaaabb
abbbbaaabbbbbbbaabaabaaababbaaab
babbbbbabaababaabaabaaab
abbaabaababaaaababababaabababbaaaababaaaaaaabaab
ababbaabbabaaaaaabbaabaa
bababaabbabbabbaababbbaa
abaababbaabaaabbbbabbabbbbaaaaab
abbabbbbaababaaaabaaaabbababbbbbaaaabaaaabaaaaab
abbbaabbbabbbaabbababbba
abbbbbabababbabbaaaabbaabbbbabaabaabbaaabbaabbaabaabaaab
babbabaababaaaaabbaaabaa
aababbaabbabbbaaabbabaaabbbbabaaaaaabbbbaaabaaabbbbbbbbb
bbbabaaabaaaabbbabaabaaaaaaaaaabbaabbbbaababaaabaabaaabaaabaabaababbbbab
abbbaabbbbbbabaabababbba
aaabaababaaabbbaaaaabbab
baaabbbbbabbaababbbbbaab
bbbbaabaabbabbabbabbaaab
babbbbbababbaaaaaaaaabaa
abbbaaabaabaaabbbaababbababbabbabbabbabbabbabaab
bbbbababbbaabbaaaaabbbabababaaabbaaaabaaabbabbbabababbbbaaaabbbaaaababab
abaabaaaabbabaababbababbabbbbaabaaaabbaa
abaabaababaabaabaaabbbbbababbbbaaaababbbbaaaabaaabababbbbbabaabb
aabbbaabababaaaabababbba
aaabaabbbbaababaabbbabbbbaabbaab
abbbbbbabbbbbaaabaaaabaa
bbbaaaaabbbaabaabababaabbbabbbbb
abaabaababbabbaabbaabababbaabbaabaabbaab
bbbbbaaaabbababbbabbbbbbaabbaaababbbabababbabaaabbabbaaabaabbbababaabbbbabaabaab
abaabbbaaabaaaaaabbaabbb
bbabbaaababaaaaaabbaaaaaababbbbbabbabbba
bbbabbbaabaaababaabbabbbaabbbabbbaabaaab
bbabbbbbabbabbbaaaaaabbbbbaaabbaabaabbbabaaabbaaabaabaaa
bbaaabaababbbaaabaabaaabababababababbaaaaaabbaba
bbbabababbbbbabbababbbbbbababaabaaabbaaabbababbbbabababbbbbbbababbbabbbb
babbaabaaaaabbbbababbbbbaaaaaabaabaaabbaabbabbbb
aaabaababbabbbbbbbabaaab
babbbbaabbbaaaaabaaaabaa
ababbbbabbabbaaababbbaabbbaababaabbbbabaaaaabbaaaaabbbba
ababbaabbabbaabababaabab
aaaabbabbabbbbbabbbbbaabaaaaabbbabaabaaaaababaababbabbbb
bbabbbbbaababaabbbaabbbbaabbbaabbbbbabaababbaaabaaaabbbabbbabbbb
baababbaaabababbabbbaabbababbbbaaaabbabababaaaba
baabbbabbabbaaaabbabababbbaabaab
baababaabbbabaabbbbbaaababbabaabbabababbabbabaab
bbaaaaaabbaaaaaaaaaabbaa
baaaaaabbbaababbaababbba
bbabbbbbbaaaabbbbbbbbabbbbbaaabbaabaaaba
aaabbbbbabaaabbbaabbaaab
baaabaababababaabaabbabbbabaaaaaabaaabaa
bababbabbababaaababbbbab
abbbaabbbaaabbabbaabababbbabbaab
bbaababbaaabbaaaabaaabbaaabaabba
bbbbabbaabaaabbabbaaabba
abaabbabaaabaabaababbaabbabbaaaaabbaababbaaaaaaa
aaaaaaaabbaaabbabaabbababbbbbaaabababbba
abbaaaaabaabaaaababbbabb
aabbbbaaaaaaabbbabaaaabaabbbaaaaabbabaaababbabbb
bbabbbbbbbbababaaabbabab
bbbaabababbbababababaaba
bbabbabbbaabaaaaababbabb
bbbbbbbaaabbaabbbaaababa
bbaaaaaaababbbbaabbaabaabaaaaabbbaaabababababbaababbaababbabaaabbababaab
bbbaaaaabbbbaabbbaaabbbbbbbbbaba
abaaabbbbaaaabbabbabbaaabaaaabab
baabbabbbbaababaababbbbaabbbabbaaaaaababbaaaaabbaaabbbaa
aaabbbbaaabaaabbbbbabbabaaabbbbbbaabbaaaaaaabaabbbbaaabaabaaabab
abaaaabbbbbbabbbaaaabbab
baababaabaabbbbaabbaaabbaaaabaabbbbabaabbababbba
ababbaaabbabbababaabaaabaaabaabbaabaaababbababab
bbaababaaaaaaabbababbabaaabbbbabaabababa
abbabbaaaaaaaaababaabbaa
aaabaaaababbaaaabaaaaaabbabbabaaabababbbbbaaaaab
babbbaabababaabbabababaaaaababbabbabbbabbababbba
aabbabaabbabbbbbbabbaaab
baabbabbbabbbbbabbaaababababbaabbaaaaaaa
aaaabbbbaaaaaaaabaabaabbbbabbaabbbbaaababaaabbaaabaabbabaaaaabab
bbababbaabababaababbaaabbbaabbbaaaaaaaaa
aabbaaaaaabaababbaaaaaba
aabbabbbabbababababaaaba
baaabbbabaabbabbaaabbbbbabaabaaaababbaab
baababbabaaabaababbabbbb
babbaabaabbaaabbbbaaaaaaaaaaababababbbab
aaaabaaababbabbababbabbbaabbabbabbbbabbbbbbaaaaaabaabbaababbbbbbaabbabaaaaaababa
babbabaaaaabbbaaaabbaaabbbababbbaaabababaababbbb
abaabaabbaabbbbbabaabbabbaababbb
aaabbaaaaabbbaabaaababbabbbaaababbbbabab
babbabaaabbaaaaabaaaabbaababbaabbabbbaaa
aabaababaabbabbbbbbabbab
bbababaaabaabbaaaabaaabbababaabababbbbbaabaababaabbabababbbbbaab
bbabababbbaaababbabbbaba
abaaaababbabbbbbbbabbbba
baabbbbababbbbbabbaaababbaababaaabaabbbababbbbabababbaaabbabaababbabaaaa
aaaaabbbabaaabbbbabbbaabbaaaabbaaabbbabbbbaaabba
bababaaabbaabaaababbaabb
aaabbabbbbbabaaabbbbbbaa
bbaabbbbbbabbabababababbabaababa
bababaaaaaabbabaaababbabbbbbbbbaaaaabbab
ababbaabbbaabbbbbbababaabaababaa
aaabbbaababaabbabaaaaaaabaaaabab
baaabbabbabbbbbaabababab
abbbaababaabababaaabaaab
aabbbaabaabbbaabbaaabaaaabbabbaabbaabbba
aaabbabbabaabaaaababbabb
ababaabbbababbabababbabb
bbbbbbbabbaaababbabbabab
abbaaabbbabbbbbbbaababbaabbbaababbbbaaab
bbbabbbabaabaaaaaabaabba
babbabaabbbbbaabbaabbabaabbbbaabbbabbabbbabbbaabaabbabaaaabaaaba
bababaababbaaabaabaabaabaaabaabbbaabaaabbbaaabba
baabbbaaabbaaabaaababbba
bababaabbaaabbbbbaaaabbaaabbbbba
babbbabbbabaaaabbabababb
abbaaabaabaabbbaababaaba
baaabaabbbbababbbabbbaabbbbbabaaaaaabbbbaaabaaabaaaabbabaaaaaaaabaaaabab
baaabbbababbbbaabbaababbaabaabaa
aabaaabbaabababbbbbabaaabbabbbab
bbbbabbbbbaabbbababbabab
baabaabbbbbbbabbaaababab
baabaaabbbaaabbaaabbabbababbbbab
aaabaabbabbabaaabbbaabba
babaaaaaaababbaaabbbabaa
bbbbaababaabaaaababaabba
babbbaababbaaabbaaaaabaa
bbabbabbaabbbaabbaaaabab
baabbbabaababbabbbbbbbab
abbaaabbabbbaabbbbbabaabababaaaaaababbabaabaabbb
bbbbaabbbabbaababbbbbbab
bbbbabbababbaaaaabbbabaabbbaaaaaabbbaabababbaabbbaabbaaabbbaabaa
aaaaaababaababaaababbbaa
bbbbaabbabbbbbaaaaabbbba
aabbabaaabbbbababaaabbababaababbaabaaababbabbabababbbabb
babbabbababbabaabbbaaabb
aababbabaaababbaaabaabaa
bbabaabababbbbabbbabbbba
bbaaaaaabaaabbbbbbbaaaab
abaabbbabbaababaaababbabbbaabbabbbbbbbaa
abaabbabaaaabbbbaaabbababbbababbbbbabbab
abaababbabaababbbaaaaaaa
bbbaaaaabbaabaabaabaaabaaabaabbbbaaaabab
aabaabbbbbbbabbbabababaaabaaaaaabbbbbbabaaaabbbaaabbabaaaababaabbabaaababbaabaab
aababaabaaaaaabababbbaabbbabbbaabaabbbababaabbabaaaababb
baabbbbbaaabbabaaabaaabb
aaaaabbbbbababbaaabaababbbaababbaabbabaababaabba
aabaaabbaaaaabbbabbaabaa
bbbabababaabaaaabbbababaaaabbababbbabaabaababbba
babababbbbabbbabbaabbaabbabbbaba
ababbbbabbabbbaaabaaabbabbbbbaab
baabbbababaababbbbabbabbbaabaabbaabbabab
abbaaabaaabbaabbbaaaabaa
bbbaaaaaabaaabbaaaaaabaa
aaaabaabaaabaaaaabbbbbbbbabbaaab
abbaaaaabbabbbaaabaabbaa
aaaabbbbbbababaababaaaab
baabababbabbbbbbababbbbbbbaabbba
baaaaaabbbbbbabbababbabb
baaabaabbbaababbbabaaabbbbaabbbbbabbaaababababbb
baaaabbaabaaabbabaaababb
abbaaabaabbaaabbaabbbaabbaabbbbbabbbaaababaababbabababababaaabba
baabbabbabbbbabaaababaaa
abbaaabbabababbbbabaabbbabbaababbbaababaababaaab
aabbaaaabaabbbbabbbaaabb
aababbabababbbbbaaaabbaa
bbaababbbbbabbbababbbbaabaaaaababaaaaabb
aaaaabbbaabaaabbbbababbb
abaabaaabaababbababaabbbabababaabaabaabbabaaaaaabbbbaaababbbbbbbbbaaaaab
aababaabbaaabaabbabaaabbbaaabbababbababbbbaabaabbbabababbbbbabababaaaabb
abbbababbbabbabbbabababb
baabbbbbaabbabaabbababbb
abaabaaaabaaaaabaaababbaaabbbabbaaaabaaa
bbbaababbbaabaaaababaaaaaabbbbbb
aaaaabbbbaabbbbbbabaaabbaabbbababaabbbaa
baaaabbbabaaaaaaabbbaaaaabbbaaabbbbbabbaaaaaabbababaaaba
aabbaabbbaabbbababbbabaa
abbbaaababaaaaabbaaaabaa
babbbbaaaabbaabaaabababbaabaabbbaaabbbababbbaabaaaaababbbbabbbabbabbabaabbbbbaaa
abbbaabbbababbababbbaabbbbababbbaababbba
baabaaaaabbbaaabababbaaababbababbabbbabbabbbbabbbabababa
babbbbbbbbbaaaaaabbabbab
aabaaaaaabbbbbaabbaabbab
babbabaaabbaaaaabaaababb
aabaaabbaaaaaabbbbbbbabbbbbaabababababbababbabbaaaaabababaabbababbabaababababbba
bababaaaabbababbabbbababababaabb
abbbababbbbbbabbaabbbbba
bbabababaaabbbbbbbbbaaab
aabbaaaabbbabaaaaaabaaaaabaababbbabbbbbaaababbaaaababbbb
baaabaababbabbaabaabbbbaabbaaaaaabbbaabb
aabbaabbbabababaababbabb
babababababbbbaaaaaaaabbbaaabbbabaaaabaa
baabbbaabbaaababbaaaabbaabbaaaabbabaabba
abbbababbabbabaaaaabaaaaabbabbaaaaabbbba
bbabbaaaabbbaaaaabbbabba
bbaabbaabaababababbbabba
aaababbbbaaabbabbbbbbaaa
aabaabababbaaaaaabaaaabb""".split('\n')

cr = sorted(rules_str, reverse=True)
cr = [r + ' ' for r in cr]
cr = [r.replace('"a"', 'a').replace('"b"', 'b') for r in cr]

for i in range(len(cr)):
    if '|' in cr[i]:
        a, b = cr[i].split(':')
        cr[i] = a + ': (' + b + ') '

for i in range(len(cr) - 1):
    r, replacement = cr[i].split(":")
    for j in range(i + 1, len(cr)):
        cr[j] = cr[j].replace(' ' + r + ' ', replacement)
        cr[j] = cr[j].replace(' ' + r + ' ', replacement)
rule_0 = cr[-1][3:].replace(' ', '')

import re

print(len([1 for line in messages if re.match(rule_0 + 'c', line + 'c')]))

# Part 2

cr = sorted(rules_str, reverse=True)
cr = [r + ' ' for r in cr]
cr = [r.replace('"a"', 'a').replace('"b"', 'b') for r in cr]


repeats = 10
for i in range(len(cr)):
    if cr[i].startswith('8:'):
        cr[i] = '8: ' + '| '.join(['42 ' * i for i in range(1, repeats)])
        print(cr[i])
    if cr[i].startswith('11:'):
        cr[i] = '11: ' + '| '.join(['42 ' * i + '31 ' * i for i in range(1, repeats)])
        print(cr[i])
    if '|' in cr[i]:
        a, b = cr[i].split(':')
        cr[i] = a + ': (' + b + ') '

for i in range(len(cr) - 1):
    r, replacement = cr[i].split(":")
    for j in range(i + 1, len(cr)):
        cr[j] = cr[j].replace(' ' + r + ' ', replacement)
        cr[j] = cr[j].replace(' ' + r + ' ', replacement)
rule_0 = cr[-1][3:].replace(' ', '')

import re

print(len([1 for line in messages if re.match(rule_0 + 'c', line + 'c')]))
