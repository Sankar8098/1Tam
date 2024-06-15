# setup.py

import os
import requests
import re
from bs4 import BeautifulSoup
import telebot
from telebot import types
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired logging level

TOKEN = os.getenv('')  # Retrieve your bot token from environment variables
if TOKEN is None:
    raise ValueError("Telegram bot token (TOKEN) not found. Make sure it's set as an environment variable.")

bot = telebot.TeleBot(TOKEN)

# Define inline keyboard buttons
button1 = types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('👨‍💻 Developed by', url='github.com/shinas101')).add(button1).add(button2).add(button3)
keyboard2 = types.InlineKeyboardMarkup().add(button2).add(button3)

# Handler for /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(chat_id=message.chat.id,
                     text=f"Hello👋 \n\n🗳 Get latest Movies from 1Tamilmv\n\n⚙️ *How to use me??* 🤔\n\n"
                          f"✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\n"
                          f"Share and Support💝", parse_mode='Markdown', reply_markup=keyboard)

# Handler for /view command
@bot.message_handler(commands=['view'])
def handle_view(message):
    try:
        bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
        movie_links = fetch_movie_links()
        if movie_links:
            bot.send_message(chat_id=message.chat.id,
                             text="Select a Movie from the list 🙂 : ",
                             reply_markup=make_keyboard(movie_links),
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Sorry, unable to fetch movie links right now. Please try again later.")
    except Exception as e:
        logging.error(f"Exception in handle_view: {e}", exc_info=True)
        bot.send_message(chat_id=message.chat.id,
                         text="Sorry, something went wrong while fetching movie links. Please try again later.")

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        bot.send_message(call.message.chat.id, text=f"Here's your Movie links 🎥 ", parse_mode='markdown')
        selected_movie = call.data
        if selected_movie in movie_dict:
            for link in movie_dict[selected_movie]:
                bot.send_message(call.message.chat.id, text=link, parse_mode='markdown')
        bot.send_message(call.message.chat.id, text="🌐 Please Join Our Status Channel", parse_mode='markdown', reply_markup=keyboard2)
    except Exception as e:
        logging.error(f"Exception in handle_callback_query: {e}", exc_info=True)
        bot.send_message(call.message.chat.id, text="Sorry, something went wrong. Please try again later.")

# Function to fetch movie links from 1TamilMV website
def fetch_movie_links():
    try:
        mainUrl = 'https://www.1TamilMV.eu/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        response = requests.get(mainUrl, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        movie_links = {}

        for link in soup.find_all('a', href=True):
            if link['href'].startswith('https://www.1TamilMV.eu/movie/'):
                movie_title = link.text.strip()
                movie_url = link['href']
                movie_links[movie_title] = movie_url

        return movie_links

    except Exception as e:
        logging.error(f"Exception in fetch_movie_links: {e}", exc_info=True)
        return None

# Function to create inline keyboard
def make_keyboard(movie_links):
    markup = types.InlineKeyboardMarkup()

    for title, url in movie_links.items():
        markup.add(types.InlineKeyboardButton(text=title, callback_data=title))

    return markup

# Start polling
def main():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    main()
