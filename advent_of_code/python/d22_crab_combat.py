from colorama import Style, Fore
p1_deck = """21
50
9
45
16
47
27
38
29
48
10
42
32
31
41
11
8
33
25
30
12
40
7
23
46"""

p2_deck = """22
20
44
2
26
17
34
37
43
5
15
18
36
19
24
35
3
13
14
1
6
39
49
4
28"""

p1_deck_orig = [int(a) for a in p1_deck.split('\n')]
p2_deck_orig = [int(a) for a in p2_deck.split('\n')]
p1_deck = p1_deck_orig.copy()
p2_deck = p2_deck_orig.copy()


i = 0
while p1_deck and p2_deck:
    # print(p1_deck)
    c1 = p1_deck.pop(0)
    c2 = p2_deck.pop(0)
    if c1 > c2:
        p1_deck.append(c1)
        p1_deck.append(c2)
    else:
        p2_deck.append(c2)
        p2_deck.append(c1)

winner_deck = p1_deck
if not winner_deck:
    winner_deck = p2_deck

print(winner_deck)
print(sum([a * (i + 1) for i, a in enumerate(reversed(winner_deck))]))


# Part 2

def play(d1, d2):
    """
    Returns: (winning player number, final deck configuration)
    """
    previous_decks = set()
    round = 0
    while d1 and d2:
        round += 1
        print(f'-- {Fore.GREEN}Round {round} {Style.RESET_ALL}--')
        print(f"Player 1's deck: {d1}")
        print(f"Player 2's deck: {d2}")
        if (tuple(d1), tuple(d2)) in previous_decks:
            return 1, d1
        previous_decks.add((tuple(d1), tuple(d2)))
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        if c1 <= len(d1) and c2 <= len(d2):
            d1_cpy = d1[0:c1].copy()
            d2_cpy = d2[0:c2].copy()
            winner, _ = play(d1_cpy, d2_cpy)
        else:
            winner = 1 if c1 > c2 else 2
        if winner == 1:
            d1.append(c1)
            d1.append(c2)
        else:
            d2.append(c2)
            d2.append(c1)

    if d1:
        return 1, d1
    else:
        return 2, d2

p1_deck = p1_deck_orig.copy()
p2_deck = p2_deck_orig.copy()
easy_d1 = [9, 2, 6, 3, 1]
easy_d2 = [5, 8, 4, 7, 10]
# w, winner_deck = play(easy_d1, easy_d2)
w, winner_deck = play(p1_deck, p2_deck)
print(f'Player {w} wins with deck {winner_deck}')
print(sum([a * (i + 1) for i, a in enumerate(reversed(winner_deck))]))
