from pyrogram import Client, filters, types
from pyrogram.types import Message
from io import BytesIO
import requests
import time
from TikTokApi import TikTokApi
import os

from config import TEL_USERNAME

api = TikTokApi.get_instance()

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
        
        # Download video using tiktok_downloader (snaptik)
        
        bot_username = client.username if client.username else TEL_USERNAME
        caption_lazy = f".\nᴡɪᴛʜ ❤ @{bot_username}\n."
        try:
            api = TikTokApi.get_instance()
            video_data = api.video(url=url).bytes()
            video_path = f"{message.chat.id}/{time.time()}/tiktok_video.mp4"

            with open(video_path, "wb") as video_file:
                video_file.write(video_data)
            
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
            print(f"Error: {e}")
        
    except Exception as e:
        await message.reply(f"❌ An unexpected error occurred: {e}")
