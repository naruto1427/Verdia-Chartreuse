import os
from pyrogram import Client
from pymediainfo import MediaInfo
from telegraph import Telegraph


# Initialize Telegraph only once
telegraph = Telegraph()
telegraph.create_account(short_name="rename_bot")


# Function to extract mediainfo
def get_media_info(file_path):
    media_info = MediaInfo.parse(file_path)
    info_text = ""
    for track in media_info.tracks:
        if track.track_type == "General":
            info_text += f"📂 File: {track.file_name}\n"
            info_text += f"💾 Size: {round(track.file_size/1024/1024, 2)} MB\n"
            info_text += f"⏱ Duration: {round(track.duration/1000, 2)} sec\n"
        elif track.track_type == "Video":
            info_text += "\n🎥 Video:\n"
            info_text += f" • Codec: {track.codec}\n"
            info_text += f" • Resolution: {track.width}x{track.height}\n"
            info_text += f" • Bitrate: {track.bit_rate}\n"
        elif track.track_type == "Audio":
            info_text += "\n🔊 Audio:\n"
            info_text += f" • Codec: {track.codec}\n"
            info_text += f" • Channels: {track.channel_s}\n"
            info_text += f" • Sampling rate: {track.sampling_rate}\n"
    return info_text or "No media information found."


# Function to upload to Telegraph
def upload_to_telegraph(title, content):
    response = telegraph.create_page(
        title=title,
        html_content=f"<pre>{content}</pre>"
    )
    return f"https://telegra.ph/{response['path']}"


# Callback query handler
@Client.on_callback_query()
async def cb_handler(client, query):
    data = query.data.split(":", 1)

    if data[0] == "mediainfo":
        msg = await query.message.reply("⏳ Extracting mediainfo...")
        file_path = await query.message.download()
        try:
            info_text = get_media_info(file_path)
            link = upload_to_telegraph("Media Info", info_text)
            await msg.edit(
                f"✅ MediaInfo uploaded:\n\n[📑 View Here]({link})",
                disable_web_page_preview=False
            )
        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    elif data[0] == "rename":
        await query.message.reply_text("✏️ Send me the new file name:")
        # Continue your rename flow here (Pyromod ask)
