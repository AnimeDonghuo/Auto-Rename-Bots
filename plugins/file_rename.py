import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import codeflixbots
from helper.utils import get_file_name, progress_for_pyrogram

@Client.on_message(filters.private & filters.media)
async def rename_file(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if template is set
    template = await codeflixbots.get_format_template(user_id)
    if not template:
        await message.reply_text("🚫 You haven't set a renaming format. Use `/autorename` to set one.")
        return

    media = message.document or message.video or message.audio
    if not media:
        await message.reply_text("❌ Unsupported media type.")
        return

    # Determine input media type
    if message.document:
        media_type = "document"
    elif message.video:
        media_type = "video"
    elif message.audio:
        media_type = "audio"
    else:
        media_type = "document"

    # Get media metadata
    file_name = media.file_name or "Unknown"
    file_ext = os.path.splitext(file_name)[1]
    file_size = media.file_size

    # Format renaming template
    season = "01"
    episode = "01"
    quality = "720p"
    new_name = template.format(
        season=season,
        episode=episode,
        quality=quality
    )
    new_name_with_ext = f"{new_name}{file_ext}"

    # Download file
    msg = await message.reply_text("📥 **Downloading your file...**")
    download_path = f"./downloads/{new_name_with_ext}"
    try:
        file_path = await client.download_media(
            message=message,
            file_name=download_path,
            progress=progress_for_pyrogram,
            progress_args=("Downloading...", msg, time.time())
        )
    except Exception as e:
        await msg.edit(f"❌ Download error: `{e}`")
        return

    # Get user thumbnail if exists
    thumb_path = await codeflixbots.get_thumbnail(client, user_id)
    caption = f"**Renamed to:** `{new_name_with_ext}`\n\n⚡️ via Auto Rename Bot"

    # Get preferred media type
    preferred_media_type = await codeflixbots.get_media_preference(user_id)
    if preferred_media_type not in ["document", "video", "audio"]:
        preferred_media_type = media_type  # fallback

    # Upload file
    await msg.edit("📤 **Uploading renamed file...**")
    try:
        upload_args = dict(
            chat_id=message.chat.id,
            caption=caption,
            thumb=thumb_path,
            progress=progress_for_pyrogram,
            progress_args=("Uploading...", msg, time.time())
        )

        if preferred_media_type == "document":
            await client.send_document(document=file_path, **upload_args)
        elif preferred_media_type == "video":
            await client.send_video(video=file_path, **upload_args)
        elif preferred_media_type == "audio":
            await client.send_audio(audio=file_path, **upload_args)
        else:
            await client.send_document(document=file_path, **upload_args)

        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Upload error: `{e}`")

    # Clean up
    try:
        os.remove(file_path)
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
    except Exception:
        pass
