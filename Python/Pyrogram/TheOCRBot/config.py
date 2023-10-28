# (c) HYBRID
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'hybrid')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OWNER = int(os.environ.get('OWNER', 1412909688))
BIN_CHANNEL = int(os.environ.get('BIN_CHANNEL', 0))
OCR_SPACE_API_KEY = os.environ.get('OCR_SPACE_API_KEY')
UPDATES_CHANNEL = os.environ.get('UPDATES_CHANNEL')
