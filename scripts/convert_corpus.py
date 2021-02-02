from pathlib import Path
import typer
from spacy.tokens import DocBin
import spacy
import math

from sqlalchemy import create_engine
import pandas as pd

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"


def load_data(assets_dir: Path = ASSETS_DIR, split: float = 0.75):
    """Load data from SQLite and split data into train, dev, and test"""
    path = (assets_dir / "fig8.db").resolve()
    engine = create_engine(f"sqlite:///{path}")
    df = pd.read_sql_table("dataset", engine)
    df = df.set_index("id")

    # Drop unused
    df = df.drop(["original", "genre"], axis=1)

    # Relabel related 2 to 0 (all of them have 0 to every other category)
    df.loc[df["related"] == 2, "related"] = 0

    # Drop if column is all ones or all zeros
    all_ones = df.loc[:, "related":].all()
    all_zeros = ~df.loc[:, "related":].any()
    cols_to_drop = df.loc[:, "related":].columns[all_ones | all_zeros].tolist()
    df = df.drop(cols_to_drop, axis=1)

    # Shuffle
    df = df.sample(frac=1, random_state=42)
    X = df["message"].tolist()
    y = df.loc[:, "related":].to_dict(orient="records")

    # Split dataset
    train_split = int(split * df.shape[0])
    dev_split = train_split + int((df.shape[0] - train_split) / 2)
    sets_split = {
        "train": (0, train_split),
        "dev": (train_split, dev_split),
        "test": (dev_split, df.shape[0]),
    }
    print(f"Split indices: {sets_split}")

    sets = {}
    for key, values in sets_split.items():
        i, j = values
        sets[key] = zip(X[i:j], y[i:j])

    return sets


def convert_record(nlp, text, label):
    """Convert a record from the tsv into a spaCy Doc object."""
    doc = nlp.make_doc(text)
    doc.cats = label
    return doc


def main(corpus_dir: Path = CORPUS_DIR, lang: str = "en"):
    """Convert the Figure8 dataset to spaCy's binary format."""
    nlp = spacy.blank(lang)
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
