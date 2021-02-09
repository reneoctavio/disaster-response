import json
import plotly
import pandas as pd
import spacy
import requests
import zipfile

from flask import Flask
from flask import render_template, request
from plotly.graph_objs import Bar

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


# index webpage displays cool visuals and receives user input text for model
@app.route("/")
def index():

    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby("genre").count()["message"]
    genre_names = list(genre_counts.index)

    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            "data": [Bar(x=genre_names, y=genre_counts)],
            "layout": {
                "title": "Distribution of Message Genres",
                "yaxis": {"title": "Count"},
                "xaxis": {"title": "Genre"},
            },
        }
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template("master.html", ids=ids, graphJSON=graphJSON)


@app.route("/go")
def go():
    # save user input in query
    query = request.args.get("query", "")

    # predict
    doc = model(query)
    classification_results = (pd.Series(doc.cats) >= 0.5).to_dict()

    # This will render the go.html Please see that file.
    return render_template(
        "go.html", query=query, classification_result=classification_results
    )


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    app.run()
