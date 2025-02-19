from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pandas as pd
import random

# Load CSV file
df = pd.read_csv("quotes.csv")

# Initialize the chatbot
chatbot = ChatBot("QuoteBot")
trainer = ListTrainer(chatbot)

# Train the bot using quotes
for index, row in df.iterrows():
    tags = str(row['tags']).split(',') if pd.notna(row['tags']) else []  # Handle NaN values
    for tag in tags:
        trainer.train([
            f"Tell me a quote about {tag.strip()}",
            f"{row['text']} - {row['author']}"
        ])
    
    trainer.train([
        f"Give me a quote by {row['author']}",
        f"{row['text']} - {row['author']}"
    ])

# Small talk dictionary
small_talk = {
    "hi": "Hello! How can I help you?",
    "hello": "Hey there! Need a quote?",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "what's your name": "I'm QuoteBot! I can share famous quotes with you.",
    "tell me a joke": "I'm better at quotes, but here's one: Why don't scientists trust atoms? Because they make up everything!",
    "goodbye": "Bye! Have an inspiring day!",
    "thank you": "You're welcome! Keep seeking wisdom."
}

# Train chatbot with small talk responses
for q, a in small_talk.items():
    trainer.train([q, a])

# Function to process user input
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Check for small talk first
    for phrase, response in small_talk.items():
        if phrase in user_input:
            return response

    # Check for author request
    for author in df["author"].dropna().unique():
        if author.lower() in user_input:
            quotes = df[df["author"].str.lower() == author.lower()]["text"].dropna().tolist()
            return f"{random.choice(quotes)} - {author}" if quotes else "I couldn't find a quote by that author."

    # Check for topic request
    for tag in df["tags"].dropna().str.split(",").explode().unique():
        if tag and tag.lower().strip() in user_input:
            quotes = df[df["tags"].str.contains(tag, case=False, na=False)]["text"].dropna().tolist()
            return f"{random.choice(quotes)}" if quotes else "I couldn't find a quote on that topic."

    # Default to chatbot response
    return chatbot.get_response(user_input)

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("ChatBot: Goodbye! Have a great day! 😊")
        break
    response = get_response(user_input)
    print("ChatBot:", response)
