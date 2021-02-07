import joblib
import spacy
import sys

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from nlp import load_spacy_model, lemmatize
from sqlalchemy import create_engine
from typing import Tuple


def load_data(database_file: str) -> Tuple[list, pd.DataFrame, list]:
    """Load data from a SQLite database"""
    engine = create_engine(f"sqlite:///{database_file}")
    df = pd.read_sql_table("dataset", engine).set_index("id")

    # Randomize
    df = df.sample(frac=1, random_state=42)

    # Divide into X, y
    X = df["message"].tolist()
    y = df.drop(["message", "original", "genre"], axis=1)

    return X, y, y.columns.tolist()


def build_model() -> GridSearchCV:
    """Build a model

    The data will pass through a tf-idf Vectorizer
    and a Random Forest Classifier

    Because of class imbalance, we set class_weight to
    balanced to give more weight to underrepresented
    classes

    We do a grid search choosing number of estimators
    and a min samples split for Random Forest.

    """

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("clf", RandomForestClassifier(class_weight="balanced")),
        ]
    )

    parameters = {
        "tfidf__max_df": [0.5, 1.0],
        "clf__n_estimators": [10, 100],
    }

    return GridSearchCV(pipeline, parameters)


def evaluate_model(
    model: GridSearchCV, X_test: list, y_test: pd.DataFrame, category_names: list,
):
    """Evaluate the model, printing Precision, Recall and F1 scores"""
    y_pred = model.predict(X_test)
    print(
        classification_report(
            y_test, y_pred, target_names=category_names, zero_division=0
        )
    )


def save_model(model: GridSearchCV, model_file: str):
    """Save model to a file"""
    joblib.dump(model.best_estimator_, model_file, compress=1)


def main():
    if len(sys.argv) == 3:
        # pylint: disable=unbalanced-tuple-unpacking
        database_file, model_file = sys.argv[1:]

        print("Loading data...\n    DATABASE: {}".format(database_file))
        X, Y, category_names = load_data(database_file)

        print("Lemmatizing texts...")
        nlp = load_spacy_model()
        X = lemmatize(X, nlp)

        # Split training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

        print("Building model...")
        model = build_model()

        print("Training model...")
        model.fit(X_train, y_train)

        print("Evaluating model...")
        evaluate_model(model, X_test, y_test, category_names)

        print("Saving model...\n    MODEL: {}".format(model_file))
        save_model(model, model_file)

        print("Trained model saved!")

    else:
        print(
            "Please provide the filepath of the disaster messages database "
            "as the first argument and the filepath of the pickle file to "
            "save the model to as the second argument. \n\nExample: python "
            "train_classifier.py ../data/DisasterResponse.db classifier.pkl"
        )


if __name__ == "__main__":
    main()
