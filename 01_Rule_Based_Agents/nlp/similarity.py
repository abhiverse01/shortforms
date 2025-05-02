# This is a semantic matcher that uses TF-IDF and cosine similarity to find the best match for a given input text from a list of candidate patterns.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List

class SemanticMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def train(self, patterns: List[str]):
        self.vectorizer.fit(patterns)

    def get_best_match(self, input_text: str, candidates: List[str]) -> tuple:
        input_vec = self.vectorizer.transform([input_text])
        candidate_vecs = self.vectorizer.transform(candidates)
        similarities = cosine_similarity(input_vec, candidate_vecs)
        max_index = np.argmax(similarities)
        return candidates[max_index], similarities[0][max_index]