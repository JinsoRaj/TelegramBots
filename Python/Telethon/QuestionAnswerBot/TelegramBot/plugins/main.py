from .. import bot, helpers
from telethon import events, Button


@bot.on(events.NewMessage(pattern='/start$'))
async def start(event):
    xyz = helpers.get_question(None) # passing None for getting first question because in the Entrypoint we have passed null
    await event.reply(xyz['q'], buttons=[[Button.inline(i['text'], i['callback']),] for i in xyz['a']])

@bot.on(events.CallbackQuery(pattern=f"^(.+)_answer"))
async def _handle_all_questions(e):
    raw_data = helpers.get_question(e.data.decode()) # new question based on answer
    question, answer = helpers.get_answered_question(e.data.decode()) # you get prevous question and answer
    if raw_data: await e.edit(raw_data['q'], buttons=[[Button.inline(i['text'], i['callback']),] for i in raw_data['a']]) # you have still next questions 
    else: await e.edit("Thanks for participating!") # if NoneType returned then you don't have more questions for users