import pandas as pd
import spacy

from pathlib import Path
from sqlalchemy import create_engine
from typing import Callable, Iterator

from spacy.training import Example
from spacy.language import Language


ASSETS_DIR = Path(__file__).parent.parent / "assets"


def load_data(
    assets_dir: Path = ASSETS_DIR, text_col_name: int = "message", split: float = 0.75
):
    """Load data from SQLite and split data into train, dev, and test"""
    path = (assets_dir / "fig8.db").resolve()
    engine = create_engine(f"sqlite:///{path}")
    df = pd.read_sql_table("dataset", engine)
    df = df.set_index("id")

    # Fill original NaNs from message column
    df["original"].fillna(df["message"], inplace=True)

    # Drop unused
    if text_col_name == "message":
        df = df.drop(["original", "genre"], axis=1)
    else:
        df = df.drop(["message", "genre"], axis=1)

    # Relabel related 2 to 0 (all of them have 0 to every other category)
    df.loc[df["related"] == 2, "related"] = 0

    # Drop if column is all ones or all zeros
    all_ones = df.loc[:, "related":].all()
    all_zeros = ~df.loc[:, "related":].any()
    cols_to_drop = df.loc[:, "related":].columns[all_ones | all_zeros].tolist()
    df = df.drop(cols_to_drop, axis=1)

    # Shuffle
    df = df.sample(frac=1, random_state=42)
    X = df[text_col_name].tolist()
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


def read_training_data():
    sets = load_data()
    training = sets["train"]

    rows = []
    for x, y in training:
        y["message"] = x
        rows.append(y)

    return pd.DataFrame(rows)


def sample_training(train_df, col_sample_sz=30):
    """Create batch sampling the same size for each label"""
    # Get target columns
    columns = set(train_df.columns)
    columns.remove("message")

    # Number of sample for positive and negative
    n_samples_pos = int(col_sample_sz / 2)
    n_samples_neg = col_sample_sz - n_samples_pos

    batch_indices = set()
    for col in columns:
        unused = ~train_df.index.isin(batch_indices)
        pos = train_df[(train_df[col] == 1) & unused].sample(n=n_samples_pos)
        neg = train_df[(train_df[col] == 0) & unused].sample(n=n_samples_neg)

        batch_indices.update(pos.index)
        batch_indices.update(neg.index)

    batch = train_df[train_df.index.isin(batch_indices)]
    texts = batch["message"].tolist()
    labels = batch.drop("message", axis=1).to_dict(orient="records")

    return zip(texts, labels)


@spacy.registry.readers("corpus_sampling.v1")
def stream_data() -> Callable[[Language], Iterator[Example]]:
    train_df = read_training_data()

    def generate_stream(nlp):
        for text, cats in sample_training(train_df):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, {"cats": cats})
            yield example

    return generate_stream
