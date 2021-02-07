from pathlib import Path
import typer
from spacy.tokens import DocBin
import spacy
import math

from functions import load_data

CORPUS_DIR = Path(__file__).parent.parent / "corpus"


def convert_record(nlp, text, label):
    """Convert a record from the tsv into a spaCy Doc object."""
    doc = nlp.make_doc(text)
    doc.cats = label
    return doc


def main(corpus_dir: Path = CORPUS_DIR):
    """Convert the Figure8 dataset to spaCy's binary format."""
    for text_col_name, lang in [("message", "en"), ("original", "xx")]:
        nlp = spacy.blank(lang)
        sets = load_data(text_col_name=text_col_name)

        # Save divided sets in spaCy format
        for key, data in sets.items():
            docs = [convert_record(nlp, text, label) for text, label in data]
            out_file = corpus_dir / f"{key}.{text_col_name}.spacy"
            out_data = DocBin(docs=docs).to_bytes()
            with out_file.open("wb") as file_:
                file_.write(out_data)


if __name__ == "__main__":
    typer.run(main)
