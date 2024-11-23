from pyrogram import Client, filters, types
from pyrogram.types import Message
from tiktok_downloader import snaptik
from io import BytesIO
import requests
import time


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
        
        # Download video using tiktok_downloader (snaptik)
        try:
            res = snaptik(url)
            # video_url = res[0].download()  # Get the download URL directly without saving to disk
            # lazydevelopercaption = res[0].caption  # Get the caption of the video
        except Exception as e:
            await message.reply(f"❌ Failed to download the video: {e}")
            return
        
        bot_username = client.username if client.username else TEL_USERNAME
        caption_lazy = f".\nᴡɪᴛʜ ❤ @{bot_username}\n."

        if res:
            try:
                path = f"{message.chat.id}_{time.time()}_downloadedby_@{client.username}.mp4"
                print(res)
                
                # Attempt to download using library's method
                video_url = res[0].download(path)
                if video_url:
                    print(f"Video downloaded successfully: {video_url}")
                else:
                    # Fallback: Attempt manual download
                    video_url = res[0].video_url  # Adjust based on actual response
                    print(f"Manual Download - Video URL: {video_url}")
                    
                    # Download video content
                    response = requests.get(video_url, stream=True)
                    if response.status_code == 200:
                        video_bytes = BytesIO(response.content)
                        video_bytes.name = path  # Set the file name for Pyrogram
                        await client.send_video(message.chat.id, video_bytes, caption=caption_lazy)
                    else:
                        print(f"Failed to download video, status code: {response.status_code}")
                    return  # Exit function after fallback

                # Send video using path (if library download works)
                print(f"trying alterate method")
                await client.send_video(message.chat.id, path, caption=caption_lazy)
            
            except Exception as e:
                print(f"Error occurred: {e}")

            # xlaxyx = await client.send_document(
            #     chat_id=message.chat.id,
            #     document=input_file,
            #     caption=caption_lazy  # Add the caption of the TikTok video
            # )

        # lazy_caption = lazydevelopercaption
        # while len(lazy_caption) + len(caption_lazy) > 1024:
        #     lazy_caption = lazy_caption[:-1]  # Trim caption if it's too long
        # lazy_caption = lazy_caption + caption_lazy
        
        # Fetch the video content as a stream
        # response = requests.get(video_url, stream=True)
        # if response.status_code != 200:
        #     await message.reply("❌ Failed to fetch the video.")
        #     return
        
        # Create an in-memory file using BytesIO
        # video_bytes = BytesIO(response.content)
        # video_bytes.name = f"{message.chat.id}_{time.time()}_downloadedby_@{client.username}.mp4" 
        
        # Send the video and caption directly from memory
        # input_file = types.InputMediaDocument(media=video_bytes, caption=caption_lazy)
        # await msg_del.delete()
        
        # If there is a caption, send it with the video
       
        # xlaxyx = await client.send_document(
        #         chat_id=message.chat.id,
        #         document=input_file,
        #         caption=caption_lazy  # Add the caption of the TikTok video
        #     )
        
        
    except Exception as e:
        await message.reply(f"❌ An unexpected error occurred: {e}")
