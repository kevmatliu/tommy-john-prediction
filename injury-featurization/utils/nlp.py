import spacy
from spacy.training import Example
import json
import random
import pandas as pd


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


def get_training_data():
    with open("../data/training_data.json", "r") as f:
        train_data = json.load(f)
    
    return train_data


def get_examples(batch, nlp):
    examples = []
    labels = {
        0: "IL_TYPE",
        1: "INJURY_TYPE",
        2: "INJURY_LOC"
    }

    for data in batch:
        text = data["text"]
        annotations = data["entities"]

        entities = []
        curr = 0
        for ent in annotations:
            loc = text.find(ent)
            if loc == -1:
                continue
            
            start = loc
            end = loc + len(ent)
            entities.append((start, end, labels[curr]))

            curr += 1
            
        examples.append(Example.from_dict(nlp.make_doc(text), {"entities": entities}))
    
    return examples


def train():
    nlp = spacy.blank("en")
    labels = ["IL_TYPE", "INJURY_TYPE", "INJURY_LOC"]
    ner = nlp.add_pipe("ner")

    for label in labels:
        ner.add_label(label)
    
    TRAIN_DATA = get_training_data()

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()

        for itn in range(50):
            random.shuffle(TRAIN_DATA)
            losses = {}
            
            for batch in spacy.util.minibatch(TRAIN_DATA, size=8):
                examples = get_examples(batch, nlp)
                nlp.update(examples, drop=0.5, losses=losses)
            
            print(f"Iteration {itn}  |  Loss: {losses}")

    nlp.to_disk("injury_classification_model")

    return nlp


def test_model(nlp):
    with open("../data/test_data.json", "r") as f:
        test_data = json.load(f)

    accuracy = 0
    total = 0
    for data in test_data:
        doc = nlp(data["text"])

        il_type, injury_type, injury_loc = None, None, None
        if len(data["entities"]) == 3:
            il_type, injury_type, injury_loc = data["entities"]
        elif len(data["entities"]) == 2:
            il_type, injury_type = data["entities"]
        else:
            il_type = data["entities"][0]

        for ent in doc.ents:
            if ent.label_ == "IL_TYPE":
                if ent.text == il_type:
                    accuracy += 1
                else:
                    print(f"{ent.text} | {il_type} | IL_TYPE | {data['text']}")
            elif ent.label_ == "INJURY_TYPE":
                if ent.text == injury_type:
                    accuracy += 1
                else:
                    print(f"{ent.text} | {injury_type} | INJURY_TYPE | {data['text']}")
            elif ent.label_ == "INJURY_LOC":
                if ent.text == injury_loc:
                    accuracy += 1
                else:
                    print(f"{ent.text} | {injury_loc} | INJURY_LOC | {data['text']}")

        total += len(data["entities"])

        print(data["text"])
        print(data["entities"])
        for ent in doc.ents:
            print(f"{ent.text} | {ent.label_}")
        print("=====================================")


    print(f"Accuracy: {accuracy / total}")


if __name__ == "__main__":
    nlp = spacy.load("../injury_classification_model")

    test_model(nlp)
    

