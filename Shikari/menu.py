from Shikari import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Shikari.utils.lang import *


fbuttons = InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                text="👥Support Group", url="https://t.me/ShikariSupportNetwork"
            ),
            InlineKeyboardButton(
                text="👤News Channel", url="https://t.me/The_SHIKARI_Network"
            )
        ], 
        [
            InlineKeyboardButton(
                text="⚒ Source Code", url="https://github.com/ShikariBaaZ/Shikari_Robot"
            ),
            InlineKeyboardButton(
                text="📓 Documentation", url="https://github.com/ShikariBaaZ"
            )
        ], 
        [
            InlineKeyboardButton(
                text="🖥 How To Deploy Me", url="https://github.com/ShikariBaaZ/Shikari_Robot/blob/main/README.md"
            )
        ], 
        [
            InlineKeyboardButton("« Back", callback_data='startcq')
        ]
        ]
)

keyboard =InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="English🇬🇧", callback_data="languages_en"
            ),
            InlineKeyboardButton(
                text="සිංහල🇱🇰", callback_data="languages_si"
            )
        ],
        [
            InlineKeyboardButton(
                text="हिन्दी🇮🇳", callback_data="languages_hi"
            ),
            InlineKeyboardButton(
                text="Italiano🇮🇹", callback_data="languages_it"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌎 Help us with translation",
                url=f"https://crowdin.com/project/shikarirobot",
            )
        ],
        [
            InlineKeyboardButton("« Back", callback_data='startcq')
        ]
    ]
)

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    user = CallbackQuery.message.from_user.mention
    await app.send_message(
        CallbackQuery.message.chat.id,
        text= _["setting_1"].format(user),
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
    
@app.on_callback_query(filters.regex("_about"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=_["menu"],
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

