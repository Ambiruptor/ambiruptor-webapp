import json
import re
import pickle
import ambiruptor.library.preprocessors.feature_extractors as fe
from ambiruptor.library.preprocessors.tokenizers import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np


def format_correction_corpus(text, disamb, correct_indices):
    ambiguous_words = []

    json_disamb = json.loads(disamb)["disamb"]

    for d in json_disamb:
        ambiguous_words.append(text[d["begin"]:d["end"]])

    tokenizer = re.compile(r"\W+", re.UNICODE)
    tokens = tokenizer.split(text)

    for i, token in enumerate(tokens):
        if token in ambiguous_words:
            index = ambiguous_words.index(token)
            tokens[i] = (token, json_disamb[index]["all_senses"][correct_indices[index]])

    return tokens

def disambiguation(text):
    with open("models/ambiguous_words.txt", "r") as words_f:
        ambiguous_words = []
        for line in words_f.readlines():
            word = line
            ambiguous_words.append(word)
            word_sense = re.findall("(.+)_.+", word.lower())[0]
            print("Loading feature extractor...")
            close_words_extractor = fe.CloseWordsFeatureExtractor()
            close_words_extractor.load("models/feature_extraction/Bar_(disambiguation).dump")
            words = np.array(word_tokenize(text))
            wordnet_lemmatizer = WordNetLemmatizer()
            lemmatized = [wordnet_lemmatizer.lemmatize(word) for word in words]
            print(close_words_extractor.extract_features(lemmatized, word_sense))



def format_disambiguation(disamb):
    pass
