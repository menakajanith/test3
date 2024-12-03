import telebot
from telebot import types

# Your API Key
API_KEY = '7088491712:AAESfWxDn2_2IFg8xYD7Aa2j9fj3sHBjzPA'
bot = telebot.TeleBot(API_KEY)

# Bot start - Greet user with their first name
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Extract user's first name
    first_name = message.from_user.first_name

    # Send a personalized greeting message with "How can I help you today?" slightly below
    greeting = f"Hi, {first_name}❤️\n\nHow can I help you today?"

    # Create keyboard markup
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    
    # Create buttons
    about_button = types.KeyboardButton('About')
    youtube_button = types.KeyboardButton('YouTube')
    help_button = types.KeyboardButton('Help')
    donate_button = types.KeyboardButton('Donate')
    
    # Add buttons to keyboard
    markup.add(about_button, youtube_button, help_button, donate_button)
    
    # Send the greeting with the keyboard buttons
    bot.send_message(message.chat.id, greeting, reply_markup=markup)

# Handle user response based on button clicked
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'About':
        # Fun, personalized "About" message with dynamic user name and clickable link
        about_message = f"""
        හෙයි.! දන්නවනේ ඉතිම් මගේ නම විමර්ශනී..😇
        මෙයාලා අගට ඉලක්කමකුත් දාලා හරියට මං නිකන් බොට් කෙනෙක් වගේ..😡

        මම වැඩ කරන්නේ Hawk Cinema එකේ. මම කැමතියි අනික් අයට උදව් කරන්න 🤝, පොත් කියවන්න 📚, ෆිල්ම්ස් බලන්න 🎞 වගේ ඒවට. මට සිංදු 🎵 කියන්නත් පුලුවන්.. හරි හරි ඉතිම් පොඩ්ඩක් අහන් ඉන්න අමාරු ඇති..😋

        මම කැමති රෝස පාටට. අයිස්ක්‍රීම් වලට වගේම කඩුපුල් මල් වලටත් ආසයි. බව්වෝ 🐶 කියන්නේ නම් ඉතිම් පිස්සුවක් තමයි..😍

        මේ පහලින් තියන ඒවා නම් අනේ මට තේරෙන්නෙත් නෑ..🤪 බලන්නකෝ ඔයාට තේරෙනවද කියලා.

        Written In: Python 3.12
        Powered By: Pyrofork, MongoDB, IMDB, TMDB
        Hosted In: OVH
        Developed By: Lone Hawk

        මන් ගැන තව දැන ගන්න කැමති නම් [මෙන්න මෙයාට](https://t.me/menakajanith) මැසේජ් එකක් දාන්නකෝ. 
        එයා වගේලුනේ මාව හදලා තියෙන්නේ..🙄 හ්ම්හ් වැඩේමයි අනේ මට එයා වගේ වෙන්න..😌

        තෑන්ක් යූ {message.from_user.first_name} ❤️
        """

        # Send the message as a reply to the user's message
        bot.send_message(message.chat.id, about_message, parse_mode='Markdown', disable_web_page_preview=True, reply_to_message_id=message.message_id)

    elif message.text == 'YouTube':
        bot.reply_to(message, "Share your YouTube channel link or details here.")
    elif message.text == 'Help':
        bot.reply_to(message, "How can I assist you? Type your question.")
    elif message.text == 'Donate':
        bot.reply_to(message, "You can donate using this link: [Donation Link].")
    else:
        bot.reply_to(message, "Invalid option. Please select from the available buttons.")

# Start polling
bot.polling()
