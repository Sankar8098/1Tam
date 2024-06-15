import time
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import threading
import os

# Configuration
TOKEN = '6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg'
CHANNEL_USERNAME = '-4111844983'  # Use the channel username or ID
MAIN_URL = 'https://www.1tamilmv.eu/'
FETCH_INTERVAL = 900  # Time in seconds to wait between fetches (15 minutes)
POSTED_MOVIES_FILE = 'posted_movies.txt'

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Global dictionaries and lists
movie_dict = {}
real_dict = {}
movie_list = []

# Load posted movies from file
def load_posted_movies():
    if os.path.exists(POSTED_MOVIES_FILE):
        with open(POSTED_MOVIES_FILE, 'r') as file:
            return set(line.strip() for line in file)
    return set()

posted_movies = load_posted_movies()

# Save posted movies to file
def save_posted_movies():
    with open(POSTED_MOVIES_FILE, 'w') as file:
        for movie in posted_movies:
            file.write(f"{movie}\n")

# Keyboard for messages
button1 = types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('👨‍💻 Developed by', url='https://github.com/shinas101')
).add(button1).add(button2).add(button3)
keyboard2 = types.InlineKeyboardMarkup().add(button2).add(button3)

@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello👋 \n\n🗳Get the latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please enter the */view* command and you'll get magnet links as well as links to torrent files 😌\n\nShare and Support💝",
        parse_mode='Markdown',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['view'])
def start(message):
    bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
    tamilmv()
    bot.send_message(
        chat_id=message.chat.id,
        text="Select a Movie from the list 🙂 : ",
        reply_markup=makeKeyboard(),
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.send_message(call.message.chat.id, text="Here's your Movie links 🎥", parse_mode='Markdown')
    if call.data.isdigit() and int(call.data) < len(movie_list):
        movie_name = movie_list[int(call.data)]
        if movie_name in real_dict:
            for i in real_dict[movie_name]:
                bot.send_message(call.message.chat.id, text=f"{i}\n\n🤖 @Tamilmv_movie_bot", parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, text="No links available for the selected movie.", parse_mode='Markdown')
    bot.send_message(call.message.chat.id, text="🌐 Please Join Our Status Channel", parse_mode='Markdown', reply_markup=keyboard2)

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value, callback_data=f"{key}"))
    return markup

def tamilmv():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    global movie_dict, real_dict, movie_list
    movie_dict = {}
    real_dict = {}
    movie_list = []

    web = requests.get(MAIN_URL, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')
    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

    linker = []
    badtitles = []

    for i in range(min(21, len(temps))):
        title = temps[i].findAll('a')[0].text.strip()
        badtitles.append(title)
        links = temps[i].find('a')['href']
        linker.append(links)

    movie_list = badtitles[:]
    num = 0

    for url in linker:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        mag = [i['href'] for i in soup.find_all('a', href=True) if i['href'].startswith('magnet')]
        filelink = [a['href'] for a in soup.findAll('a', {"data-fileext": "torrent"}, href=True)]
        alltitles = [title.find('span').text.strip() for title in soup.find_all('a') if title.find('span') and title.find('span').text.endswith('torrent')]

        for p in range(len(mag)):
            try:
                real_dict.setdefault(movie_list[num], [])
                formatted_title = alltitles[p] if p < len(alltitles) else "Unknown Title"
                formatted_filelink = filelink[p] if p < len(filelink) else "#"
                real_dict[movie_list[num]].append(
                    f"/qbleech {mag[p]}\n*{formatted_title}* -->\n🗒️->[Torrent file]({formatted_filelink})"
                )
                # Automatically post to the channel if the movie is not already posted
                if formatted_title not in posted_movies:
                    post_to_channel(formatted_title, mag[p], formatted_filelink)
                    posted_movies.add(formatted_title)
                    save_posted_movies()
            except IndexError as e:
                print(f"IndexError: {e}")
            except Exception as e:
                print(f"Error: {e}")

        num += 1

def post_to_channel(title, magnet, filelink):
    try:
        print(f"Posting to channel: {title}")
        bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=f"/qbleech {magnet}\n*{title}* -->\n🗒️->[Torrent file]({filelink})",
            parse_mode='Markdown'
        )
        # Send the /qbleech command separately to ensure it's executed
        print(f"Sending /qbleech command: {magnet}")
        bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=f"/qbleech {magnet}",
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error posting to channel: {e}")

def fetch_and_post():
    while True:
        try:
            tamilmv()
            print("Fetched and posted new movies.")
        except Exception as e:
            print(f"Error during fetch and post: {e}")
        time.sleep(FETCH_INTERVAL)

def main():
    fetch_thread = threading.Thread(target=fetch_and_post)
    fetch_thread.start()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    main()
                
