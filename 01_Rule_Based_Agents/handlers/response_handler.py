from abc import ABC, abstractmethod
import random
import re
import json

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
    



class SmartResponseGenerator:
    def __init__(self, memory):
        self.memory = memory
        self.response_templates = self._load_templates()

    def _load_templates(self):
        return {
            "greeting": [
                "Hello! {context} How can I help you today?",
                "Hi there! {context} What would you like to discuss?"
            ],
            "follow_up": [
                "Continuing from our previous talk about {topic}, {response}",
                "Since you mentioned {topic}, {response}"
            ]
        }

    def generate_response(self, intent: str, entities: list) -> str:
        template = random.choice(self.response_templates.get(intent, ["{response}"]))
        context = self.memory.get_recent_context()
        
        replacements = {
            "{context}": f"I see you're back. " if context else "",
            "{topic}": entities[0] if entities else "our conversation",
            "{response}": random.choice(intent["responses"])
        }

        return template.format(**replacements)


class SurpriseGenerator:
    @staticmethod
    def unexpected_response():
        surprises = [
            ("fact", "Did you know? The first computer virus was created in 1983!"),
            ("joke", "Why don't scientists trust atoms? Because they make up everything!"),
            ("quote", random.choice(famous_quotes)),
            ("riddle", "I speak without a mouth. What am I? (Answer: An echo)")
        ]
        return random.choice(surprises)