"""
cli_chat.py - Command Line Interface for StockPulse AI
Allows running the stock-domain chatbot directly in the terminal.
"""

import os
import sys
from dotenv import load_dotenv
from stock_agent import StockChatbot

load_dotenv()

def main():
    print("=" * 65)
    print(" 📈 StockPulse AI - Stock Market Domain Chatbot (CLI)")
    print(" [Domain Guardrail]: ONLY Stock Market queries are answered.")
    print(" Type 'exit' or 'quit' to end the session.")
    print("=" * 65)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API Key (or press Enter if set in .env): ").strip()

    if not api_key:
        print("\n❌ Error: OpenAI API Key is required to run the chatbot.")
        print("Please set OPENAI_API_KEY in your .env file or enter it at prompt.\n")
        sys.exit(1)

    chatbot = StockChatbot(api_key=api_key, model="gpt-4o-mini", temperature=0.2)
    conversation_history = []

    print("\n✅ StockPulse AI ready! Ask your stock market questions below:\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                print("\nGoodbye! Happy investing. 📊\n")
                break

            conversation_history.append({"role": "user", "content": user_input})
            print("\nStockPulse AI: ", end="", flush=True)

            response_text = ""
            for token in chatbot.get_response_stream(conversation_history):
                print(token, end="", flush=True)
                response_text += token
            print("\n")

            conversation_history.append({"role": "assistant", "content": response_text})

        except KeyboardInterrupt:
            print("\n\nSession terminated by user.")
            break
        except Exception as e:
            print(f"\n[Error]: {e}\n")

if __name__ == "__main__":
    main()
