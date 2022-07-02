from pyrogram.types import Message
from Shikari import *
from Shikari.utils.filter_groups import *
from Shikari.utils.filter_groups import *
from os import remove         
from Shikari.utils.commands import *
from Shikari.utils.lang import *


@app.on_message(command("nsfwscan"))
async def nsfw_scan_command(_, message: Message):
    err = "Reply to an image/document/sticker/animation to scan it."
    if not message.reply_to_message:
        await message.reply_text(err)
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(err)
        return
    m = await message.reply_text("Scanning")
    file_id = get_file_id(reply)
    if not file_id:
        return await m.edit("Something went wrong.")
    file = await app.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception as e:
        return await m.edit(str(e))
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**NSFW** scan Result Here ✅
==========================
• **Neutral:** `{results.neutral} %`
• **Porn:** `{results.porn} %`
• **Hentai:** `{results.hentai} %`
• **Sexy:** `{results.sexy} %`
• **Drawings:** `{results.drawings} %`
• **NSFW:** `{results.is_nsfw}`
==========================
"""
    )


@app.on_message(command("spamscan"))
async def scanNLP(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to scan it.")
    r = message.reply_to_message
    text = r.text or r.caption
    if not text:
        return await message.reply("Can't scan that")
    data = await arq.nlp(text)
    data = data.result[0]
    msg = f"""
**SPAm** scan Result Here ✅
==========================    
• **Is Spam:** `{data.is_spam}`
• **Spam Probability:** `{data.spam_probability}` %
• **Spam:** `{data.spam}`
• **Ham:** `{data.ham}`
• **Profanity:** `{data.profanity}`
==========================
"""
    await message.reply(msg, quote=True)

#helpers
def get_file_id(message):
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
        return message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            return message.sticker.thumbs[0].file_id
        return message.sticker.file_id

    if message.photo:
        return message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        return message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        return message.video.thumbs[0].file_id
  

async def admins(chat_id: int):
    return [ member.user.id
        async for member in app.iter_chat_members(
            chat_id, filter="administrators"
        )]

def get_file_unique_id(message):
    m = message
    m = m.sticker or m.video or m.document or m.animation or m.photo
    if not m:
        return
    return m.file_unique_id
