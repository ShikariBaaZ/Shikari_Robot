from time import time
import asyncio
from pyrogram.types import Message
from Shikari.utils.extract_user import extract_user
from Shikari import BOT_ID,app
from Shikari.utils.functions import extract_user_and_reason,time_converter
from pyrogram.types import Message
from lang import get_command
from Shikari.utils.commands import *
from Shikari.utils.lang import *
from Shikari.utils.custom_filters import restrict_filter
from Shikari.plugins.fsub import ForceSub
from button import *

KICK_ME = get_command("KICK_ME")
SKICK = get_command("SKICK")
KICK = get_command("KICK")
BAN = get_command("BAN")
UNBAN = get_command("UNBAN")
SBAN = get_command("SBAN")


@app.on_message(command(KICK_ME) )
@language
async def kickFunc(client, message: Message, _):
    reason = None
    if len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    try:
        await message.chat.ban_member(message.from_user.id)
        txt = f" Bye {message.from_user.mention}, you're right - get out."
        txt += f"\n<b>Reason</b>: {reason}" if reason else ""
        await message.reply_text(txt)
        await message.chat.unban_member(message.from_user.id)
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return


@app.on_message(command(SKICK) & restrict_filter)
@language
async def kickFunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return
    try:
        user_id = await extract_user(message)
    except Exception:
        return   
    if not user_id:
        await message.reply_text(_["ban2"])
        return  
    st = await client.get_chat_member(message.chat.id, user_id)
    if (
                st.status == "administrator"
                and st.status == "creator"
        ):
            return
    try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
        await message.chat.unban_member(user_id)
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return



@app.on_message(command(KICK) & restrict_filter)
@language
async def kickFunc(client, message: Message, _):
    FSub = await ForceSub(app, message)
    if FSub == 400:
        return
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await message.reply_text(_["ban3"])
    if user_id == BOT_ID:
        return await message.reply_text(_["ban4"])
    st = await client.get_chat_member(message.chat.id, user_id)
    if (
                st.status == "administrator"
                and st.status == "creator"
        ):
        return await message.reply_text(_["ban7"])
    mention = (await app.get_users(user_id)).mention
    msg = f"""
{mention}** Was Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


@app.on_message(command(BAN)& restrict_filter)
@language
async def banFunc(client, message: Message, _):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text(_["ban3"])
    if user_id == BOT_ID:
        return await message.reply_text(_["ban4"])
    st = await client.get_chat_member(message.chat.id, user_id)
    if (
                st.status == "administrator"
                and st.status == "creator"
        ):
        return await message.reply_text("I can't ban admin in this group !")
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    await message.chat.ban_member(user_id)
    msg = (
        f"{mention}\n"
        f"**Was Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text(_["ban14"])
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


@app.on_message(command(UNBAN)  & restrict_filter)
@language
async def unbanFunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("Provide a username or reply to a user's message to unban.")
        await message.stop_propagation()

    if message.reply_to_message and not message.reply_to_message.from_user:
        user_id, user_first_name = (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )
    else:
        try:
            user_id, user_first_name, _ = await extract_user(app, message)
        except Exception:
            return
    await message.chat.unban_member(user_id)
    await message.reply_text(f"{user_first_name} was unbanned by {message.from_user.mention}")


@app.on_message(command(SBAN) & restrict_filter)
async def kickunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return
    try:
        user_id = await extract_user(message)
    except Exception:
        return   
    if not user_id:
        await message.reply_text("Can't find user to kick")
        return   
    st = await app.get_chat_member(message.chat.id, user_id)
    if (
                st.status == "administrator"
                and st.status == "creator"
        ):
        return     
    try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return


__MODULE__ = f"{Restrict}"
__HELP__ = """
Some people need to be publicly banned; spammers, annoyances, or just trolls.

This module allows you to do that easily, by exposing some common actions, so everyone will see!

**User commands:**
- /kickme: Users that use this, kick themselves.

**Admin commands:**
- /ban: Ban a user.
- /dban: Ban a user by reply, and delete their message.
- /sban: Silently ban a user, and delete your message.
- /tban: Temporarily ban a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
- /unban: Unban a user.

- /mute: Mute a user.
- /dmute: Mute a user by reply, and delete their message.
- /smute: Silently mute a user, and delete your message.
- /tmute: Temporarily mute a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
- /unmute: Unmute a user.

- /kick: Kick a user.
- /dkick: Kick a user by reply, and delete their message.
- /skick: Silently kick a user, and delete your message

**Examples:**
- Mute a user for two hours.
- `/tmute @username 2h`
"""
