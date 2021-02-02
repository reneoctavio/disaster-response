from pathlib import Path
import typer
from spacy.tokens import DocBin
import spacy
import math

from sqlalchemy import create_engine
import pandas as pd

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"


def load_data():
    path = (ASSETS_DIR / "fig8.db").resolve()
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

    for text, label in zip(X, y):
        yield text, label


def convert_record(nlp, text, label):
    """Convert a record from the tsv into a spaCy Doc object."""
    doc = nlp.make_doc(text)
    doc.cats = label
    return doc


def main(corpus_dir: Path = CORPUS_DIR, lang: str = "en", split: float = 0.75):
    """Convert the Figure8 dataset to spaCy's binary format."""
    nlp = spacy.blank(lang)
    docs = [convert_record(nlp, text, label) for text, label in load_data()]

    # Split dataset
    train_split = int(split * len(docs))
    dev_split = train_split + int((len(docs) - train_split) / 2)
    sets = {
        "train": (0, train_split),
        "dev": (train_split, dev_split),
        "test": (dev_split, len(docs)),
    }
    print(sets)

    # Save divided sets in spaCy format
    for key, values in sets.items():
        i, j = values
        out_file = corpus_dir / f"{key}.spacy"
        out_data = DocBin(docs=docs[i:j]).to_bytes()
        with out_file.open("wb") as file_:
            file_.write(out_data)


if __name__ == "__main__":
    typer.run(main)
