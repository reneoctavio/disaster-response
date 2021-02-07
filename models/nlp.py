import os
import re
import spacy

from typing import List


def load_spacy_model():
    """Load a spaCy model, if does not exist download"""
    spacy.prefer_gpu()
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Download resources
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    return nlp


def lemmatize(texts: list, nlp: spacy.Language) -> List[spacy.tokens.Doc]:
    """This function will tokenize, detect POS and
    lemmatize each text in a list

    Args:
        texts (list): A list of texts
    Returns:
        list: A list of spaCy Docs

    """

    return [clean_text(doc) for doc in nlp.pipe(texts, disable=["parser", "ner"])]


def clean_text(doc: spacy.tokens.Doc) -> str:
    """Clean a Doc processed by a spaCy model.

    Remove stopwords, lowercase text, remove non-alphanumeric words

    Args:
        doc (spacy.tokens.Doc): A spaCy docs after lemmatization
    Returns:
        str: A cleaned text

    """
    text = " ".join([token.lemma_ for token in doc if not token.is_stop])
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = " ".join(text.split())
    return text
