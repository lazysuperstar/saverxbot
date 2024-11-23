import instaloader
import re
import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message


# Initialize Instaloader
insta = instaloader.Instaloader()

# Helper function to download media based on URL type
# async def download_instagram_media(url, user_id):
#     try:
#         # Generate a dynamic directory based on user ID and timestamp
#         timestamp = str(int(time.time()))
#         base_folder = f"downloads/{user_id}/{timestamp}"
#         os.makedirs(base_folder, exist_ok=True)

#         if "/p/" in url:
#             shortcode = url.split("/p/")[1].split("/")[0]
#             post = instaloader.Post.from_shortcode(insta.context, shortcode)
#             target_folder = os.path.join(base_folder, "post")
#             os.makedirs(target_folder, exist_ok=True)
#             insta.download_post(post, target=target_folder)
#             return target_folder, post.url  # Folder path and URL for success message

#         elif "/reel/" in url:
#             shortcode = url.split("/reel/")[1].split("/")[0]
#             post = instaloader.Post.from_shortcode(insta.context, shortcode)
#             target_folder = os.path.join(base_folder, "reel")
#             os.makedirs(target_folder, exist_ok=True)
#             insta.download_post(post, target=target_folder)
#             return target_folder, post.url

#         elif "/stories/" in url or "stories" in url:
#             username = re.findall(r"instagram\.com/stories/([^/]+)", url)[0]
#             target_folder = os.path.join(base_folder, "stories", username)
#             os.makedirs(target_folder, exist_ok=True)
#             insta.download_stories(usernames=[username], filename_target=target_folder)
#             return target_folder, f"Stories from {username}"

#         else:
#             return None, "Unsupported URL type. Please send a valid Instagram URL."

#     except Exception as e:
#         return None, f"Error occurred: {e}"

@Client.on_message(filters.private & filters.text & ~filters.command(['start','users','broadcast']))
async def handle_incoming_message(client: Client, message: Message):
    try:
        # Extract the message text and user ID
        url = message.text.strip()
        user_id = message.from_user.id  # Get user ID dynamically

        # Check if the URL contains 'instagram.com'
        if "instagram.com" not in url:
            await message.reply("❌ Please send a valid Instagram URL.")
            return

        # Inform user about processing
        await message.reply("🔄 Detecting URL type and processing the download...")

        # Extract shortcode from Instagram URL (assuming this is a function you implemented)
        post_shortcode = get_post_or_reel_shortcode_from_link(url)
        
        if not post_shortcode:
            print(f"log:\n\nuser: {message.chat.id}\n\nerror in getting post_shortcode")
            return  # Post shortcode not found, stop processing
        
        # Get an instance of Instaloader (assuming this function initializes it)
        L = get_ready_to_work_insta_instance()        
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)

        # Caption handling (ensure the caption does not exceed Telegram's limit)
        bot_username = "@LazyDevDemo_BOT"
        caption_trail = "\n\n\n" + bot_username
        session_file_name = "session"  # Change session name if needed

        new_caption = post.caption
        while len(new_caption) + len(caption_trail) > 1024:
            new_caption = new_caption[:-1]  # Trim caption if it's too long
        new_caption = new_caption + caption_trail  # Add bot username at the end

        # Check if the post has one media item (image/video)
        if post.mediacount == 1:
            if post.is_video:
                # Send video if the post is a video
                await client.send_video(message.chat.id, post.video_url, caption=new_caption)
            else:
                # Send photo if the post is an image
                await client.send_photo(message.chat.id, post.url, caption=new_caption)
            return

        else:
            # Handle case for posts with multiple media (not implemented here)
            print("Post contains multiple media items, further logic needed.")
            # You can add logic for handling multiple images or videos here.

    except Exception as e:
        # Handle any other errors
        await message.reply(f"❌ An error occurred: {e}")


# regex
# insta_post_or_reel_reg = r'(?:https?://www\.)?instagram\.com\S*?/(p|reel)/([a-zA-Z0-9_-]{11})/?'
insta_post_or_reel_reg = r'(?:https?://(?:www\.)?)?instagram\.com/(p|reel)/([a-zA-Z0-9_-]{11})/?'

def get_post_or_reel_shortcode_from_link(link):
    match = re.search(insta_post_or_reel_reg, link)
    if match:
        return match.group(2)
    else:
        return False

def get_ready_to_work_insta_instance():
    L = instaloader.Instaloader()
    return L



# Telegram bot handler (Pyrogram version)
# @Client.on_message(filters.text)
# async def handle_incoming_message(client: Client, message: Message):
#     try:
#         # Extract the message text and user ID
#         url = message.text.strip()
#         user_id = message.from_user.id  # Get user ID dynamically

#         if "instagram.com" not in url:
#             await message.reply("❌ Please send a valid Instagram URL.")
#             return

#         # Inform user about processing
#         await message.reply("🔄 Detecting URL type and processing the download...")

#         # Process the Instagram URL
#         folder, result = await download_instagram_media(url, user_id)

#         if folder:
#             # Send all files in the dynamic folder to the user
#             for file_name in os.listdir(folder):
#                 file_path = os.path.join(folder, file_name)
#                 await client.send_document(message.chat.id, file_path)

#             # Clean up dynamic folder after sending files
#             for file_name in os.listdir(folder):
#                 os.remove(os.path.join(folder, file_name))
#             os.removedirs(folder)

#             await message.reply("✅ Download completed and sent!")
#         else:
#             # If no folder, return the error message
#             await message.reply(result)

#     except Exception as e:
#         await message.reply(f"❌ An error occurred: {e}")
