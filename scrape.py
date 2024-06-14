import asyncio
import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import re

TOKEN = '6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg'

bot = telebot.TeleBot(TOKEN)

# Define your inline keyboard buttons
button1 = types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('👨‍💻 Developed by', url='github.com/shinas101')).add(button1).add(button2).add(button3)
keyboard2 = types.InlineKeyboardMarkup().add(button2).add(button3)

# Define callback query handler
@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(chat_id=message.chat.id, text=f"Hello👋 \n\n🗳 Get latest Movies from 1Tamilmv\n\n⚙️ *How to use me??*🤔\n\n✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\nShare and Support💝", parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=['view'])
def start(message):
    bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
    loop = asyncio.get_event_loop()
    loop.create_task(fetch_and_send_movies(message.chat.id))  # Execute the coroutine task

async def fetch_and_send_movies(chat_id):
    await tamilmv()
    await bot.send_message(chat_id=chat_id, text="Select a Movie from the list 🙂 : ", reply_markup=makeKeyboard(), parse_mode='HTML')

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.send_message(call.message.chat.id, text=f"Here's your Movie links 🎥 ", parse_mode='markdown')
    for key, value in enumerate(movie_list):
        if call.data == f"{key}":
            if movie_list[int(call.data)] in real_dict.keys():
                for i in real_dict[movie_list[int(call.data)]]:
                    bot.send_message(call.message.chat.id, text=f"{i}\n\n🤖 @Tamilmv_movie_bot", parse_mode='markdown')
    bot.send_message(call.message.chat.id, text=f"🌐 Please Join Our Status Channel", parse_mode='markdown', reply_markup=keyboard2)

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value, callback_data=f"{key}"))
    return markup

async def tamilmv():
    mainUrl = 'https://www.1TamilMV.eu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }
    global movie_dict
    movie_dict = {}
    global real_dict
    real_dict = {}
    web = requests.request("GET", mainUrl, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')
    linker = []
    num = 0
    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})
    for i in range(21):
        title = temps[i].findAll('a')[0].text
        badtitles.append(title)
        links = temps[i].find('a')['href']
        content = str(links)
        linker.append(content)
    for element in badtitles:
        realtitles.append(title.strip())
        append.strip()
  are
        
