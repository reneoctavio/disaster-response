import pandas as pd
import spacy
import requests
import zipfile

from flask import Flask

from sqlalchemy import create_engine

DOWNLOAD_LINK = (
    "https://api.onedrive.com/v1.0/shares/u!"
    + "aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBalpDaVlrY2twdF9oWXg4UF8zUEFoeG1udjNtdEE"
    + "/root/content"
)


def download_model():
    """Download trained spaCy model"""
    with requests.get(DOWNLOAD_LINK, stream=True) as r:
        r.raise_for_status()
        with open("model-best.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile("model-best.zip", "r") as f:
        f.extractall()


# Load Model
try:
    model = spacy.load("model-best")
except OSError:
    download_model()
    model = spacy.load("model-best")

# Load Data
engine = create_engine("sqlite:///../data/DisasterResponse.db")
df = pd.read_sql_table("dataset", engine)

app = Flask(__name__)


@app.route("/api/genre_counts")
def genre_counts():
    genre_counts = df.groupby("genre").count()["message"]
    genre_names = list(genre_counts.index)

    return {"genre_names": genre_names, "genre_counts": genre_counts.to_list()}


@app.route("/api/labels_count")
def labels_count():
    labels_count = df.loc[:, "related":].sum().sort_values(ascending=False)
    labels_name = list(labels_count.index)
    labels_name = [n.replace("_", " ").title() for n in labels_name]

    return {"labels_name": labels_name, "labels_count": labels_count.to_list()}


@app.route("/api/predict/<query>")
def predict(query):
    # Predict
    doc = model(query)
    results = pd.Series(doc.cats).sort_values(ascending=False)

    return {"results": list(zip(results.index, results))}


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    app.run()
