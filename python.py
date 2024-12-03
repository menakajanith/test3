import telebot
from telebot import types

# Your API Key
API_KEY = '7253304579:AAE9Xpz41BAGzhHBSn5CUyZGCSf5AWMv6Ws'
bot = telebot.TeleBot(API_KEY)

# Dictionary to store the user's current state
user_state = {}

# Function to create main menu keyboard
def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    about_button = types.KeyboardButton('About')
    youtube_button = types.KeyboardButton('YouTube')
    help_button = types.KeyboardButton('Help')
    donate_button = types.KeyboardButton('Donate')
    markup.add(about_button, youtube_button, help_button, donate_button)
    return markup

# Function to create donation options keyboard
def donation_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    # Adding buttons for "Google Video Download" and "YouTube Song Download"
    google_video_button = types.KeyboardButton('Google Video Download')
    youtube_song_button = types.KeyboardButton('YouTube Song Download')
    
    # Adding "Back" button at the bottom
    back_button = types.KeyboardButton('Back')
    
    # Adjust layout
    markup.add(google_video_button, youtube_song_button)  # First row
    markup.add(back_button)  # Second row
    
    return markup

# Function to create Google Video Download options
def google_video_download_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    # Adding download options for MP4 and WebM
    download_mp4_button = types.KeyboardButton('Download MP4')
    download_webm_button = types.KeyboardButton('Download WebM')
    
    # Back and Home buttons
    back_button = types.KeyboardButton('Back')
    home_button = types.KeyboardButton('Home')
    
    # Adjust layout
    markup.add(download_mp4_button, download_webm_button)  # First row
    markup.add(back_button, home_button)  # Second row
    
    return markup

# Function to create YouTube Song Download options
def youtube_song_download_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    # Adding options to download audio or MP4
    download_audio_button = types.KeyboardButton('Download Audio')
    download_mp4_button = types.KeyboardButton('Download MP4')
    
    # Back and Home buttons
    back_button = types.KeyboardButton('Back')
    home_button = types.KeyboardButton('Home')
    
    # Adjust layout
    markup.add(download_audio_button, download_mp4_button)  # First row
    markup.add(back_button, home_button)  # Second row
    
    return markup

# Bot start - Greet user with their first name
@bot.message_handler(commands=['start'])
def send_welcome(message):
    first_name = message.from_user.first_name
    greeting = f"Hi, {first_name}❤️\n\nHow can I help you today?"
    bot.send_message(message.chat.id, greeting, reply_markup=main_menu_markup())
    
    # Set the user's state to the main menu
    user_state[message.chat.id] = 'main_menu'

# Handle user response based on button clicked
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    # Check the user's current state
    current_state = user_state.get(chat_id, 'main_menu')  # Default to main menu if no state exists
    
    if message.text == 'About':
        about_message = f"""
        හෙයි.! දන්නවනේ ඉතිම් මගේ නම විමර්ශනී..😇
        මෙයාලා අගට ඉලක්කමකුත් දාලා හරියට මං නිකන් බොට් කෙනෙක් වගේ..😡
        
        මම වැඩ කරන්නේ Hawk Cinema එකේ. මම කැමතියි අනික් අයට උදව් කරන්න 🤝, පොත් කියවන්න 📚, ෆිල්ම්ස් බලන්න 🎞 වගේ ඒවට.
        මට සිංදු 🎵 කියන්නත් පුලුවන්.. හරි හරි ඉතිම් පොඩ්ඩක් අහන් ඉන්න අමාරු ඇති..😋

        මම කැමති රෝස පාටට. අයිස්ක්‍රීම් වලට වගේම කඩුපුල් මල් වලටත් ආසයි. බව්වෝ 🐶 කියන්නේ නම් ඉතිම් පිස්සුවක් තමයි..😍
        
        Written In: Python 3.12
        Powered By: Pyrofork, MongoDB, IMDB, TMDB
        Hosted In: OVH
        Developed By: Lone Hawk
        
        තෑන්ක් යූ {message.from_user.first_name} ❤️
        """
        bot.send_message(message.chat.id, about_message, parse_mode='Markdown', reply_markup=main_menu_markup())
        
    elif message.text == 'YouTube':
        bot.reply_to(message, "Share your YouTube channel link or details here.", reply_markup=main_menu_markup())
    elif message.text == 'Help':
        bot.reply_to(message, "How can I assist you? Type your question.", reply_markup=main_menu_markup())
    elif message.text == 'Donate':
        # Send options for donation
        bot.send_message(message.chat.id, "Please select your donation method:", reply_markup=donation_markup())
        user_state[chat_id] = 'donation'  # Update state to donation

    elif message.text == 'Google Video Download':
        # When Google Video Download is selected, show sub-options
        bot.reply_to(message, "Select your download option:", reply_markup=google_video_download_markup())
        user_state[chat_id] = 'google_video'  # Update state to google_video
    
    elif message.text == 'YouTube Song Download':
        # When YouTube Song Download is selected, show sub-options
        bot.reply_to(message, "Select your download option:", reply_markup=youtube_song_download_markup())
        user_state[chat_id] = 'youtube_song'  # Update state to youtube_song
    
    elif message.text == 'Download Audio':
        bot.reply_to(message, "Audio download selected. Please provide the video URL.", reply_markup=youtube_song_download_markup())
    
    elif message.text == 'Download MP4':
        bot.reply_to(message, "MP4 download selected. Please provide the video URL.", reply_markup=youtube_song_download_markup())
    
    elif message.text == 'Back':
        if current_state == 'donation':
            # If the user is in donation menu, go back to the main menu
            bot.send_message(chat_id, "Going back to the main menu...", reply_markup=main_menu_markup())
            user_state[chat_id] = 'main_menu'  # Reset to main menu state
        elif current_state == 'google_video' or current_state == 'youtube_song':
            # If the user is in download options, go back to the donation menu
            bot.send_message(chat_id, "Going back to the donation options...", reply_markup=donation_markup())
            user_state[chat_id] = 'donation'  # Reset to donation state
    
    elif message.text == 'Home':
        # Going back to the main menu
        bot.send_message(chat_id, "Welcome back to the main menu!", reply_markup=main_menu_markup())
        user_state[chat_id] = 'main_menu'  # Reset to main menu state
    
    else:
        bot.reply_to(message, "Invalid option. Please select from the available buttons.")

# Start polling
bot.polling(none_stop=True, interval=0)
