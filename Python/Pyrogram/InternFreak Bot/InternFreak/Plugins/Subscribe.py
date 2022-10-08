from .__init__ import *


@bot.on_message(filters.command(['subscribe', 'subscribe@internfreakbot']) & filters.private)
async def subscribe(app, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    if await loop.run_in_executor(executor, lambda: checkSubs(str(user_id))):
        await loop.run_in_executor(executor, lambda: addSubs(name, str(user_id)))
        await message.reply(text=f"<b><i>Successfully Subscribed</b></i>")
    else:
        await message.reply(text=f"<b><i>You are already Subscribed :)</b></i>")


@bot.on_message(filters.command(['unsubscribe', 'unsubscribe@internfreakbot']) & filters.private)
async def unsubscribe(app, message):
    user_id = message.from_user.id
    await loop.run_in_executor(executor, lambda: removeSubs(str(user_id)))
    await message.reply(text=f"<b><i>Successfully Unsubscribed :(</b></i>")
