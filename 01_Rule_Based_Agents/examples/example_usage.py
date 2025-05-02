from agents.basic_agent import Agent

if __name__ == "__main__":
    agent = Agent("data/intents.json", handler_type="exact_match")
    agent.run_cli()


    