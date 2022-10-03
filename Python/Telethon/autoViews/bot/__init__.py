from telethon import TelegramClient
from config import vars

client = TelegramClient(
    session="bot",
    api_id=vars.api_id,
    api_hash=vars.api_hash
).start(bot_token=vars.bot_token)