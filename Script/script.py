from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class script:
    START_TXT = "Hi {}, I am Auto Rename Bot.\nSend me any file and I will rename it for you!"
    HELP_TXT = "Send any file to rename.\nUse buttons to set format or mode.\nJoin update channel to use this bot."
    ABOUT_TXT = "🤖 Bot: Auto Rename Bot\n👨‍💻 Dev: @YourUsername\n📦 Library: Pyrogram\n🗄️ Language: Python"

    START_BUTTONS = InlineKeyboardMarkup([
        [InlineKeyboardButton("Set Media Format", callback_data="media")],
        [InlineKeyboardButton("Help", callback_data="help"), InlineKeyboardButton("About", callback_data="about")],
    ])

    HELP_BUTTONS = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data="start")],
        [InlineKeyboardButton("Close", callback_data="close")],
    ])

    ABOUT_BUTTONS = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data="start")],
        [InlineKeyboardButton("Close", callback_data="close")],
    ])

    MEDIA_BUTTONS = InlineKeyboardMarkup([
        [InlineKeyboardButton("Document", callback_data="set_doc"),
         InlineKeyboardButton("Video", callback_data="set_vid"),
         InlineKeyboardButton("Audio", callback_data="set_aud")],
        [InlineKeyboardButton("Back", callback_data="start")],
    ])
