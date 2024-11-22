from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
# from pyrogram.errors import FloodWait
# import humanize
# import random
from helpo.txt import mr
from helpo.database import db
from config import *
from plugins.LazyDev_F_Sub import lazy_force_sub, is_subscribed

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)

    if (FORCE_SUB_CHANNEL or FORCE_SUB_CHANNEL2 or FORCE_SUB_CHANNEL3) and not await is_subscribed(client, message):
        # User is not subscribed to any of the required channels, trigger force_sub logic
        return await lazy_force_sub(client, message) 
              
    welcome_text = """
    👋 Hey {}! Welcome to the *LazyBot* 🤖✨

    I'm here to make your life easier and fun! Here's what I can do for you:

    1️⃣ *Instagram* – Download Stories, Reels, and Posts from Instagram.
    2️⃣ *TikTok* – Get videos without watermark.
    3️⃣ *Twitter* – Download media from tweets.
    4️⃣ *Pinterest* – Grab images and posts from Pinterest.
    5️⃣ Plus, much more... 🚀

    Simply send me the *URL* of the media you want to download, and I'll take care of the rest! 🎉

    Let's start downloading your favorite content! 🚀
    """

    button=InlineKeyboardMarkup([[
        InlineKeyboardButton('📢 𝚄𝙿𝙳𝙰𝚃𝙴𝚂', url='https://t.me/lazydeveloper'),
        InlineKeyboardButton('♻ 𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url='https://t.me/lazydeveloper')
        ],[
        InlineKeyboardButton("❤.[-. 𝙳𝙴𝚅𝚂 .-].🍟", callback_data='dev')
        ][
        InlineKeyboardButton('🦋 𝙰𝙱𝙾𝚄𝚃', callback_data='about'),
        InlineKeyboardButton('ℹ️ 𝙷𝙴𝙻𝙿', callback_data='help')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=welcome_text.format(message.from_user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=welcome_text.format(message.from_user.mention), reply_markup=button, disable_web_page_preview=True)
   

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"""👋 Hai {query.from_user.mention} \n𝙸'𝚖 𝙰 𝚂𝚒𝚖𝚙𝚕𝚎 𝙵𝚒𝚕𝚎 𝚁𝚎𝚗𝚊𝚖𝚎+𝙵𝚒𝚕𝚎 𝚃𝚘 𝚅𝚒𝚍𝚎𝚘 𝙲𝚘𝚟𝚎𝚛𝚝𝚎𝚛 𝙱𝙾𝚃 𝚆𝚒𝚝𝚑 𝙿𝚎𝚛𝚖𝚊𝚗𝚎𝚗𝚝 𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕 & 𝙲𝚞𝚜𝚝𝚘𝚖 𝙲𝚊𝚙𝚝𝚒𝚘𝚗 𝚂𝚞𝚙𝚙𝚘𝚛𝚝! """,
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("👼 𝙳𝙴𝚅𝚂 👼", callback_data='dev')                
                ],[
                InlineKeyboardButton('📢 𝚄𝙿𝙳𝙰𝚃𝙴𝚂', url='https://t.me/'),
                InlineKeyboardButton('🍂 𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url='https://t.me/')
                ],[
                InlineKeyboardButton('🍃 𝙰𝙱𝙾𝚄𝚃', callback_data='about'),
                InlineKeyboardButton('ℹ️ 𝙷𝙴𝙻𝙿', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=mr.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton("❣️ 𝚂𝙾𝚄𝚁𝙲𝙴", url="https://github.com/")
               ],[
               InlineKeyboardButton("❤️‍🔥 𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴  ❤️‍🔥", url='https://youtu.be/')
               ],[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=mr.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton("❣️ 𝚂𝙾𝚄𝚁𝙲𝙴", url="https://github.com/")
               ],[
               InlineKeyboardButton("🖥️ 𝙷𝙾𝚆 𝚃𝙾 𝙼𝙰𝙺𝙴", url="https://youtu.be/")
               ],[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=mr.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton("❣️ 𝚂𝙾𝚄𝚁𝙲𝙴", url="https://github.com/")
               ],[
               InlineKeyboardButton("🖥️ 𝙷𝙾𝚆 𝚃𝙾 𝙼𝙰𝙺𝙴", url="https://youtu.be/")
               ],[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()





