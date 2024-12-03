import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import CallbackContext, filters
import yt_dlp
import os

TOKEN = '7088491712:AAESfWxDn2_2IFg8xYD7Aa2j9fj3sHBjzPA'

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a YouTube video link to download.")

async def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    await update.message.reply_text("Downloading video... Please wait.")
    retries = 3  # Number of retry attempts
    for _ in range(retries):
        try:
            ydl_opts = {'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info_dict)
                ydl.download([url])

            await update.message.reply_text(f"Download complete! Sending your video...")
            await update.message.reply_video(open(filename, 'rb'))

            os.remove(filename)
            break  # Break the loop if successful

        except Exception as e:
            await update.message.reply_text(f"An error occurred: {str(e)}")
            time.sleep(5)  # Wait for a few seconds before retrying

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.run_polling()

if __name__ == '__main__':
    main()
