from pyrogram import Client, filters, types
from pyrogram.types import Message
from io import BytesIO
import requests
import time
# from TikTokApi import TikTokApi
import os
# from tiktok_downloader import snaptik
from tiktok_scraper import TikTokScraper


from config import TEL_USERNAME



@Client.on_message(filters.private & filters.text & ~filters.command(['start', 'help']))
async def download_tiktok(client, message):
    url = message.text.strip()
    if "tiktok.com" not in url:
        await message.reply("❌ Please send a valid TikTok URL.")
        return

    msg_del = await message.reply("🔄 Processing your TikTok link. Please wait...")

    output_dir = "./downloads"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    try:
        scraper = TikTokScraper()
        video_path = scraper.download_video(url, output_dir)
        print("Downloaded video:", video_path)

        # Rename the video
        video_name = os.path.basename(video_path)
        new_video_name = f"tiktok_{video_name}"
        new_video_path = os.path.join(output_dir, new_video_name)
        os.rename(video_path, new_video_path)

        # Send the video to the user
        await client.send_video(
            chat_id=message.chat.id,
            video=new_video_path,
            caption=f"🎥 Downloaded via @{client.username}"
        )

        # Cleanup
        await msg_del.delete()
        os.remove(new_video_path)

    except Exception as e:
        await msg_del.delete()
        await message.reply(f"❌ An error occurred: {str(e)}")
        print("Error:", str(e))

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
