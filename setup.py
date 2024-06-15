from asyncio import events
import telebot
from telebot import types
import requests
import re
from bs4 import BeautifulSoup

TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = telebot.TeleBot(TOKEN)

# Define your channel ID where you want to post updates
channel_id = 'YOUR_CHANNEL_ID_HERE'

# Keyboard buttons setup
button1 = telebot.types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = telebot.types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = telebot.types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('👨‍💻 Developed by', url='https://github.com/shinas101')
).add(button1).add(button2).add(button3)
keyboard2 = telebot.types.InlineKeyboardMarkup().add(button2).add(button3)

# Handler for /start command
@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=(
            "Hello👋 \n\n🗳Get latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n"
            "✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\n"
            "Share and Support💝"
        ),
        parse_mode='Markdown',
        reply_markup=keyboard
    )

# Handler for /view command
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

# Callback query handler
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.send_message(call.message.chat.id, text="Here's your Movie links 🎥 ", parse_mode='markdown')
    for key, value in enumerate(movie_list):
        if call.data == f"{key}":
            if movie_list[int(call.data)] in real_dict.keys():
                for item in real_dict[movie_list[int(call.data)]]:
                    bot.send_message(call.message.chat.id, text=item, parse_mode='markdown')
    bot.send_message(call.message.chat.id, text="🌐 Please Join Our Status Channel", parse_mode='markdown', reply_markup=keyboard2)

# Function to create inline keyboard markup
def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value, callback_data=f"{key}"))
    return markup

# Function to scrape 1TamilMV website and fetch movie details
def tamilmv():
    mainUrl = 'https://www.1TamilMV.eu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    web = requests.get(mainUrl, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')

    linker = []
    global real_dict
    real_dict = {}
    global movie_list
    movie_list = []

    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

    for i in range(21):
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
            real_dict.setdefault(movie_list[num], [])
            for p in range(len(mag)):
                real_dict[movie_list[num]].append(
                    f"*{alltitles[p]}* -->\n🧲 `{mag[p]}`\n🗒️->[Torrent file]({filelink[p]})"
                )
        except IndexError:
            pass

        num += 1

# Main function to start the bot
def main():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    main()
                           
