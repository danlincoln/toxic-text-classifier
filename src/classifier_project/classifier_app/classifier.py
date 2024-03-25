from django.conf import settings
import logging
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pandas.io.sql as psql
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import sqlalchemy
from typing import Self

logger = logging.getLogger("Classifier")

space = r"[-_+=/\\|]"
no_space = r"[!@#$%^&*(){}[\];:'\",.?`~]"


class Classifier(object):
    """ML Classifier: this stores the machine learning model, which is trained
    at app startup. Because training the model is expensive, it's only trained
    once and this object is stored as a singleton, which is retrieved any time
    new instances are requested.
    """

    _instance = None
    _pipeline = None

    def __new__(cls) -> Self:
        """Python singleton pattern"""
        if cls._instance is None:
            cls._instance = super(Classifier, cls).__new__(cls)
        return cls._instance

    def train_model(self):
        """Train the model. Connects to the classifier database to retrieve
        training data.
        """
        logger.info("Training classifier instance.")

        db = settings.DATABASES["default"]
        conn_str = (
            "postgresql+psycopg2://"
            "{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**db)
        )

        engine = sqlalchemy.create_engine(conn_str)

        query = (
            "SELECT t.processed as processed, hr.rating as rating "
            "FROM classifier_app_humanrating hr "
            "LEFT JOIN classifier_app_text t "
            "ON t.id = hr.text_id"
        )

        df = psql.read_sql(query, engine)

        train_X, train_y = df["processed"], df["rating"]

        pipeline = Pipeline(
            [
                (
                    "vect",
                    TfidfVectorizer(max_df=0.6, min_df=3, ngram_range=(1, 2)),
                ),
                ("chi2", SelectKBest(chi2, k=10000)),
                ("mnb", MultinomialNB(alpha=1e-06)),
            ]
        )
        pipeline.fit(train_X, train_y)
        self._pipeline = pipeline
        logger.info("Training complete.")

    def classify(self, text: str) -> tuple[bool, tuple[float, float]]:
        """Classify text.

        Args:
            text str: The text to classify.

        Returns:
            tuple[bool, tuple[float, float]]: A tuple containing the
            classification (boolean) and a tuple of floats (probability
            false, probability true).
        """
        logger.info(f"Classifying {text}")
        prediction = self._pipeline.predict([text])[0]
        probability = self._pipeline.predict_proba([text])[0]
        return prediction, probability


def pos_tags(words: list[str]) -> list[tuple[str, str]]:
    """Derive parts of speech for a list of words for use with
       WordNetLemmatizer.

       * Noun: n
       * Adjective: a
       * Verb: v
       * Adverb: r

       In the case of no match, it assumes the word is a noun (n).

    Args:
        words (list[str]): The list of words to find parts of speech for.

    Returns:
        list[tuple[str, str]]: Tuples of the form (word, part_of_speech).
    """
    result = []
    for word, pos in nltk.pos_tag(words):
        if pos[0] in ["N", "V", "R"]:
            pos = pos[0].lower()
        elif pos[0] == "J":
            # Stanford definition uses "J" for adjectives.
            pos = "a"
        else:
            pos = "n"
        result.append((word, pos))
    return result


def preprocess(text: str):
    """Given a string, return a list of lower_case, lemmatized words.

    Args:
        text (str): The raw string to process.

    Returns:
        list[str]: The list of lemmatized words.
    """
    wnl = WordNetLemmatizer()

    # Make sure we have a string
    result = str(text)

    # Lowercase
    result = result.lower()

    # Remove punctuation
    result = re.sub(space, " ", result)
    result = re.sub(no_space, "", result)

    # Remove leading/trailing spaces
    result = result.strip()

    # Split into a list for lemmatization
    result = word_tokenize(result)

    # Lemmatize each word
    result = [wnl.lemmatize(w, pos=p) for w, p in pos_tags(result)]

    return " ".join(result)
