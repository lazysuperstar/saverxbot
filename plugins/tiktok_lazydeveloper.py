from pyrogram import Client, filters, types
from pyrogram.types import Message
from io import BytesIO
import requests
import time
from TikTokApi import TikTokApi
import os
from tiktok_downloader import snaptik


from config import TEL_USERNAME



@Client.on_message(filters.private & filters.text & ~filters.command(['start', 'help']))
async def handle_tiktok_download(client: Client, message: Message):
    try:
        url = message.text.strip()
        
        # Check if the URL is a valid TikTok link
        if "tiktok.com" not in url:
            await message.reply("❌ Please send a valid TikTok URL.")
            return
        
        # Inform the user about the processing
        msg_del = await message.reply("🔄 Processing your TikTok link. Please wait...")
        
        bot_username = client.username or "LazyDownloaderBot"
        caption_lazy = f".\nᴡɪᴛʜ ❤ @{bot_username}\n."
        
        # Initialize TikTokApi
        try:
            api = TikTokApi()
            
            # Fetch video bytes
            video_data = api.video(url=url).bytes()

            if not video_data:
                await message.reply("❌ Unable to fetch the video. Please try again later or check the URL.")
                await msg_del.delete()
                return

            # Define the path to save the video
            video_path = f"{message.chat.id}_{time.time()}_tiktok_video.mp4"

            # Save video bytes to a file
            with open(video_path, "wb") as video_file:
                video_file.write(video_data)

            # Send the video
            await client.send_video(
                chat_id=message.chat.id,
                video=video_path,
                caption=caption_lazy
            )
            print(f"Video sent successfully: {video_path}")

            # Cleanup
            await msg_del.delete()
            os.remove(video_path)

        except Exception as e:
            await msg_del.delete()
            await message.reply(f"❌ Failed to download video. Error: {str(e)}")
            print(f"Error during TikTok download: {e}")
        
    except Exception as e:
        await message.reply(f"❌ An unexpected error occurred: {e}")

    #     try:
    #         res = snaptik(url)  # Download the TikTok video
    #         video_url = res[0]["download_url"]  # Get the direct download URL for the video
    #         video_path = f"{message.chat.id}_{time.time()}.mp4"

    #         # Download the video to a file
    #         video_data = requests.get(video_url).content
    #         with open(video_path, "wb") as video_file:
    #             video_file.write(video_data)

    #         # Send the video to the user
    #         await client.send_video(chat_id=message.chat.id, video=video_path, caption=caption_lazy)
    #         print(f"Video sent successfully: {video_path}")

    #         # Cleanup
    #         await msg_del.delete()
    #         os.remove(video_path)

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         await message.reply("❌ Failed to download the TikTok video. Please try again later.")

    # except Exception as e:
    #     await message.reply(f"❌ An unexpected error occurred: {e}")

        # try:
        #     api = TikTokApi.get_instance()
        #     video_data = api.video(url=url).bytes()
        #     video_path = f"{message.chat.id}/{time.time()}/tiktok_video.mp4"

        #     with open(video_path, "wb") as video_file:
        #         video_file.write(video_data)
            
        #     await client.send_video(
        #         chat_id=message.chat.id,
        #         video=video_path,
        #         caption=caption_lazy
        #     )
        #     print(f"Video sent successfully: {video_path}")

        #     # Cleanup
        #     await msg_del.delete()
        #     os.remove(video_path)
        # except Exception as e:
        #     print(f"Error: {e}")
        
    # except Exception as e:
    #     await message.reply(f"❌ An unexpected error occurred: {e}")
