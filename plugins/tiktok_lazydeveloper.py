from pyrogram import Client, filters, types
from pyrogram.types import Message
from io import BytesIO
import requests
import time
# from TikTokApi import TikTokApi
import os
# from tiktok_downloader import snaptik
import yt_dlp
import asyncio
import subprocess

from config import TEL_USERNAME

TEMP_DOWNLOAD_FOLDER = "downloads"
TELEGRAM_MAX_SIZE_MB = 200

if not os.path.exists(TEMP_DOWNLOAD_FOLDER):
    os.makedirs(TEMP_DOWNLOAD_FOLDER)

# Function to handle real-time download progress
async def download_progress(d, message):
    if d['status'] == 'downloading':
        percentage = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        # Update the progress by editing the same message
        if int(percentage) % 10 == 0:  # Update every 10% to avoid too many edits
            await message.edit_text(f"Download progress: {percentage:.2f}%")
    elif d['status'] == 'finished':
        await message.edit_text("Download complete, processing file...")

# Function to reduce video quality if it's too large using ffmpeg
def reduce_quality_ffmpeg(video_path, output_path, target_size_mb=50):
    try:
        # Command to reduce video quality using ffmpeg
        command = [
            'ffmpeg', '-i', video_path,
            '-b:v', '500k',  # Adjust the video bitrate (can be modified as needed)
            '-vf', 'scale=iw/2:ih/2',  # Reduce resolution by half
            '-c:a', 'aac',  # Encode audio with AAC
            '-b:a', '128k',  # Adjust the audio bitrate
            output_path
        ]

        # Execute the ffmpeg command
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reducing video quality with ffmpeg: {e}")
        return False

# Function to download videos or audios (YouTube, Twitter/X, and TikTok)
async def download_video(url, destination_folder, message, format="video"):
    try:
        # Determine the format
        if format == "audio":
            format_type = 'bestaudio/best'
            ext = 'mp3'
        else:
            format_type = 'best'
            ext = 'mp4'

        # yt-dlp configuration with progress_hooks
        options = {
            'outtmpl': f'{destination_folder}/%(id)s.%(ext)s',  # Use the video ID to avoid filename issues
            'format': format_type,  # Select the format based on user input
            'restrictfilenames': True,  # Limit special characters
            'progress_hooks': [lambda d: asyncio.create_task(download_progress(d, message))],  # Hook to show real-time progress
        }

        # Download the video or audio
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Error during download: {e}")
        return False


@Client.on_message(filters.private & filters.text & ~filters.command(['start', 'help']))
async def handle_tiktok_download(client: Client, message: Message):
    try:
        message_text = message.text.strip()
        print(message_text)
        
        # Check if the URL is a valid TikTok link
        # if "tiktok.com" not in url:
        #     await message.reply("❌ Please send a valid TikTok URL.")
        #     return
        
        # Inform the user about the processing
        msg_del = await message.reply("🔄 Processing your TikTok link. Please wait...")
        
        # Download video using tiktok_downloader (snaptik)
        
        bot_username = client.username if client.username else TEL_USERNAME
        caption_lazy = f".\nᴡɪᴛʜ ❤ @{bot_username}\n."

        # TEMP_DOWNLOAD_FOLDER = f"{message.from_user.id}_{time.time()}_ok.mp4"
        if any(domain in message_text for domain in ["https://www.youtube.com/", "https://youtu.be/", "https://twitter.com/", "https://x.com/", "https://www.tiktok.com/"]):
            # params = message_text.split(" ")
            # url = params[1]  # Extract the URL after the command
            url = message_text  # Extract the URL after the command
            format = "video" #if len(params) < 3 or params[2].lower() != "audio" else "audio"
            destination_folder = TEMP_DOWNLOAD_FOLDER  # Use the temporary download folder
            print(f"continue to download")
            # Send the initial message and keep it for updates
            message = await message.reply_text(f'Starting the {format} download from: {url}')

            # Start the download and update the same message
            success_download = await download_video(url, destination_folder, message, format)
            print(f"Download success")
            if not success_download:
                await message.edit_text('Error during the video download. Please try again later.')
                return

            # Get the name of the downloaded file
            video_filename = max([os.path.join(destination_folder, f) for f in os.listdir(destination_folder)], key=os.path.getctime)
            print(video_filename)
            # Check the file size
            file_size_mb = os.path.getsize(video_filename) / (1024 * 1024)
            if file_size_mb > TELEGRAM_MAX_SIZE_MB:
                await message.edit_text(f'The file is too large ({file_size_mb:.2f} MB). '
                                        f'Reducing the quality to meet the 50 MB limit...')

                # Attempt to reduce the quality using ffmpeg
                output_filename = os.path.join(destination_folder, 'compressed_' + os.path.basename(video_filename))
                success_reduce = reduce_quality_ffmpeg(video_filename, output_filename, TELEGRAM_MAX_SIZE_MB)

                if not success_reduce:
                    await message.edit_text('Error reducing the video quality. Please try again later.')
                    return

                # Switch to the compressed file for sending
                video_filename = output_filename

            # Send the video/audio file to the user
            await message.edit_text(f'Sending the {format}...')
            try:
                await message.reply_video(video=open(video_filename, 'rb'))
            except Exception as e:
                await message.edit_text(f'Error sending the file: {e}')
                print(f"Error sending the file: {e}")
            finally:
                # Delete the downloaded file (optional)
                if os.path.exists(video_filename):
                    os.remove(video_filename)
        else:
            await message.reply_text('Please provide a valid YouTube, Twitter/X, or TikTok URL.')



         # Download video using TikTokApi
        # try:
        #     # api = TikTokApi()
        #     video_data = api.video(url=url).bytes()  # Fetch video bytes
            
        #     # Downloading video using Pyrogram's `download` method
        #     video_file = BytesIO(video_data)
        #     video_file.name = f"{message.chat.id}/{time.time()}/tiktok_video.mp4"

        #     # Download video to file using Pyrogram
        #     # file = await client.download(video_data, file_name=video_file)

        #     # Send the downloaded video
        #     await client.send_video(
        #         chat_id=message.chat.id,
        #         video=video_file,
        #         caption=caption_lazy
        #     )
        #     # print(f"Video sent successfully: {video_path}")

        #     # Cleanup
        #     await msg_del.delete()
        #     # os.remove(video_path)

        # except Exception as e:
        #     print(f"Error: {e}")
        
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
