import os
import re
import spacy


class NLPTransformer:
    """This class will transform text into tokenized forms

    The text will go through a pipeline in a spaCy model
    where it will be tokenized, have their POS determined,
    and lemmatized.

    After lemmatization, it will be through more cleaning.
    It will have stop words removed, we will lower case the text,
    and remove all non-alphanumeric tokens.

    Attributes:
        nlp (spacy.Language): A spaCy language model

    """

    def __init__(self):
        spacy.prefer_gpu()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Download resources
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def cleaning(self, doc: spacy.tokens.Doc) -> str:
        """Clean a Doc processed by a spaCy model."""
        text = " ".join([token.lemma_ for token in doc if not token.is_stop])
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = " ".join(text.split())
        return text

    def transform(self, texts: list, **transform_params) -> list:
        """The transform method of sklearn Transform classes.

        It will take a list of texts, and clean them for further
        vectorization.

        Args:
            texts (list): A list of texts
        """
        transformed_texts = []

        for doc in self.nlp.pipe(texts, disable=["parser", "ner"]):
            transformed_texts.append(self.cleaning(doc))

        return transformed_texts

    def fit(self, X, y=None, **fit_params):
        return self
