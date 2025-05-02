from abc import ABC, abstractmethod
import random
import re

class BaseHandler(ABC):
    @abstractmethod
    def get_response(self, input_text: str, intents: list) -> str:
        pass

class ExactMatchHandler(BaseHandler):
    def get_response(self, input_text: str, intents: list) -> str:
        for intent in intents:
            for pattern in intent["patterns"]:
                if pattern in input_text:
                    return random.choice(intent["responses"])
        return "I'm not sure how to answer that. Can you rephrase?"

class RegexHandler(BaseHandler):
    def get_response(self, input_text: str, intents: list) -> str:
        for intent in intents:
            for pattern in intent["patterns"]:
                if re.search(pattern, input_text):
                    return random.choice(intent["responses"])
        return "I'm not sure how to answer that. Can you rephrase?"

class ResponseHandler:
    @staticmethod
    def create_handler(handler_type: str) -> BaseHandler:
        handlers = {
            "exact_match": ExactMatchHandler,
            "regex": RegexHandler
        }
        return handlers.get(handler_type, ExactMatchHandler)()