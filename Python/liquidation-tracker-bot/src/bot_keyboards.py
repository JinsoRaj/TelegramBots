from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    kb = [
        [
            KeyboardButton(text="Binance Liquidations"),
            KeyboardButton(text="BYBIT Liquidations")
        ],
        [
            KeyboardButton(text="Settings"),
            KeyboardButton(text="Stop")
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def settings_keyboard():
    kb = [
        [
            KeyboardButton(text="Save Settings")
        ],
        [
            KeyboardButton(text="Liquidation Price"),
            KeyboardButton(text="Crypto Range")
        ],
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)