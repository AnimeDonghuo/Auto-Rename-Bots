from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant
from config import Config
from Script import script
from database.users_chats_db import add_user, add_upload_mode

# Start command
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await add_user(message.from_user.id)
    
    if Config.UPDATE_CHANNEL:
        try:
            user = await client.get_chat_member(Config.UPDATE_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await message.reply_text("🚫 You are Banned from using me.")
                return
        except UserNotParticipant:
            buttons = [[InlineKeyboardButton("📢 Join Updates Channel", url=f"https://t.me/{Config.UPDATE_CHANNEL}")]]
            await message.reply_text("📢 Please join my update channel to use me!", reply_markup=InlineKeyboardMarkup(buttons))
            return

    buttons = [
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Anime_Donghua")],
        [InlineKeyboardButton("📁 Set Upload Mode", callback_data="setmedia")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about"), InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    await message.reply_text(
        text=script.START_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# Help Button
@Client.on_callback_query(filters.regex("help"))
async def help_cb(client, query: CallbackQuery):
    await query.message.edit_text(
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
    )

# About Button
@Client.on_callback_query(filters.regex("about"))
async def about_cb(client, query: CallbackQuery):
    await query.message.edit_text(
        text=script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
    )

# Start Button
@Client.on_callback_query(filters.regex("start"))
async def restart_cb(client, query: CallbackQuery):
    buttons = [
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Anime_Donghua")],
        [InlineKeyboardButton("📁 Set Upload Mode", callback_data="setmedia")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about"), InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    await query.message.edit_text(
        text=script.START_TXT.format(query.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# Upload Mode Selection Button
@Client.on_callback_query(filters.regex("setmedia"))
async def setmedia_cb(client, query: CallbackQuery):
    buttons = [
        [InlineKeyboardButton("📂 Document", callback_data="upload:document")],
        [InlineKeyboardButton("🎬 Video", callback_data="upload:video")],
        [InlineKeyboardButton("🎵 Audio", callback_data="upload:audio")],
        [InlineKeyboardButton("🔙 Back", callback_data="start")]
    ]
    await query.message.edit_text(
        text="🔘 Choose your default upload type:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Save Upload Mode Choice
@Client.on_callback_query(filters.regex("upload:(document|video|audio)"))
async def save_upload_mode(client, query: CallbackQuery):
    mode = query.data.split(":")[1]
    await add_upload_mode(query.from_user.id, mode)
    await query.answer(f"✅ Upload mode set to {mode.title()}", show_alert=True)
