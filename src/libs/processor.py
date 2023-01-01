import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import sklearn.metrics.pairwise as pwm
from tensorflow_text import SentencepieceTokenizer


class SentenceProcessor:

    def __init__(self):
        self.model = hub.load('/model')

    def transform(self, text: str) -> list:
        tensor = self.model(text)
        return tensor[0].numpy().tolist()

    def similarity(self, left_text: str, right_text: str) -> float:
        left_tensor = self.model(left_text)
        right_tensor = self.model(right_text)
        cs = pwm.cosine_similarity(left_tensor, right_tensor)
        result = 1 - np.arccos(cs) / np.pi
        return float(result[0][0])
