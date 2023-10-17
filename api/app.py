import re
from io import StringIO
from pathlib import Path

import joblib
import sklearn
import unicodedata
import numpy as np
import pandas as pd
import demoji
from functools import partial
from flashtext import KeywordProcessor

HASHTAG = 'hashtag'

aspects = ["FOOD#PRICES",
           "FOOD#QUALITY",
           "FOOD#STYLE&OPTIONS",
           "DRINKS#PRICES",
           "DRINKS#QUALITY",
           "DRINKS#STYLE&OPTIONS",
           "RESTAURANT#PRICES",
           "RESTAURANT#GENERAL",
           "RESTAURANT#MISCELLANEOUS",
           "SERVICE#GENERAL",
           "AMBIENCE#GENERAL",
           "LOCATION#GENERAL"]

sentiments_mapping = {1: 'negative', 2: "neutral", 3: "positive"}


pipeline_fp = Path('api/pipe.joblib')

full_pipeline = joblib.load(pipeline_fp)

def classify_sentence(sentence):
    return full_pipeline.predict([sentence])[0].astype(np.uint)

def remove_emojis(text):
    return demoji.replace(text, '')

def SentimentAnalysis(inputText: str):
    classes = classify_sentence(inputText)
    results = []
    for index, aspect in enumerate(classes):
        if aspect:
            result = f"{aspects[index]}: {sentiments_mapping[aspect]}"
            results.append(result)
    return results
