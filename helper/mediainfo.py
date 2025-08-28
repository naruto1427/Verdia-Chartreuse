from pymediainfo import MediaInfo
from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name="rename_bot")

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

def upload_to_telegraph(title, content):
    response = telegraph.create_page(
        title=title,
        html_content=f"<pre>{content}</pre>"
    )
    return f"https://telegra.ph/{response['path']}"
