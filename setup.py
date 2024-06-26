import time
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import threading
import os
from transmissionrpc import Client

# Configuration
TOKEN = '6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg'
CHANNEL_USERNAME = '-4111844983'  # Use the channel username or ID
MAIN_URL = 'https://www.1tamilmv.eu/'
FETCH_INTERVAL = 900  # Time in seconds to wait between fetches (15 minutes)
POSTED_MOVIES_FILE = 'posted_movies.txt'

# Initialize bot
bot = telebot.TeleBot(TOKEN)

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

# Inline keyboard setup
button1 = types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('👨‍💻 Developed by', url='https://github.com/shinas101')
).add(button1).add(button2).add(button3)
keyboard2 = types.InlineKeyboardMarkup().add(button2).add(button3)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello👋 \n\n🗳Get the latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please enter the */view* command and you'll get magnet links as well as links to torrent files 😌\n\nShare and Support💝",
        parse_mode='Markdown',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['view'])
def send_movie_list(message):
    bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
    fetch_movies()
    bot.send_message(
        chat_id=message.chat.id,
        text="Select a Movie from the list 🙂 : ",
        reply_markup=make_keyboard(),
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_movie_selection(call):
    bot.send_message(call.message.chat.id, text="Here's your Movie links 🎥", parse_mode='Markdown')
    movie_name = movie_list[int(call.data)]
    if movie_name in movie_links:
        for link in movie_links[movie_name]:
            bot.send_message(call.message.chat.id, text=f"{link}\n\n🤖 @Tamilmv_movie_bot", parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, text="No links available for the selected movie.", parse_mode='Markdown')
    bot.send_message(call.message.chat.id, text="🌐 Please Join Our Status Channel", parse_mode='Markdown', reply_markup=keyboard2)

def make_keyboard():
    markup = types.InlineKeyboardMarkup()
    for index, movie in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=movie, callback_data=str(index)))
    return markup

def fetch_movies():
    global movie_list, movie_links
    movie_list = []
    movie_links = {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    response = requests.get(MAIN_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    movie_entries = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

    for entry in movie_entries[:21]:
        title = entry.find('a').text.strip()
        link = entry.find('a')['href']
        movie_list.append(title)
        movie_links[title] = fetch_movie_links(link)

def fetch_movie_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    magnets = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('magnet')]
    torrents = [a['href'] for a in soup.find_all('a', {"data-fileext": "torrent"}, href=True)]
    titles = [a.find('span').text.strip() for a in soup.find_all('a') if a.find('span') and a.find('span').text.endswith('torrent')]

    movie_links = []
    for i, magnet in enumerate(magnets):
        title = titles[i] if i < len(titles) else "Unknown Title"
        torrent = torrents[i] if i < len(torrents) else "#"
        movie_links.append(f"/qbleech {magnet}\n*{title}* -->\n🗒️->[Torrent file]({torrent})")

        if title not in posted_movies:
            post_to_channel(title, magnet, torrent)
            posted_movies.add(title)
            save_posted_movies()

    return movie_links

def post_to_channel(title, magnet, torrent):
    try:
        download_torrent(torrent, title)
        # Post to channel logic can go here after download completes
    except Exception as e:
        print(f"Error posting to channel: {e}")

def download_torrent(torrent_url, title):
    # Transmission client setup
    tc = Client('localhost', port=9091, username='transmission', password='transmission')

    # Add torrent to transmission
    tc.add_torrent(torrent_url)

    # You can handle the download progress and completion logic here
    # For simplicity, this example just waits for a fixed time
    time.sleep(300)  # Simulating a 5-minute download

    # Assuming the torrent is downloaded to a specific directory
    # You can then proceed to post the downloaded file to Telegram

def fetch_and_post():
    while True:
        try:
            fetch_movies()
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
