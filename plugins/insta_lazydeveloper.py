import instaloader
import re
import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo
import asyncio
# Initialize @LazyDeveloperr Instaloader 
insta = instaloader.Instaloader()

@Client.on_message(filters.private & filters.text & ~filters.command(['start','users','broadcast']))
async def handle_incoming_message(client: Client, message: Message):
    try:
        if message.from_user.id not in ADMIN:
            await client.send_message(chat_id=message.chat.id, text=f"Sorry Sweetheart! cant talk to you \nTake permission from my Lover @LazyDeveloperr")
        # Extract the message text and user ID
        url = message.text.strip()
        user_id = message.from_user.id  # Get user ID dynamically

        # Check if the URL contains 'instagram.com'
        if "instagram.com" not in url:
            await message.reply("❌ ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ.")
            return

        # Inform user about processing
        progress_message = await message.reply("🔄 ᴅᴇᴛᴇᴄᴛɪɴɢ ᴜʀʟ ᴛʏᴘᴇ ᴀɴᴅ ᴘʀᴏᴄᴇssɪɴɢ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ...")

        # Extract shortcode from Instagram URL (assuming this is a function you implemented)
        post_shortcode = get_post_or_reel_shortcode_from_link(url)
        
        if not post_shortcode:
            print(f"log:\n\nuser: {message.chat.id}\n\nerror in getting post_shortcode")
            return  # Post shortcode not found, stop processing
        
        progress_message2 = await progress_message.edit("<i>⚙ ᴘʀᴇᴘᴀʀɪɴɢ ᴛᴏ ꜰᴇᴛᴄʜ ᴄᴀᴘᴛɪᴏɴ...</i>")
        await asyncio.sleep(1)
        
        # Get an instance of Instaloader (assuming this function initializes it)
        L = get_ready_to_work_insta_instance()        
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)

        # Caption handling (ensure the caption does not exceed Telegram's limit)
        bot_username = client.username if client.username else "@lazydeveloeprr"
        caption_trail = "\n\n\n" + bot_username

        new_caption = post.caption
        while len(new_caption) + len(caption_trail) > 1024:
            new_caption = new_caption[:-1]  # Trim caption if it's too long
        new_caption = new_caption + caption_trail  # Add bot username at the end
         # Initialize media list
        
        progress_message3 = progress_message2.edit("<i>⚡ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ...</i>")
        await asyncio.sleep(1)
        media_list = []

        # Handle sidecars (multiple media in a post)
        if post.mediacount > 1:
            sidecars = post.get_sidecar_nodes()
            for s in sidecars:
                if s.is_video:
                    url = s.video_url
                    media = InputMediaVideo(url)
                    if not media_list:  # Add caption to the first media
                        media = InputMediaVideo(url, caption=new_caption)
                else:
                    url = s.display_url
                    media = InputMediaPhoto(url)
                    if not media_list:  # Add caption to the first media
                        media = InputMediaPhoto(url, caption=new_caption)
                media_list.append(media)

            # Send media group
            await client.send_media_group(message.chat.id, media_list)

        else:
            # Single media handling
            if post.is_video:
                await client.send_video(message.chat.id, post.video_url, caption=new_caption)
            else:
                await client.send_photo(message.chat.id, post.url, caption=new_caption)

        await progress_message3.delete()
        lazydeveloper = await client.send_message(f"❤ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ sʜᴀʀᴇ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ꜰʀɪᴇɴᴅ ᴄɪʀᴄʟᴇ...")
        await asyncio.sleep(300)
        await lazydeveloper.delete()
    except Exception as e:
        # Handle any errors
        await message.reply(f"❌ An error occurred: {e}")

    except Exception as e:
        # Handle any other errors
        await message.reply(f"❌ An error occurred: {e}")


# regex
insta_post_or_reel_reg = r'(?:https?://www\.)?instagram\.com\S*?/(p|reel)/([a-zA-Z0-9_-]{11})/?'

def get_post_or_reel_shortcode_from_link(link):
    match = re.search(insta_post_or_reel_reg, link)
    if match:
        return match.group(2)
    else:
        return False

def get_ready_to_work_insta_instance():
    L = instaloader.Instaloader()
    return L

