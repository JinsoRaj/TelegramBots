import requests
from pyrogram import Client, filters
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API ID, API Hash, and Bot Token from the environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Initialize the bot with the token, API ID, and API Hash
app = Client("joke_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Command handler for /start
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Hello! I am a Joke Bot 🤖. Use /joke to get a random joke, or /help for more options.")

# Command handler for /help
@app.on_message(filters.command("help"))
def help_command(client, message):
    message.reply_text("Available Commands:\n"
                       "/start - Start the bot\n"
                       "/joke - Get a random joke\n"
                       "/help - Show this help message")

# Command handler for /joke
@app.on_message(filters.command("joke"))
def joke_command(client, message):
    # Fetch a joke from JokeAPI
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    
    if response.status_code == 200:
        joke_data = response.json()
        if not joke_data.get("error"):
            # Create the joke text formatted as a code block
            if joke_data.get("type") == "single":
                joke_text = f"```\n{joke_data.get('joke')}\n```"
            else:
                setup = joke_data.get("setup")
                delivery = joke_data.get("delivery")
                joke_text = f"```\n{setup}\n{delivery}\n```"
            
            # Create a response message with the rest of the fields
            details = (
                f"Category: {joke_data.get('category')}\n"
                f"Type: {joke_data.get('type')}\n"
                f"ID: {joke_data.get('id')}\n"
                f"Safe: {joke_data.get('safe')}\n"
                f"Language: {joke_data.get('lang')}\n"
                f"Flags: {', '.join([flag for flag, value in joke_data.get('flags', {}).items() if value]) or 'None'}"
            )
            
            # Combine the joke and the details
            response_message = f"{joke_text}\n{details}"
            
            # Send the combined response
            message.reply_text(response_message)
        else:
            message.reply_text("Failed to fetch a joke. Please try again.")
    else:
        message.reply_text("Sorry, I couldn't fetch a joke at the moment. Please try again later!")

# Start the bot
if __name__ == "__main__":
    app.run()
