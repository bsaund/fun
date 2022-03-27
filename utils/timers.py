import time
import sys

def countdown(time_sec):
    while time_sec > 0:
        mins, secs = divmod(time_sec, 60)
        timeformat = f'{int(mins)}:{secs:05.2f}'

        print(f"Sleeping for {timeformat}", end='')
        dt = 0.07
        time.sleep(dt)
        time_sec -= dt

        sys.stdout.write('\r')
        sys.stdout.flush()
