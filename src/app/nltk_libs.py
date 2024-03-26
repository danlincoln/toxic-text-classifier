# This script downloads and installs the Natural Language Toolkit libraries
# that the text preprocessor requires. It is run during app startup.

import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
