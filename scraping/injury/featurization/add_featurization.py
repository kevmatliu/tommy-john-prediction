import pandas
import spacy


def add_injury_featurization():
    df = pandas.read_csv("../../data/injury.csv")
    nlp = spacy.load("injury_classification_model")

    df["il_type"] = None
    df["injury_type"] = None
    df["injury_loc"] = None

    cnt = 0
    for i, row in df.iterrows():
        if not isinstance(row["notes"], str) or not isinstance(row["relinquished"], str):
            continue

        doc = nlp(row["notes"])

        il_type, injury_type, injury_loc = None, [], []
        for ent in doc.ents:
            if ent.label_ == "IL_TYPE":
                il_type = ent.text
            elif ent.label_ == "INJURY_TYPE":
                injury_type.append(ent.text)
            elif ent.label_ == "INJURY_LOC":
                injury_loc.append(ent.text)

        df.at[i, "il_type"] = il_type
        df.at[i, "injury_type"] = injury_type
        df.at[i, "injury_loc"] = injury_loc

        cnt += 1

        if cnt % 100 == 0:
            print(f"Processed {cnt} rows")


    df.to_csv("../../data/injury_featurized.csv", index=False)


if __name__ == "__main__":
    add_injury_featurization()