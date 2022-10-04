import os
import importlib

for view in [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if f.endswith(".py") and f != "__init__.py"]:
    importlib.import_module(f"TelegramBot.plugins.{view[:-3]}") 
