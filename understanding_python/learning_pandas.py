import pandas as pd


def multiindex_trim():
    df = pd.DataFrame.from_dict({('a', 1): [1, 2, 3], ('a', 2): [1, 2, 3], ('b', 1): [2, 4, 6], ('c', 2): [3, 6, 9]}).transpose()
    df.index.get_l
    print(df)

def main():
    df = pd.DataFrame.from_dict({'a': [1, 2, 3], 'b': [2, 4, 6], 'c': [3, 6, 9]})
    df.index = df.index.map(lambda i:  str(i+1) + ' mississippi')

    def trim(s):
        return s[0:6]

    df.index = df.index.map(trim)

    print(df)


if __name__ == "__main__":
    # main()
    multiindex_trim()