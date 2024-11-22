from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from random import choice

from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client,  __version__, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import ChatAdminRequired,UserNotParticipant
from config import *
logger = logging.getLogger(__name__)


async def is_subscribed(bot, query):
    required_channels = [FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3]
    for channels in required_channels:
        try:
            user = await bot.get_chat_member(channels, query.from_user.id)
        except UserNotParticipant:
            pass
        except Exception as e:
            logger.exception(e)
        else:
            if user.status != enums.ChatMemberStatus.BANNED:
                return True
    return False

async def lazy_force_sub(client: Client, message: Message):
    try:
        invite_link = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL), creates_join_request=True)
        invite_link2 = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL2), creates_join_request=True)
        invite_link3 = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL3), creates_join_request=True)
    except ChatAdminRequired:
        logger.error("Hey Sona, Ek dfa check kr lo ki auth Channel mei Add hu ya nhi...!")
        return
    buttons = [
        
            [InlineKeyboardButton(text="📌ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ1", url=invite_link.invite_link)],
            [InlineKeyboardButton(text="📌ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ2", url=invite_link2.invite_link)],
            [InlineKeyboardButton(text="📌ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ3", url=invite_link3.invite_link)],
        
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='↺ʀᴇʟᴏᴀᴅ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass
    # setting up multiple message for force sub msg LazyDeveloperr
    lazydeveloperquotes = [
        "🌟{} \n *Great things never came from comfort zones.* Step in and join us for exciting updates!",
        "🚀{} \n *Stay connected, stay inspired.* Hit the join button to explore more!",
        "✨{} \n *Dream big, act bigger.* Stay with us for amazing content!",
        "💡{} \n *Knowledge is power.* Join us now and never miss an update!",
        "🔥{} \n *Your journey to greatness begins here.* Tap the button to join now!",
        "🎉{} \n *Be part of something amazing.* Join our channel and experience the magic!",
        "📚{} \n *Stay informed, stay ahead.* Join now for the latest updates!",
        "💪{} \n *Together, we grow stronger.* Don't miss out—join us today!",
        "🌈{} \n *Unlock a world of possibilities.* Tap below to stay connected!",
        "🌟{} \n *Your support fuels our journey.* Join the channel and be part of the family!"
    ]

    # Randomly select a quote
    text = choice(lazydeveloperquotes)

    await message.reply(
        text=text.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )
