import json
import random
import logging
from pathlib import Path
from typing import Dict, List, Optional
from handlers.input_processor import InputProcessor
from handlers.response_handler import ResponseHandler
from response_handler.surprise_generator import SurpriseGenerator  # Import SurpriseGenerator

class Agent:
    def __init__(self, intents_path: str, handler_type: str = "exact_match"):
        self.intents = self._load_intents(intents_path)
        self.input_processor = InputProcessor()
        self.response_handler = ResponseHandler.create_handler(handler_type)
        self.logger = logging.getLogger(__name__)
        
    def _load_intents(self, path: str) -> Dict:
        try:
            with open(Path(__file__).parent.parent / path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading intents: {str(e)}")
            return {"intents": []}

    def process_input(self, user_input: str) -> Optional[str]:
        try:
            if not user_input.strip():
                return None
                
            processed_input = self.input_processor.normalize(user_input)
            return self.response_handler.get_response(
                processed_input, 
                self.intents["intents"]
            )
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")
            return "Sorry, I encountered an error processing your request."

    def run_cli(self):
        print("Agent started. Type 'exit' to end.")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break
                response = self.process_input(user_input)
                print(f"Agent: {response}")
            except KeyboardInterrupt:
                break


class AdvancedAgent:
    def __init__(self, config):
        self.memory = ConversationMemory()
        self.nlp = NLPProcessor()
        self.matcher = SemanticMatcher()
        self.response_gen = SmartResponseGenerator(self.memory)
        self.knowledge = KnowledgeEngine(config["wolfram_key"])
        self.weather = WeatherAssistant(config["weather_key"])
        
    def process_input(self, user_input: str):
        # Analyze input
        analysis = self.nlp.process_text(user_input)
        
        # Context-aware matching
        context = self.memory.get_recent_context()
        full_text = f"{context}\n{user_input}"
        
        # Get best match using semantic similarity
        intent, confidence = self._match_intent(full_text)
        
        # Generate response
        if confidence < 0.4:
            return self._handle_unknown_input(user_input)
            
        response = self.response_gen.generate_response(intent, analysis["entities"])
        
        # Add surprise with 10% probability
        if random.random() < 0.1:
            response += f"\n{SurpriseGenerator.unexpected_response()[1]}"
            
        self.memory.add_interaction(user_input, response)
        return response