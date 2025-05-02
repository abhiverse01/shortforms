import spacy
from spacy.lang.en.stop_words import STOP_WORDS

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def process_text(self, text: str):
        doc = self.nlp(text)
        return {
            "lemmas": [token.lemma_ for token in doc],
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "intent_keywords": [
                token.lemma_ for token in doc 
                if not token.is_stop and token.is_alpha
            ],
            "sentiment": doc.sentiment
        }