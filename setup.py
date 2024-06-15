import os
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ.get('6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg')  # Use environment variable for token

bot = telebot.TeleBot(TOKEN)

# Keyboard buttons setup
button1 = types.InlineKeyboardButton(text="⚡ Powered by", url='https://t.me/heyboy2004')
button2 = types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('👨‍💻 Developed by', url='https://github.com/shinas101')
).add(button1).add(button2).add(button3)
keyboard2 = types.InlineKeyboardMarkup().add(button2).add(button3)

# Handler for /start command
@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=(
            "Hello👋 \n\n🗳 Get latest Movies from 1Tamilmv\n\n⚙️ *How to use me??* 🤔\n\n"
            "✯ Please Enter */view* command and you'll get magnet link as well as a link to the torrent file 😌\n\n"
            "Share and Support💝"
        ),
        parse_mode='Markdown',
        reply_markup=keyboard
    )

# Handler for /view command
@bot.message_handler(commands=['view'])
def start(message):
    bot.send_message(message.chat.id, text="Fetching latest movies, please wait...")
    movie_list, real_dict = fetch_movies()
    
    if not movie_list:
        bot.send_message(message.chat.id, text="No movies found at the moment. Please try again later.")
        return
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Select a Movie from the list 🙂 : ",
        reply_markup=makeKeyboard(movie_list),
        parse_mode='HTML'
    )

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    movie_list, real_dict = fetch_movies()
    
    if call.data.isdigit() and int(call.data) < len(movie_list):
        movie_title = movie_list[int(call.data)]
        if movie_title in real_dict:
            bot.send_message(call.message.chat.id, text=f"Here are the links for '{movie_title}':", parse_mode='markdown')
            for link in real_dict[movie_title]:
                bot.send_message(call.message.chat.id, text=link, parse_mode='markdown')
        else:
            bot.send_message(call.message.chat.id, text="No links found for this movie.")
    else:
        bot.send_message(call.message.chat.id, text="Invalid selection. Please select a valid movie.")

    bot.send_message(call.message.chat.id, text="🌐 Please Join Our Status Channel", parse_mode='markdown', reply_markup=keyboard2)

# Function to create inline keyboard markup
def makeKeyboard(movie_list):
    markup = types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value, callback_data=str(key)))
    return markup

# Function to fetch movies from 1TamilMV website
def fetch_movies():
    mainUrl = 'https://www.1TamilMV.eu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        web = requests.get(mainUrl, headers=headers)
        soup = BeautifulSoup(web.text, 'lxml')  # Ensure 'lxml' parser is used

        linker = []
        real_dict = {}
        movie_list = []

        temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

        for i in range(min(21, len(temps))):
            title = temps[i].findAll('a')[0].text.strip()
            links = temps[i].find('a')['href']
            linker.append(links)

        num = 0

        for url in linker:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')

            alltitles = []
            mag = []
            filelink = []

            for i in soup.find_all('a', href=True):
                if i['href'].startswith('magnet'):
                    mag.append(i['href'])

            for a in soup.findAll('a', {"data-fileext": "torrent", 'href': True}):
                filelink.append(a['href'])

            for title in soup.find_all('a'):
                if title.find('span') is not None:
                    if title.find('span').text.endswith('torrent'):
                        alltitles.append(title.find('span').text[19:-8])

            try:
                real_dict.setdefault(title, [])
                for p in range(len(mag)):
                    real_dict[title].append(
                        f"*{alltitles[p]}* -->\n🧲 `{mag[p]}`\n🗒️->[Torrent file]({filelink[p]})"
                    )
                movie_list.append(title)
            except IndexError:
                pass

            num += 1

        return movie_list, real_dict

    except Exception as e:
        print(f"Error fetching movies: {e}")
        return [], {}

# Main function to start the bot
def main():
    try:
        bot.polling(none_stop=True)  # Start the bot and continue polling
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()
    
