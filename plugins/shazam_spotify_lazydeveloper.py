    # if re.search(instagram_regex, text):
    #     msg_del = await message.reply("⏳")
    #     app = FastDLAppDownloader()
    #     vid = app.download_url(text)
    #     if vid:
    #         try:
    #             await msg_del.delete()
    #             await bot.send_document(message.chat.id, vid, caption="Downloaded via @Ultimatedownbot")
    #             with open(f"{message.message_id}.mp4", 'wb') as video:
    #                 rrr = requests.get(vid)
    #                 video.write(rrr.content)
    #             input_file = types.InputFile(f"{message.message_id}.mp4")
    #             shazammusic = await shazamtop(f"{message.message_id}.mp4")
    #             title = shazammusic['title']
    #             if title is not None:
    #                 musics = SearchFromSpotify(track_name=title, limit=5)
    #                 audio_urls = DownloadMusic(musics)
    #             inline_kbs = types.InlineKeyboardMarkup()
    #             os.remove(f"{message.message_id}.mp4")


                    
                
    #         except Exception as err:
    #             with open(f"{message.message_id}.mp4", 'wb') as video:
    #                 rrr = requests.get(vid)
    #                 video.write(rrr.content)
    #             input_file = types.InputFile(f"{message.message_id}.mp4")
    #             await bot.send_document(message.chat.id, document=input_file,caption="Downloaded via @Ultimatedownbot")
    #             shazammusic = await shazamtop(f"{message.message_id}.mp4")
    #             title = shazammusic['title']


    #             os.remove(f"{message.message_id}.mp4")
            
    #         with open(f"{message.message_id}.mp4", 'wb') as video:
    #             rrr = requests.get(vid)
    #             video.write(rrr.content)
    #         shazammusic = await shazamtop(f"{message.message_id}.mp4")
    #         title = shazammusic['title']

    #         os.remove(f"{message.message_id}.mp4")
            

