import os
import logging
import tinify
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve credentials from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TINIFY_API_KEY = os.getenv("TINIFY_API_KEY")

# Initialize Tinify API
tinify.key = TINIFY_API_KEY

# Create a Pyrogram client
app = Client("tinify_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Log the bot startup
logger.info("Bot is starting...")

# /start command
@app.on_message(filters.command("start"))
def start(client, message: Message):
    welcome_text = (
        "👋 Welcome to the Image Compressor Bot!\n"
        "I can help you compress images from a URL or by uploading a file.\n"
        "Just send me an image URL or upload an image file, and I'll do the rest! 📸"
    )
    client.send_message(message.chat.id, welcome_text)
    logger.info(f"Start command received from {message.from_user.id}.")

# /help command
@app.on_message(filters.command("help"))
def help_command(client, message: Message):
    help_text = (
        "💡 Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Show this help information\n"
        "Just send an image URL or upload an image file, and I'll compress it for you! "
    )
    client.send_message(message.chat.id, help_text)
    logger.info(f"Help command received from {message.from_user.id}.")

# Handle file uploads
@app.on_message(filters.document)
def handle_file(client, message: Message):
    logger.info(f"Received file upload from {message.from_user.id}.")
    # Notify the user about the received file
    client.send_message(message.chat.id, "📥 Received your file! I will download and compress it now.")
    
    file_path = client.download_media(message.document.file_id)
    compress_and_send_file(client, message.chat.id, file_path, message.document.file_name)

# Handle messages with an image URL
@app.on_message(filters.text)
def handle_url(client, message: Message):
    logger.info(f"Received image URL from {message.from_user.id}: {message.text}")
    # Notify the user about the received URL
    client.send_message(message.chat.id, "📥 Received your URL! I will download and compress the image now.")
    
    compress_and_send_url(client, message.chat.id, message.text)

def compress_and_send_file(client, chat_id, file_path, original_file_name):
    try:
        source = tinify.from_file(file_path)
        
        # Create a compressed filename
        base, ext = os.path.splitext(original_file_name)
        compressed_file_name = f"{base}_compressed{ext}"
        
        compressed_image_path = compressed_file_name  # Use the new file name
        source.to_file(compressed_image_path)

        # Send the compressed image back to the user as a document
        with open(compressed_image_path, "rb") as file:
            client.send_document(chat_id=chat_id, document=file)

        # Cleanup the compressed image file and the original file
        os.remove(compressed_image_path)
        os.remove(file_path)

        client.send_message(chat_id, "✅ Your image has been compressed and sent! You can download it now.")
        logger.info(f"Compressed image sent to {chat_id} successfully from file upload.")
        
    except Exception as e:
        client.send_message(chat_id, f"❌ An error occurred: {e}")
        logger.error(f"Error compressing file: {e}")

def compress_and_send_url(client, chat_id, image_url):
    try:
        source = tinify.from_url(image_url)
        
        # Create a compressed filename
        base = image_url.split("/")[-1]  # Get the last part of the URL
        ext = os.path.splitext(base)[-1]  # Extract the file extension
        compressed_file_name = f"{base}_compressed{ext}"
        
        compressed_image_path = compressed_file_name  # Use the new file name
        source.to_file(compressed_image_path)

        # Send the compressed image back to the user as a document
        with open(compressed_image_path, "rb") as file:
            client.send_document(chat_id=chat_id, document=file)

        # Cleanup the compressed image file
        os.remove(compressed_image_path)

        client.send_message(chat_id, "✅ Your image has been compressed and sent! You can download it now.")
        logger.info(f"Compressed image sent to {chat_id} successfully from URL.")
        
    except tinify.errors.AccountError:
        client.send_message(chat_id, "⚠️ The Tinify API key is invalid. Please check and try again.")
        logger.error("Invalid Tinify API key.")
    except tinify.errors.ClientError:
        client.send_message(chat_id, "⚠️ There was an issue with the image URL. Please ensure it's valid.")
        logger.error("Client error while processing the image URL.")
    except Exception as e:
        client.send_message(chat_id, f"❌ An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

# Run the bot
if __name__ == "__main__":
    app.run()
    logger.info("Bot has stopped.")
