import pandas as pd
import json


def injury_data_to_df():
    with open("../injury/injury.json", "r") as f:
        data = json.load(f)
    
    return pd.DataFrame(data)


def clean_injury_data(df):
    df["date"] = pd.to_datetime(df["date"])
    df["team"] = df["team"].str.strip()
    df["acquired"] = df["acquired"].str[3:]
    df["relinquished"] = df["relinquished"].str[3:]
    df["notes"] = df["notes"].str.strip()
    df["url"] = df["url"].str.strip()

    return df

if __name__ == "__main__":
    df = injury_data_to_df()
    df = clean_injury_data(df)
    df.to_csv("../data/injury.csv", index=False)

