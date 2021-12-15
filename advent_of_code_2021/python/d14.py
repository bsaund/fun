import more_itertools
from collections import defaultdict

easy_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


real_input = """KKOSPHCNOCHHHSPOBKVF

NV -> S
OK -> K
SO -> N
FN -> F
NB -> K
BV -> K
PN -> V
KC -> C
HF -> N
CK -> S
VP -> H
SK -> C
NO -> F
PB -> O
PF -> P
VC -> C
OB -> S
VF -> F
BP -> P
HO -> O
FF -> S
NF -> B
KK -> C
OC -> P
OV -> B
NK -> B
KO -> C
OH -> F
CV -> F
CH -> K
SC -> O
BN -> B
HS -> O
VK -> V
PV -> S
BO -> F
OO -> S
KB -> N
NS -> S
BF -> N
SH -> F
SB -> S
PP -> F
KN -> H
BB -> C
SS -> V
HP -> O
PK -> P
HK -> O
FH -> O
BC -> N
FK -> K
HN -> P
CC -> V
FO -> F
FP -> C
VO -> N
SF -> B
HC -> O
NN -> K
FC -> C
CS -> O
FV -> P
HV -> V
PO -> H
BH -> F
OF -> P
PC -> V
CN -> O
HB -> N
CF -> P
HH -> K
VH -> H
OP -> F
BK -> S
SP -> V
BS -> V
VB -> C
NH -> H
SN -> K
KH -> F
OS -> N
NP -> P
VN -> V
KV -> F
KP -> B
VS -> F
NC -> F
ON -> S
FB -> C
SV -> O
PS -> K
KF -> H
CP -> H
FS -> V
VV -> H
CB -> P
PH -> N
CO -> N
KS -> K"""

def part1(inp):
    lines = inp.split("\n")
    poly = lines[0]

    map = {line[0:2]: line[-1] for line in lines[2:]}

    paircts = defaultdict(int)
    for p in more_itertools.pairwise(poly):
        paircts["".join(p)]+=1

    for step in range(40):
        tmp = defaultdict(int)
        for it in paircts:
            c = map[it]
            tmp[it[0]+c] += paircts[it]
            tmp[c+it[1]] += paircts[it]
        paircts = tmp


    letcnts = defaultdict(int)
    for p in paircts:
        letcnts[p[0]] += paircts[p]
        letcnts[p[1]] += paircts[p]
    letcnts[poly[0]] += 1
    letcnts[poly[-1]] += 1

    cnts = sorted(letcnts.values())
    print(int((cnts[-1] - cnts[0])/2))





if __name__ == "__main__":
    inp = real_input
    # inp = easy_input
    part1(inp);