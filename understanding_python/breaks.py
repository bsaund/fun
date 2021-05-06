def break_from_try():
    for i in range(10):
        try:
            print("Beginning try")
            if i > 3:
                break
            raise RuntimeError("ahhhh")
        except RuntimeError as e:
            print(f"Error raised at iteration {i}")
    print(f"Loop exited at iteration {i}")


if __name__ == "__main__":
    break_from_try()
