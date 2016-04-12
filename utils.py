import json
import re
import pickle
import os.path

import numpy as np
import ambiruptor.library.preprocessors.feature_extractors as fe

from ambiruptor.library.preprocessors.tokenizers import word_tokenize



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


def predictor(datadir, text):    
    # List of ambiguous words
    filename_ambiguouswords = datadir + "/ambiguous_words.txt"
    with open(filename_ambiguouswords, 'r') as f:
        ambiguous_words = {x.rstrip() for x in f.readlines()}
        if "" in ambiguous_words:
            ambiguous_words.remove("")

    # Word tokenize
    results = []
    words = np.array(word_tokenize(text.lower()))

    # Disambiguation
    for w in ambiguous_words:

        # Ambiguous word
        ambiguous_word = re.match(r"[^_]+", w).group(0).lower()

        # Feature extraction
        filename_features = datadir + "/feature_extractors/" + w + ".dump"
        if not os.path.isfile(filename_features):
            continue
        with open(filename_features, "rb") as f:
            ambiguous_extractor = pickle.load(f)

        ambiguous_data = ambiguous_extractor.extract_features(words, ambiguous_word)

        if ambiguous_data.data.shape[0] == 0:
            continue

        # Model prediction
        filename_models = datadir + "/models/" + w + ".dump"
        if not os.path.isfile(filename_models):
            continue

        with open(filename_models, "rb") as f:
            model = pickle.load(f)
            predictions = model.predict_classes(ambiguous_data)
            for index, meaning in zip(ambiguous_data.targets, predictions):
                result = dict()
                result["begin"] = sum([len(words[i]) for i in range(index)])
                result["end"] = result["begin"] + len(words[index])
                result["all_senses"] = model.lb.inverse_transform(model.model.classes_).tolist()
                result["sense_index"] = result["all_senses"].index(meaning)
                result["url"] = "https://en.wikipedia.org/wiki/%s" % meaning
                results.append(result)

    # Return results
    return results



def disambiguation(text):
    return json.dumps(predictor("data/", text))
