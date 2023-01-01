import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer


class SentenceProcessor:

    def __init__(self):
        self.model = hub.load('/model')

    def transform(self, text: str) -> list:
        tensor = self.model(text)
        return tensor[0].numpy().tolist()
