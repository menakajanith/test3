import os
import logging
from pytube import YouTube
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = '7253304579:AAE9Xpz41BAGzhHBSn5CUyZGCSf5AWMv6Ws'

# Function to start the bot
def start(update: Update, context):
    update.message.reply_text('Welcome! Send me a YouTube link to download the video.')

# Function to handle YouTube link
def handle_message(update: Update, context):
    url = update.message.text
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        
        # Create a list of available resolutions
        keyboard = [
            [InlineKeyboardButton(f"{stream.resolution}", callback_data=stream.itag) for stream in streams]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Choose a resolution:", reply_markup=reply_markup)

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Callback function to handle resolution selection
def button(update: Update, context):
    query = update.callback_query
    itag = query.data
    query.answer()

    try:
        # Fetch the YouTube video stream by itag
        yt = YouTube(query.message.text)
        stream = yt.streams.get_by_itag(itag)

        # Download the video
        query.message.reply_text("Downloading the video, please wait...")
        video_file = stream.download()

        # Send the video file back to the user
        query.message.reply_video(video=open(video_file, 'rb'))

        # Remove the downloaded file from the server
        os.remove(video_file)

    except Exception as e:
        query.message.reply_text(f"Error: {e}")

# Error handler function
def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Main function to run the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
