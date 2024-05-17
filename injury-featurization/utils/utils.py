import pandas as pd
import spacy
import regex as re
import datetime as datetime

TEAMS = {
    "Angels": "ANA",
    "Diamondbacks": "ARI",
    "Braves": "ATL",
    "Orioles": "BAL",
    "Red Sox": "BOS",
    "Cubs": "CHC",
    "White Sox": "CHW",
    "Reds": "CIN",
    "Indians": "CLE",
    "Guardians": "CLE",
    "Rockies": "COL",
    "Tigers": "DET",
    "Marlins": "FLA",
    "Astros": "HOU",
    "Royals": "KCR",
    "Dodgers": "LAD",
    "Brewers": "MIL",
    "Twins": "MIN",
    "Mets": "NYM",
    "Yankees": "NYY",
    "Athletics": "OAK",
    "Phillies": "PHI",
    "Pirates": "PIT",
    "Padres": "SDP",
    "Mariners": "SEA",
    "Giants": "SFG",
    "Cardinals": "STL",
    "Rays": "TBD",
    "Rangers": "TEX",
    "Blue Jays": "TOR",
    "Nationals": "WSN",
}


# Injury Featurization
def add_injury_featurization():
    df = pd.read_csv("../../data/old_data/injury.csv")
    nlp = spacy.load("../injury_classification_model")

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


    df.to_csv("../../data/old_data/injury_featurized.csv", index=False)


# Cross-referencing
def get_key_bbref_no_num():
    historical_data = pd.read_csv("../../data/old_data/jeffbagwell_war_historical.csv", encoding="latin-1")

    curr_id = historical_data.loc[0, "key_bbref"]
    drop_ids = []
    years = []
    for i, row in historical_data.iterrows():
        if curr_id != row["key_bbref"]:
            biggest_year = max(years)

            if biggest_year < 2008:
                drop_ids.append(curr_id)
                print(f"Dropping {curr_id}")

            curr_id = row["key_bbref"]
            years = []

        years.append(row["year_ID"])

        historical_data.at[i, "key_bbref_no_num"] = row["key_bbref"][:-2]


    new_df = historical_data[~historical_data["key_bbref"].isin(drop_ids)]
    new_df.to_csv("../../data/war_historical_2008.csv", index=False)


def fetch_bbref():
    historical_data = pd.read_csv("../../data/war_historical_2008.csv", encoding="latin-1")
    injury_data = pd.read_csv("../../data/old_data/injury_featurized.csv", encoding="latin-1")

    anomalies = []
    rows_to_drop = []

    for i, row in injury_data.iterrows():
        date = row["date"]
        year = date.split("-")[0]
        if year == "2023":
            break

        team = row["team"]

        if team not in TEAMS:
            anomalies.append(row)
            continue
        franch_id = TEAMS[team]

        name = row["acquired"] if isinstance(row["acquired"], str) else row["relinquished"]
        if not isinstance(name, str):
            rows_to_drop.append(_)
            continue
            
        
        if "/" in name:
            names = name.split(" / ")
        else:
            names = [name]
        
        new_names = []
        for name in names:
            if "Jr." in name:
                new_names.append(name.replace(" Jr.", ""))
            
            new_names.append(name)

            name = re.sub(r"[^a-zA-Z ]", "", name)
            new_names.append(name)
        
        possible_ids = set()
        player_codes = set()
        for name in new_names:
            parts = name.split(" ")
            actual_name = []
            for part in parts:
                if "(" not in part and ")" not in part:
                   actual_name.append(part)
            
            actual_name = " ".join(actual_name)

            player_code = "".join(actual_name.split(" ")[1:])[:5] + actual_name.split(" ")[0][:2]
            player_code = player_code.lower()
            group = historical_data[(historical_data["key_bbref_no_num"] == player_code) & 
                                    ((historical_data["year_ID"] == int(year)) |
                                    (historical_data["year_ID"] == int(year) - 1)) &
                                    (historical_data["franch_ID"] == franch_id)]
            
            group2 = historical_data[(historical_data["key_bbref_no_num"] == player_code) & 
                                    (historical_data["year_ID"] >= int(year)) & 
                                    (historical_data["prev_tm"] == franch_id)]
        
            player_codes.add(player_code)
        
        
            if group.empty:
                anomalies.append(row)
                if group2.empty:
                    continue
                group = group2

            for _, r in group.iterrows():
                possible_ids.add(r["key_bbref"])
            
        if not possible_ids:
            anomalies.append(row)
            print(f"Anomaly for {name} for {team} on {year}")
            
            for player_code in player_codes:
                possible_ids.add(f"{player_code}01")

        injury_data.at[i, "key_bbref"] = str(possible_ids)
        print(f"Processed {name} for {team} on {year}")

        

    injury_data.to_csv("../../data/old_data/injury_cross_referenced.csv", index=False)

    anomalies = pd.DataFrame(anomalies)
    anomalies.to_csv("../../data/old_data/anomalies.csv", index=False)

    injury_data.drop(rows_to_drop, inplace=True)


# Injury Difference
def get_injury_diff():
    df = pd.read_csv("../../data/old_data/injury_cross_referenced.csv")

    for i in range(len(df)):
        row = df.loc[i]

        if not isinstance(row["relinquished"], str):
            continue

        il_type = row["il_type"]
        date = row["date"]
        date = pd.to_datetime(date)

        name = row["relinquished"]

        if il_type == "DTD":
            df.at[i, "days out"] = 0
            continue

        diff = 0
        for j in range(i + 1, len(df)):
            row2 = df.loc[j]
            activated = False
            if isinstance(df.loc[j, "acquired"], str):
                tmp_name = df.loc[j, "acquired"]
                activated = True
            else:
                tmp_name = df.loc[j, "relinquished"]
            
            if tmp_name == name:
                if activated:
                    date2 = row2["date"]
                    date2 = pd.to_datetime(date2)

                    diff = (date2 - date).days

                    df.at[i, "days out"] = diff
                else:
                    df.at[i, "days out"] = -1

                break
        
        print(f"Starting from {date.year}-{date.month}-{date.day}, {name} was out for {diff} days")
        

        
    df.to_csv("../../data/old_data/injury_diff.csv", index=False)


if __name__ == "__main__":
    df = pd.read_csv("../../data/old_data/injury_diff.csv")
    df = df[df["date"].str.split("-").str[0].astype(int) < 2023]

    df.to_csv("../../data/injury_v1.csv", index=False)