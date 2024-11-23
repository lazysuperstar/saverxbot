import instaloader
import re
import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message


# Initialize Instaloader
insta = instaloader.Instaloader()

# Helper function to download media based on URL type
async def download_instagram_media(url, user_id):
    try:
        # Generate a dynamic directory based on user ID and timestamp
        timestamp = str(int(time.time()))
        base_folder = f"downloads/{user_id}/{timestamp}"
        os.makedirs(base_folder, exist_ok=True)

        if "/p/" in url:
            shortcode = url.split("/p/")[1].split("/")[0]
            post = instaloader.Post.from_shortcode(insta.context, shortcode)
            target_folder = os.path.join(base_folder, "post")
            os.makedirs(target_folder, exist_ok=True)
            insta.download_post(post, target=target_folder)
            return target_folder, post.url  # Folder path and URL for success message

        elif "/reel/" in url:
            shortcode = url.split("/reel/")[1].split("/")[0]
            post = instaloader.Post.from_shortcode(insta.context, shortcode)
            target_folder = os.path.join(base_folder, "reel")
            os.makedirs(target_folder, exist_ok=True)
            insta.download_post(post, target=target_folder)
            return target_folder, post.url

        elif "/stories/" in url or "stories" in url:
            username = re.findall(r"instagram\.com/stories/([^/]+)", url)[0]
            target_folder = os.path.join(base_folder, "stories", username)
            os.makedirs(target_folder, exist_ok=True)
            insta.download_stories(usernames=[username], filename_target=target_folder)
            return target_folder, f"Stories from {username}"

        else:
            return None, "Unsupported URL type. Please send a valid Instagram URL."

    except Exception as e:
        return None, f"Error occurred: {e}"

@Client.on_message(filters.private & filters.text & ~filters.command(['start','users','broadcast']))
async def handle_incoming_message(client: Client, message: Message):
    try:
        # Extract the message text and user ID
        url = message.text.strip()
        user_id = message.from_user.id  # Get user ID dynamically

        if "instagram.com" not in url:
            await message.reply("❌ Please send a valid Instagram URL.")
            return

        # Inform user about processing
        await message.reply("🔄 Detecting URL type and processing the download...")

        # Process the Instagram URL
        folder, result = await download_instagram_media(url, user_id)

        if folder:
            # Loop through the downloaded files in the folder
            media_sent = False
            for file_name in sorted(os.listdir(folder)):
                file_path = os.path.join(folder, file_name)

                # Upload files to Telegram if they are media files
                if file_name.endswith((".jpg", ".png", ".mp4")):
                    await client.send_document(chat_id=message.chat.id, document=file_path)
                    media_sent = True

            # Inform the user when all files have been sent
            if media_sent:
                await message.reply("✅ Reel has been downloaded and sent to you!")
            else:
                await message.reply("❌ Could not find valid media to send.")

            # Clean up dynamic folder after sending files
            for file_name in os.listdir(folder):
                os.remove(os.path.join(folder, file_name))
            os.removedirs(folder)

        else:
            # If no folder, return the error message
            await message.reply(result)

    except Exception as e:
        await message.reply(f"❌ An error occurred: {e}")


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
