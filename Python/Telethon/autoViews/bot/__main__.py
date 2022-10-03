from telethon import events, functions, TelegramClient
from random import randint
from config import vars
from bot import client
import asyncio
import os

@client.on(events.NewMessage(from_users=vars.channel_ids))
async def eventHandler(e):
    x = await e.forward_to(vars.channel)
    for account in vars.accounts:
        try:
            await account.start()
            await account(functions.messages.GetMessagesViewsRequest(
                peer=vars.channel,
                id=[x.id],
                increment=True
            ))
        except Exception as error: print(error)
        await asyncio.sleep(randint(1, 5))
    await x.delete()

if __name__ == "__main__":
    for i in [x for x in os.listdir("sessions") if x.endswith(".session")]:
        account = TelegramClient(
            session=os.path.join("sessions", i),
            api_id=vars.api_id,
            api_hash=vars.api_hash
        )
        vars.accounts.append(account)
    client.run_until_disconnected()