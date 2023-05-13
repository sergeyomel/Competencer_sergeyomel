from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from pymystem3 import Mystem

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def lowercase(input: str) -> str:
    """
    Returns lowercase text
    """
    return input.lower()


def remove_punctuation(input: str) -> str:
    """
    Returns text without punctuation
    """
    return input.translate(str.maketrans('', '', string.punctuation))


def remove_whitespaces(input: str) -> str:
    """
    Returns text without extra whitespaces
    """
    return " ".join(input.split())


def remove_html_tags(input: str) -> str:
    """
    Returns text without HTML tags
    """
    soup = BeautifulSoup(input, "html.parser")
    stripped_input = soup.get_text(separator=" ")
    return stripped_input


def tokenize(input: str) -> str:
    """
    Returns tokenized version of text
    """
    return word_tokenize(input)


def remove_stop_words(input: str) -> str:
    """
    Returns text without stop words
    """
    stopwords_eng_ru = stopwords.words('english') + stopwords.words('russian')
    return ' '.join([word for word in input.split() if word not in stopwords_eng_ru])


def lemmatize(input: str) -> str:
    """
    Lemmatizes input using NLTK's WordNetLemmatizer
    """
    lemmatizer = WordNetLemmatizer()
    input_str = word_tokenize(input)
    new_words = []
    for word in input_str:
        new_words.append(lemmatizer.lemmatize(word))
    return ' '.join(new_words)


def stem(input: str) -> str:
    """
    Stem input using PyMyStem
    """
    stemmer = Mystem()
    return ' '.join(stemmer.lemmatize(input))


def stem_or_lemmatize(input: str) -> str:
    """
    Use stemming if the first symbol in name is russian, otherwise use lemmatize
    """
    if input[0].isascii():
        return lemmatize(input)
    else:
        return stem(input)

# Example of usage

# import pandas as pd

# words = pd.Series(['мама?        мыла, раму', 'NO WAY!(', 'without mercy secondary masters we did it by laying down'])
# words = words.apply(lowercase)\
#    .apply(remove_punctuation)\
#    .apply(remove_whitespaces)\
#    .apply(remove_stop_words)\
#    .apply(stem_or_lemmatize)\
#    .apply(tokenize)
