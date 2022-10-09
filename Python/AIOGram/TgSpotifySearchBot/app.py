from aiogram import types, executor

from loader import dp, logger, spotify
from lib.middleware import (
    AuthUserMiddleware,
    BasicMiddleware, 
    auth_user_command
)



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    `/start` and `/help` commands handler
    """
    await message.reply((
        '<b>Hello there! </b> \n'
        '<b>I am spotify searcher bot </b> \n'
        '<b>Type /search to search in spotify </b>\n'
    ))


@auth_user_command
@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    """
    `/search` command handler
    """
    if len(message['args']) == 0:
        return await message.reply((
            '<b>Empty Search! </b> \n'
            '<b>Please type /search</b> <i>query</i> \n'
            '<b>Example: <code>/search eminem</code> </b> \n'
        ))
    
    results = await spotify.search(message['args'][0])
    
    for item in results.playlists.items:
        await message.reply((
            f'<b>Name</b>: <code>{item.name}</code> \n'
            f'<b>Description</b>: <i>{item.description}</i> \n'
            f'<b>Owner</b>: <code>{item.owner.display_name}</code> \n'
            f'<b>Tracks C</b>: <code>{item.tracks.total}</code> \n'
            f'<b>Link</b>: <a href="{item.external_urls.spotify}">Open in Spotify</a> \n'
            f'<b>Image</b>: <a href="{item.images[0].url}">Open in Spotify</a> \n'
        ));




if __name__ == '__main__':
    logger.info('Bot started')
    dp.middleware.setup(BasicMiddleware())
    dp.middleware.setup(AuthUserMiddleware())
    executor.start_polling(dp, skip_updates=True)