from deta import Deta
import os

deta = Deta(os.environ.get("DETA"))
POSTS = deta.Base("POSTS")
SUBS = deta.Base("SUBSCRIBERS")


def check(_key):
    result = POSTS.get(_key)
    if not result:
        return True
    else:
        return False


def publish(_key, title, msg_id):
    doc = {
        'key': _key,
        'title': title,
        'message_id': msg_id
    }
    POSTS.put(doc)


def checkSubs(user_id):
    sub_feeds = SUBS.get(user_id)
    if sub_feeds:
        return False
    else:
        doc = {
            'key': user_id,
            'name': "name",
        }
    SUBS.put(doc)
    return True


def addSubs(name, user_id):
    doc = {
        'name': name,
    }
    SUBS.update(doc, user_id)


def removeSubs(user_id):
    SUBS.delete(user_id)


def fetchIds():
    result = SUBS.fetch()
    all_items = result.items
    while result.last:
        result = SUBS.fetch(last=result.last)
        all_items += result.items
    return all_items
