import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import CallbackContext, filters
import yt_dlp
import os

# Bot Token (ඔබගේ Telegram bot API Key එකට වෙනස් කරන්න)
TOKEN = '7088491712:AAESfWxDn2_2IFg8xYD7Aa2j9fj3sHBjzPA'

async def start(update: Update, context: CallbackContext):
    # User එකට ආරම්භක පණිවිඩයක් ලබා දීම
    await update.message.reply_text("Hello! Send me a YouTube video link to download.")

async def download_video(update: Update, context: CallbackContext):
    url = update.message.text  # User එකේ URL එක ලබා ගැනීම
    await update.message.reply_text("Downloading video... Please wait.")

    try:
        # yt-dlp යොදාගෙන වීඩියෝව ඩවුන්ලෝඩ් කිරීම
        ydl_opts = {'format': 'best'}  # Best quality video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info_dict)
            ydl.download([url])

        # Download නිමාවට පසුව video එක පණිවිඩය සමඟ පරිශීලකයාට යවයි
        await update.message.reply_text(f"Download complete! Sending your video...")

        # Video එක user එකට යැවීම
        await update.message.reply_video(open(filename, 'rb'))

        # Video file එක delete කිරීම (optional)
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    # Bot Application එක නිර්මාණය කිරීම
    application = Application.builder().token(TOKEN).build()

    # Command handler එක add කිරීම
    application.add_handler(CommandHandler("start", start))

    # Message handler එක add කිරීම
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Bot එක පටන් ගන්නවා
    application.run_polling()

if __name__ == '__main__':
    main()
