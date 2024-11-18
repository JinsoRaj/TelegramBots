from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    """
    Generate the main menu keyboard for the Telegram bot.

    Returns:
        ReplyKeyboardMarkup: A keyboard with options for Binance, BYBIT, settings, and stop.
    """
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
    """
    Generate the settings menu keyboard for the Telegram bot.

    Returns:
        ReplyKeyboardMarkup: A keyboard with options to save settings, set liquidation price, and crypto range.
    """
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

def binance_liquidations_keyboard_tracking():
    """
    Generate the Binance liquidations menu keyboard when tracking is active.

    Returns:
        ReplyKeyboardMarkup: A keyboard with options to stop tracking and go back.
    """
    kb = [
        [
            KeyboardButton(text="Stop Tracking"),
            KeyboardButton(text="Back")
        ]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def binance_liquidations_keyboard_not_tracking():
    """
    Generate the Binance liquidations menu keyboard when tracking is not active.

    Returns:
        ReplyKeyboardMarkup: A keyboard with options to start tracking and go back.
    """
    kb = [
        [
            KeyboardButton(text="Start Tracking"),
            KeyboardButton(text="Back")
        ]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
