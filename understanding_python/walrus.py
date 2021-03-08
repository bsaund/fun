import time

start = time.time()
then = start

while (now := time.time()) - start < 5:
    dt = now - then
    print(f"The elsapsed time is {dt}")
    time.sleep(0.3)
