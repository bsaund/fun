notes = """1000495
19,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,521,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,523,x,x,x,x,x,37,x,x,x,x,x,x,13"""

your_time = int(notes.split("\n")[0])
bus_ids = [int(id) for id in notes.split("\n")[1].split(",") if id != "x"]
print(bus_ids)

leave_times = sorted([(bus_id - (your_time % bus_id), bus_id) for bus_id in bus_ids])
print(leave_times)
print(leave_times[0][0] * leave_times[0][1])

# Part 2
bus_offsets = [(int(id), offset) for offset, id in enumerate(notes.split("\n")[1].split(",")) if id != "x"]
print(bus_offsets)

departures = []
for i in range(100):
    for id, offset in bus_offsets[0:2]:
        departures.append((id * i - offset, id))

from math import gcd

def lcm(a, b):
    return (a * b) // gcd(a, b)

def find_alignment(bus_1, bus_2):
    id_1, offset_1 = bus_1
    id_2, offset_2 = bus_2
    t = offset_1
    while True:
        if t % id_2 == offset_2 % id_2:
            new_bus_id = lcm(id_1, id_2)
            return new_bus_id, t % new_bus_id - new_bus_id
        t += id_1


print(find_alignment(bus_offsets[0], bus_offsets[1]))

# test_bus_ids = [(17, 0), (13, 2), (19, 3)]
# test_bus_ids = [(67,0), (7,2), (59,3), (61,4)]
test_bus_ids = bus_offsets

combined_bus = test_bus_ids[0]
for bus in test_bus_ids[1:]:
    print(f"checking bus {combined_bus}, {bus}")
    combined_bus = find_alignment(combined_bus, bus)

print(combined_bus)
