from agents.basic_agent import Agent

def main():
    agent = Agent("data/intents.json")
    print("Agent system activated. Type 'exit' to end session.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = agent.process_input(user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()