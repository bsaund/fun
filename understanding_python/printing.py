import time

def repeated_printing_on_same_line():
    for i in range(100,0,-1):
        # \x1b[1
        print(f'\rtime: {i}', end='')
        time.sleep(0.1)


if __name__ == "__main__":
    repeated_printing_on_same_line()
