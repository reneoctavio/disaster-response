import spacy
import typer

import pandas as pd

from pathlib import Path
from spacy.tokens import DocBin
from sqlalchemy import create_engine


CORPUS_DIR = Path(__file__).parent.parent / "corpus"


def load_data(split: float = 0.80):
    """Load data from SQLite and split data into train, dev, and test"""
    path = "../../data/DisasterResponse.db"
    engine = create_engine(f"sqlite:///{path}")
    df = pd.read_sql_table("dataset", engine)
    df = df.set_index("id")

    # Randomize
    df = df.sample(frac=1, random_state=42)

    # Split dataset
    train_split = int(split * df.shape[0])
    dev_split = train_split + int((df.shape[0] - train_split) / 2)
    sets_split = {
        "train": (0, train_split),
        "dev": (train_split, dev_split),
        "test": (dev_split, df.shape[0]),
    }
    print(f"Split indices: {sets_split}")

    # Divide into X, y
    X = df["message"].tolist()
    y = df.drop(["message", "original", "genre"], axis=1).to_dict(orient="records")

    sets = {}
    for key, values in sets_split.items():
        i, j = values
        sets[key] = zip(X[i:j], y[i:j])

    return sets


def convert_record(nlp: spacy.Language, text: str, label: dict):
    """Convert a record from the tsv into a spaCy Doc object."""
    doc = nlp.make_doc(text)
    doc.cats = label
    return doc


def main(corpus_dir: Path = CORPUS_DIR):
    """Convert the Figure8 dataset to spaCy's binary format."""
    nlp = spacy.blank("en")
    sets = load_data()

    # Save divided sets in spaCy format
    for key, data in sets.items():
        docs = [convert_record(nlp, text, label) for text, label in data]
        out_file = corpus_dir / f"{key}.spacy"
        out_data = DocBin(docs=docs).to_bytes()
        with out_file.open("wb") as file_:
            file_.write(out_data)


if __name__ == "__main__":
    typer.run(main)
