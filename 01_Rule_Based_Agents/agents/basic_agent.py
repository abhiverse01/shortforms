import json
import random
import logging
from pathlib import Path
from typing import Dict, List, Optional
from handlers.input_processor import InputProcessor
from handlers.response_handler import ResponseHandler

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