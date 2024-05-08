import pandas as pd
import json


def generate_data(type_of_data, num):
    df = pd.read_csv("../../data/injury.csv")
    df = df[df["relinquished"].notnull()]

    data = []

    for _ in range(num):
        row = df.sample()
        if any([row["notes"].values[0] in datum["text"] for datum in data]):
            continue

        data.append({
            "text": row["notes"].values[0],
        })
    
    if type_of_data == "training":
        with open("../data/training_data.json", "w") as f:
            json.dump(data, f, indent=4)
    elif type_of_data == "test":
        with open("../data/test_data.json", "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    generate_data("test", 40)
    

    