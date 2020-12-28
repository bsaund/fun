nums = [9, 3, 1, 0, 8, 4]
# nums = [2,1,3]

d = {num: [i + 1] for i, num in enumerate(nums)}
t = len(nums) + 1
prev_num = nums[-1]

print(d)
while t <= 2020:
    print(prev_num)
    if len(d[prev_num]) == 1:
        prev_num = 0
    else:
        prev_num = d[prev_num][-1] - d[prev_num][-2]
    if prev_num in d:
        d[prev_num].append(t)
    else:
        d[prev_num] = [t]
    t += 1

print(f"{t}, {prev_num}")

# Part 2

nums = [9, 3, 1, 0, 8, 4]
# nums = [2,1,3]

d = {num: [i + 1] for i, num in enumerate(nums)}
t = len(nums) + 1
prev_num = nums[-1]

print(d)
while t <= 30000000:
    if t % 1000000 == 0:
        print(t)
    if len(d[prev_num]) == 1:
        prev_num = 0
    else:
        prev_num = d[prev_num][-1] - d[prev_num][-2]
    if prev_num in d:
        d[prev_num].append(t)
    else:
        d[prev_num] = [t]
    t += 1

print(f"{t}, {prev_num}")