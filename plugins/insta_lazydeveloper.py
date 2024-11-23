import instaloader
import re
import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo

# Initialize Instaloader
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
            await message.reply("❌ Please send a valid Instagram URL.")
            return

        # Inform user about processing
        progress_message = await message.reply("🔄 Detecting URL type and processing the download...")

        # Extract shortcode from Instagram URL (assuming this is a function you implemented)
        post_shortcode = get_post_or_reel_shortcode_from_link(url)
        
        if not post_shortcode:
            print(f"log:\n\nuser: {message.chat.id}\n\nerror in getting post_shortcode")
            return  # Post shortcode not found, stop processing
        
        # Get an instance of Instaloader (assuming this function initializes it)
        # L = get_ready_to_work_insta_instance()        
        post = instaloader.Post.from_shortcode(insta.context, post_shortcode)

        # Caption handling (ensure the caption does not exceed Telegram's limit)
        bot_username = "@LazyDevDemo_BOT"
        caption_trail = "\n\n\n" + bot_username

        await progress_message.edit("<i>⚙fetching caption...</i>")

        new_caption = post.caption
        while len(new_caption) + len(caption_trail) > 1024:
            new_caption = new_caption[:-1]  # Trim caption if it's too long
        new_caption = new_caption + caption_trail  # Add bot username at the end
         # Initialize media list
        
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

    except Exception as e:
        # Handle any errors
        await message.reply(f"❌ An error occurred: {e}")
        # Check if the post has one media item (image/video)
        # if post.mediacount == 1:
        #     if post.is_video:
        #         # Send video if the post is a video
        #         await client.send_video(message.chat.id, post.video_url, caption=new_caption)
        #     else:
        #         # Send photo if the post is an image
        #         await client.send_photo(message.chat.id, post.url, caption=new_caption)
        #     return

        # else:
        #     # Handle case for posts with multiple media (not implemented here)
        #            # handle post with multiple media
        #     media_list = []
        #     sidecars = post.get_sidecar_nodes()
        #     for s in sidecars:
        #         if s.is_video: # it's a video
        #             url = s.video_url
        #             media = InputMediaVideo(url)
        #             if not media_list: # first media of post
        #                 media = InputMediaVideo(url, caption=new_caption)
        #         else: # it's an image
        #             url = s.display_url
        #             media = InputMediaPhoto(url)
        #             if not media_list: # first media of post
        #                 media = InputMediaPhoto(url, caption=new_caption)
        #         media_list.append(media)
        #     client.send_media_group(message.chat.id, media_list)
        

    except Exception as e:
        # Handle any other errors
        await message.reply(f"❌ An error occurred: {e}")


# regex
insta_post_or_reel_reg = r'(?:https?://www\.)?instagram\.com\S*?/(p|reel)/([a-zA-Z0-9_-]{11})/?'
# insta_post_or_reel_reg = r'(?:https?://(?:www\.)?)?instagram\.com/(p|reel)/([a-zA-Z0-9_-]{11})/?'

def get_post_or_reel_shortcode_from_link(link):
    match = re.search(insta_post_or_reel_reg, link)
    if match:
        return match.group(2)
    else:
        return False

def get_ready_to_work_insta_instance():
    L = instaloader.Instaloader()
    return L

