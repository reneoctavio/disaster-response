import pandas as pd
import spacy

from flask import Flask
from sqlalchemy import create_engine

from download_model import download_model

# Load Model
try:
    model = spacy.load("model-best")
except OSError:
    download_model()
    model = spacy.load("model-best")

# Load Data
engine = create_engine("sqlite:///../data/DisasterResponse.db")
df = pd.read_sql_table("dataset", engine)

app = Flask(__name__, static_folder="react-app/", static_url_path="/")


@app.route("/")
def index():
    return app.send_static_file("index.html")


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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
