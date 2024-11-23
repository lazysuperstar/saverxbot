from helpo.lazyprogress import progress_for_pyrogram, convert
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
# from hachoir.metadata import extractMetadata
# from hachoir.parser import createParser
from helpo.database import db
import os
# import humanize
from PIL import Image
import time
from config import *
import asyncio




@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return

