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
from sklearn.base import BaseEstimator, TransformerMixin

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

class TextCleanerBase(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()

        # Create preprocessing function
        self.normalize_unicode = partial(unicodedata.normalize, 'NFC')
            
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not isinstance(X, pd.Series):
            X = pd.Series(X)

        return X.apply(str.lower) \
                .apply(remove_emojis) \
                .apply(self.normalize_unicode)

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
