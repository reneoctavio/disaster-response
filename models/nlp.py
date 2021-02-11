import re

from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer


def convert_nltk_to_wordnet_tag(tag: str):
    """Convert nltk POS tags to WordNet tags

    Adapted from
    https://simonhessner.de/lemmatize-whole-sentences-with-python-and-nltks-wordnetlemmatizer/

    Args:
        tag (str): The name of the tag
    Returns:
        A WordNet tag, or None

    """
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return None


def clean_text(text: str) -> str:
    """This function will tokenize, detect POS and
    lemmatize and remove stopword from a text

    Args:
        text (str): A text to be clean
    Returns:
        str: A cleaned text

    """
    lemmatizer = WordNetLemmatizer()

    # Tokenize a text and get POS tag
    tokenized = word_tokenize(text)
    tagged = pos_tag(tokenized)

    # Create tuples with token and converted tag
    converted_tagged = map(
        lambda token: (token[0], convert_nltk_to_wordnet_tag(token[1])), tagged
    )

    # Get lemmatized tokens
    text = [
        lemmatizer.lemmatize(token, tag) if tag else token
        for token, tag in converted_tagged
    ]

    # Remove stopwords
    text = " ".join(
        [lemma for lemma in text if lemma not in stopwords.words("english")]
    )

    # Lowercase, remove non-alphanumeric words
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = " ".join(text.split())

    return text
