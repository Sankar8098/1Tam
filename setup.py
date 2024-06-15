from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
import re
import os
import telebot

TOKEN = os.getenv('6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg')  # Retrieve Telegram token from environment variables

bot = telebot.TeleBot(TOKEN)

# Inline keyboard buttons
button1 = InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('👨‍💻 Developed by', url='https://github.com/shinas101')).add(button1).add(button2).add(button3)
keyboard2 = InlineKeyboardMarkup().add(button2).add(button3)

# Handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Hello! Welcome to 1Tamilmv bot. Use /view to get latest movie links.",
                     reply_markup=keyboard)

# Handler for /view command
@bot.message_handler(commands=['view'])
def view(message):
    bot.send_message(message.chat.id, text="Please wait for a moment while we fetch the latest movies...")
    movies = fetch_latest_movies()
    if movies:
        bot.send_message(chat_id=message.chat.id,
                         text="Select a Movie from the list:",
                         reply_markup=make_keyboard(movies))
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Sorry, could not fetch movies at the moment. Please try again later.")

# Function to fetch latest movies from 1TamilMV
def fetch_latest_movies():
    try:
        mainUrl = 'https://www.1TamilMV.eu/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        response = requests.get(mainUrl, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_list = []
        for link in soup.find_all('a'):
            if link.get('href') and link.text:
                movie_list.append((link.text, link.get('href')))
        return movie_list[:10]  # Return only the top 10 movies
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return None

# Function to create inline keyboard markup with movie options
def make_keyboard(movies):
    markup = InlineKeyboardMarkup()
    for idx, movie in enumerate(movies):
        markup.add(InlineKeyboardButton(text=movie[0], callback_data=f"movie_{idx}"))
    return markup

# Handler for callback queries from inline keyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        movies = fetch_latest_movies()
        movie_index = int(call.data.split('_')[1])
        selected_movie = movies[movie_index]
        bot.send_message(call.message.chat.id, text=f"Here's your selected movie: {selected_movie[0]}")
        bot.send_message(call.message.chat.id, text=f"Movie URL: {selected_movie[1]}")
        bot.send_message(call.message.chat.id, text="Please Join Our Status Channel", reply_markup=keyboard2)
    except Exception as e:
        print(f"Error handling callback query: {e}")

# Polling method to keep the bot running
def main():
    print("Bot started polling...")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
    
