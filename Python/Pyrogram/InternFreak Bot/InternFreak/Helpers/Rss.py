from .__init__ import *
from ..Helpers.FetchPosts import fetch_posts

CAPTION = """
<b>{title}</b>

<code>{batch}</code>

<b>{offer}</b> - <code>{date}</code>

<b>Post Link</b> - [link]({link})
"""

CHANNEL = -1001504019946
CODING_GROUP = -1001419259815


def jsload(file):
    with open(file, 'r') as js:
        return json.load(js)


def jsdump(obj, file):
    with open(file, 'w') as js:
        json.dump(obj, js, indent=4)


async def save_posts():
    posts = await loop.run_in_executor(executor, lambda: fetch_posts())
    if posts:
        jsdump(posts, "Intern.json")


async def upload_posts():
    posts = jsload("Intern.json")
    for title, content in posts.items():
        if await loop.run_in_executor(executor, lambda: check(content["link"])):
            post = await bot.send_photo(
                chat_id=CHANNEL,
                photo=content["thumbnail"].replace(" ", "%20"),
                caption=CAPTION.format(
                    title=title,
                    batch=content["batch"],
                    offer=content["offer"],
                    date=content["date"],
                    link=content["link"]
                )
            )
            await bot.send_sticker(
                chat_id=CHANNEL,
                sticker="CAACAgUAAx0CSVhoDAABFM_aYk01ZlDsdO_9BtdfYyLaKwI0QJ4AAjsAA0NzyRIuGBJU0KTNKyME"
            )
            await loop.run_in_executor(executor, lambda: publish(content["link"], title, str(post.id)))
            button = [
                [
                    InlineKeyboardButton(
                        text="Join Channel", url="https://t.me/internfreakposts"),
                ]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard=button)
            info = await bot.copy_message(chat_id=CODING_GROUP, from_chat_id=CHANNEL, message_id=post.id, reply_markup=markup)
            await bot.pin_chat_message(chat_id=CODING_GROUP, message_id=info.id)
            result = await loop.run_in_executor(executor, lambda: fetchIds())
            for users in result:
                try:
                    await bot.copy_message(chat_id=int(
                        users["key"]), from_chat_id=CHANNEL, message_id=post.id, reply_markup=markup)
                except FloodWait as e:
                    await asyncio.sleep(e.x)

            await asyncio.sleep(3)

save_post = AsyncIOScheduler()
save_post.add_job(save_posts, 'interval', minutes=1)
save_post.start()

upload_post = AsyncIOScheduler()
upload_post.add_job(upload_posts, 'interval', minutes=2)
upload_post.start()
