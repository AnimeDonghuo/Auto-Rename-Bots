from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

from Script import script
from database.users_chats_db import add_user, add_upload_mode


@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    user = message.from_user
    await add_user(user.id)

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 Set Upload Mode", callback_data="set_mode")],
            [InlineKeyboardButton("📢 Updates", url="https://t.me/YourChannel")],
        ]
    )

    await message.reply_text(
        text=script.START_TXT.format(user.mention),
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@Client.on_callback_query()
async def callback_query_handler(client: Client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "set_mode":
        mode_buttons = [
            [
                InlineKeyboardButton("📤 Document", callback_data="upload_doc"),
                InlineKeyboardButton("🎬 Video", callback_data="upload_vid"),
                InlineKeyboardButton("🎵 Audio", callback_data="upload_aud")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back_start")]
        ]

        await query.message.edit_text(
            "Please select your default upload mode:",
            reply_markup=InlineKeyboardMarkup(mode_buttons)
        )

    elif data in ["upload_doc", "upload_vid", "upload_aud"]:
        mode = {
            "upload_doc": "document",
            "upload_vid": "video",
            "upload_aud": "audio"
        }.get(data)

        await add_upload_mode(user_id, mode)
        await query.answer(f"Upload mode set to {mode.capitalize()} ✅", show_alert=True)

    elif data == "back_start":
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📝 Set Upload Mode", callback_data="set_mode")],
                [InlineKeyboardButton("📢 Updates", url="https://t.me/YourChannel")],
            ]
        )

        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
