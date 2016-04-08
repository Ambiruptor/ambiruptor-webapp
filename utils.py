import json
import re


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
