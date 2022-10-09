import os

from loader import logger
from lib.utils import in_file

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler,current_handler


class BasicMiddleware(BaseMiddleware):
    def __init__(self):
        """Middleware that handles the stuffs that are common to all handlers"""
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """ This function will run whenever a new message is received """

        # Cancle the handler if the message is sended by a bot
        if message.from_user.is_bot:
            return CancelHandler()
        
        handler = current_handler.get()

        # if not @dp.message_handler is setup for this command then the command will be ignored
        if not handler: 
            return CancelHandler()

        logger.info(f'@{message.from_user.username} typed {message.get_command()} command')
        
        if message.get_args():
            message['command'] = message.get_command()
            message['args'] = message.get_args().split()
            
        else:
            msg = message.text.split()
            message['command'] = msg.pop(0)
            message['args'] = msg
            
            
class AuthUserMiddleware(BaseMiddleware):
    def __init__(self):
        """Middleware that will check if the user is authorized"""
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """ This function will run whenever a new message is received """
        
        handler = current_handler.get()

        # if this command does not has the @auth_user_command decorator then this middleware will not be executed
        if not getattr(handler, 'auth_user_command', False):
            return

        # Check if user is in the database 
        if not in_file('users', str(message.from_user.id)):
            logger.info(f'@{message.from_user.username}User is not registered')

            await message.answer((
                '<b>You are not authorized user</b> \n'
                f'<b>Please contact <a href="tg://user?id={os.getenv("BOT_OWNER_ID")}">owner</a> to get authorization. </b>\n'
            ))
            raise CancelHandler()
        

def auth_user_command(func):
    """A decorator that will be used to mark the commands that need authorization

    Args:
        func : The function that will be decorated

    Returns:
        A @auth_user_command decorated function
    """
    setattr(func, 'auth_user_command', True)
    return func
