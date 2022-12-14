import pandas as pd

def main():
    df = pd.read_pickle("./maxReturnsTrigger")
    print(df)

if __name__ == "__main__":
    main()