import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message
from methods import on_message_binance
from bot import (
    command_start_handler,
    settings_handler,
    ask_liquidation_price,
    set_liquidation_price,
    start_tracking_handler,
    stop_tracking_handler,
    active_trackers,
    user_liquidation_prices,
)


class TestBotHandlers(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Create a mock message object with nested attributes
        self.message = AsyncMock(spec=Message)
        self.message.chat = MagicMock()
        self.message.chat.id = 12345
        self.message.text = "Some text"
        self.message.from_user = MagicMock()
        self.message.from_user.id = 12345
        self.message.from_user.full_name = "Test User"

        # Mock the answer method explicitly as AsyncMock
        self.message.answer = AsyncMock()

        # Mock state for FSMContext
        self.state = MagicMock()
        self.state.set_state = AsyncMock()
        self.state.clear = AsyncMock()

    @patch("bot.bk.main_keyboard")
    async def test_command_start_handler(self, mock_main_keyboard):
        # Mock keyboard
        mock_main_keyboard.return_value = "Mock Keyboard"

        # Call the handler
        await command_start_handler(self.message)

        # Assertions
        self.message.answer.assert_awaited_with(
            f"Hi, {self.message.from_user.full_name}! I'm a Liquidation Notifier Bot.",
            reply_markup="Mock Keyboard",
        )

    @patch("bot.bk.settings_keyboard")
    async def test_settings_handler(self, mock_settings_keyboard):
        # Mock keyboard
        mock_settings_keyboard.return_value = "Mock Settings Keyboard"

        # Call the handler
        await settings_handler(self.message)

        # Assertions
        self.message.answer.assert_awaited_with(
            "Settings menu:", reply_markup="Mock Settings Keyboard"
        )

    async def test_ask_liquidation_price_not_set(self):
        user_liquidation_prices.pop(self.message.chat.id, None)

        await ask_liquidation_price(self.message, self.state)

        # Assertions for all message.answer calls
        self.message.answer.assert_has_awaits(
            [
                unittest.mock.call("You have not set a liquidation price yet."),
                unittest.mock.call("Please enter the minimum liquidation price you want to track:"),
            ],
            any_order=False,
        )
        self.state.set_state.assert_awaited_with(
            "LiquidationSettings:waiting_for_liquidation_price"
        )

    async def test_set_liquidation_price_valid(self):
        # Mock user input
        self.message.text = "100"

        # Call the handler
        await set_liquidation_price(self.message, self.state)

        # Assertions
        self.assertEqual(user_liquidation_prices[self.message.chat.id], 100000.0)
        self.message.answer.assert_awaited_with(
            "Your liquidation price has been set to 100000.00"
        )
        self.state.clear.assert_awaited()

    @patch("bot.bk.binance_liquidations_keyboard_tracking")
    async def test_start_tracking_handler(self, mock_keyboard_tracking):
        # Mock the reply keyboard
        mock_keyboard = MagicMock()
        mock_keyboard_tracking.return_value = mock_keyboard

        # Clear active trackers before test
        active_trackers.clear()

        # Call the handler
        await start_tracking_handler(self.message)

        # Assertions
        self.assertIn(self.message.chat.id, active_trackers)
        self.message.answer.assert_awaited_with(
            "Starting Tracking Liquidations on Binance. You will receive notifications.",
            reply_markup=mock_keyboard,
        )

    @patch("bot.bk.binance_liquidations_keyboard_not_tracking")
    async def test_stop_tracking_handler(self, mock_keyboard_not_tracking):
        # Mock the reply keyboard
        mock_keyboard = MagicMock()
        mock_keyboard_not_tracking.return_value = mock_keyboard

        # Add user to active trackers
        active_trackers.add(self.message.chat.id)

        # Call the handler
        await stop_tracking_handler(self.message)

        # Assertions
        self.assertNotIn(self.message.chat.id, active_trackers)
        self.message.answer.assert_awaited_with(
            "Binance Tracking Stopped. You will no longer receive notifications.",
            reply_markup=mock_keyboard,
        )

    @patch("methods.connect_binance")
    async def test_binance_api_connection(self, mock_connect_binance):
        # Mock parameters for the connect_binance function
        mock_loop = MagicMock()
        mock_bot = MagicMock()

        # Call the mocked connect_binance function
        await mock_connect_binance(mock_loop, mock_bot, user_liquidation_prices, active_trackers)

        # Assertions
        mock_connect_binance.assert_awaited_once_with(mock_loop, mock_bot, user_liquidation_prices, active_trackers)

class TestOnMessageBinance(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Mock the Bot instance
        self.mock_bot = AsyncMock()
        self.mock_ws = MagicMock()

        # Mock user liquidation prices
        self.user_liquidation_prices = {
            12345: 10000.0,
        }

        # Mock active trackers
        self.active_trackers = {12345}

    async def test_on_message_binance_alert_sent(self):
        # Example WebSocket message
        message = {
            "o": {
                "s": "BTCUSDT",
                "p": "11000",  # Liquidation price
                "ap": "9000",  # Final price
                "q": "1",  # Quantity
                "S": "SELL",  # Side
            }
        }

        # Call the handler
        await on_message_binance(
            self.mock_ws,
            json.dumps(message),
            self.mock_bot,
            self.user_liquidation_prices,
            self.active_trackers,
        )

        # Assertions
        self.mock_bot.send_message.assert_awaited_once_with(
            chat_id=12345,
            text=(
                "Alert for Binance:\n"
                "Symbol: BTCUSDT\n"
                "Side: SELL\n"
                "Liquidation Price: 11000.0\n"
                "Quantity: 1.0\n"
                "ROI Loss: 2000.0\n"
                "Total Loss: 11000.0\n"
                "PNL Loss: 18.18%"
            )
        )

    async def test_on_message_binance_no_alert(self):
        # Example WebSocket message with no liquidation exceeding thresholds
        message = {
            "o": {
                "s": "BTCUSDT",
                "p": "5000",    # Liquidation price
                "ap": "4900",   # Final price
                "q": "1",       # Quantity
                "S": "SELL",    # Side
            }
        }

        # Call the handler
        await on_message_binance(
            self.mock_ws,
            json.dumps(message),
            self.mock_bot,
            self.user_liquidation_prices,
            self.active_trackers,
        )

        # Assertions
        self.mock_bot.send_message.assert_not_awaited()

if __name__ == "__main__":
    unittest.main()
