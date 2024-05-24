
# pip install requests
import random
import requests
from collections import defaultdict

# Define the Chatbot Responses
responses = defaultdict(list)

# Greetings
responses["greet"].extend([
    "Hello! How can I help you today?",
    "Hi there! What can I do for you?",
    "Greetings! How may I assist you?"
])

# Farewells
responses["goodbye"].extend([
    "Goodbye! Have a great day!",
    "See you later! Take care!",
    "Farewell! Hope to see you soon!"
])

# Default fallback
default_responses = [
    "I'm not sure how to respond to that.",
    "Can you please rephrase your question?",
    "Sorry, I didn't understand that."
]

# Define Intents using simple keyword matching
def get_intent(text):
    text = text.lower()
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "greet"
    elif any(word in text for word in ["bye", "goodbye", "see you", "later"]):
        return "goodbye"
    elif any(word in text for word in ["search", "find", "look for"]):
        return "search"
    return "default"

# Generate Responses
def generate_response(intent, query=None):
    if intent == "search" and query:
        return perform_search(query)
    elif intent in responses:
        return random.choice(responses[intent])
    else:
        return random.choice(default_responses)

# Perform a search using DuckDuckGo Instant Answer API
def perform_search(query):
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': query,
        'format': 'json',
        'no_html': 1,
        'skip_disambig': 1
    }
    response = requests.get(url, params=params)
    search_results = response.json()

    # Get the abstract or related topics
    if 'AbstractText' in search_results and search_results['AbstractText']:
        return search_results['AbstractText']
    elif 'RelatedTopics' in search_results and search_results['RelatedTopics']:
        results = search_results['RelatedTopics'][:3]
        return "\n".join([f"{result['Text']}: {result['FirstURL']}" for result in results if 'Text' in result and 'FirstURL' in result])
    else:
        return "Sorry, I couldn't find any results for your query."

# Main Chatbot Loop
def chatbot():
    print("Chatbot: Hello! I am a simple chatbot. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye! Have a great day!")
            break
        intent = get_intent(user_input)
        if intent == "search":
            query = user_input.lower().replace("search", "").strip()
            response = generate_response(intent, query)
        else:
            response = generate_response(intent)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()

