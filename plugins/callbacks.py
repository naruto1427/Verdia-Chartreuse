import os
from pyrogram import Client
from helpers.mediainfo import get_media_info, upload_to_telegraph

@Client.on_callback_query()
async def cb_handler(client, query):
    data = query.data.split(":", 1)

    if data[0] == "mediainfo":
        msg = await query.message.reply("⏳ Extracting mediainfo...")
        file_path = await query.message.download()
        try:
            info_text = get_media_info(file_path)
            link = upload_to_telegraph("Media Info", info_text)
            await msg.edit(f"✅ MediaInfo uploaded:\n\n[📑 View Here]({link})", disable_web_page_preview=False)
        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    elif data[0] == "rename":
        await query.message.reply_text("✏️ Send me the new file name:")
        # continue rename flow here
