class script(object):

    START_MSG = """👋 Hello {}!

I'm a File Renamer Bot with features like:
➤ Rename Files
➤ Upload as Video or Document
➤ Custom Thumbnail Support

Just send me a file to get started!
"""

    HELP_MSG = """🛠 **How to Use Me:**

1. Send me any file.
2. I’ll ask you for a new file name.
3. Choose how you want to upload:
   ➤ As Document
   ➤ As Video
   ➤ Or Cancel

📌 **Commands:**
/start – Restart the bot  
/help – Show this help  
/about – Bot information  
"""

    ABOUT_MSG = """📖 **About This Bot:**

🤖 **Bot Name:** File Renamer Bot  
👨‍💻 **Developer:** [YourNameHere](https://t.me/YourUsername)  
📚 **Library:** Pyrogram  
💻 **Language:** Python 3  
🗃 **Features:** Rename | Convert | Custom Thumbnails  
"""

    # Optional keyboard button text layout, if you're using inline buttons
    BUTTONS = {
        "start": [["Help", "About"]],
        "help": [["Back", "About"]],
        "about": [["Back", "Help"]]
    }
