import pytest
from agents.basic_agent import Agent

@pytest.fixture
def test_agent():
    return Agent("data/intents.json")

def test_loading_intents(test_agent):
    assert len(test_agent.intents["intents"]) > 0

def test_greeting_response(test_agent):
    response = test_agent.process_input("Hi there!")
    assert response in ["Hello!", "Hi there!", "Hey!"]

def test_unknown_input(test_agent):
    assert "rephrase" in test_agent.process_input("asdfghjkl")

def test_empty_input(test_agent):
    assert test_agent.process_input("   ") is None